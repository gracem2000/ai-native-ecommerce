"""
个性化推荐引擎模块
面向终端用户的"AI 购物助手"核心：结合用户画像 + 时节/热点场景 + 商品库，
通过 LLM 进行多轮对话式推荐，并给出推荐理由。

设计原则：
- 最大化复用现有 llm_client（通用 chat）与 product_matching（商品库 / sku 还原）
- 推荐结果"落地化"：LLM 只能从受约束的候选商品库中选 sku，杜绝幻觉商品
"""
import json
import re
from typing import Dict, List, Optional, Any

from src.config import Config


class Recommender:
    """对话式个性化推荐引擎"""

    # 每个来源取最近多少条场景作为推荐上下文
    SCENES_PER_SOURCE = 3
    # 候选商品库上限（控制 token）
    MAX_CANDIDATES = 40
    # 单次最多推荐商品数
    MAX_RECOMMENDATIONS = 4

    def __init__(self, llm_client, product_matching, service):
        """初始化推荐引擎

        Args:
            llm_client: GLMClient 实例（复用其 chat() 与 _parse_json_response）
            product_matching: ProductMatching 实例（提供商品库与 sku 还原）
            service: ScenarioService 实例（提供 get_scenes_by_source 取活跃场景）
        """
        self.llm_client = llm_client
        self.product_matching = product_matching
        self.service = service
        self.users = self._load_profiles()

    # ==================== 用户画像 ====================

    def _load_profiles(self) -> List[Dict]:
        """加载用户画像数据"""
        try:
            with open(Config.USER_PROFILES_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                users = data.get('users', [])
                print(f"👤 已加载 {len(users)} 个用户画像")
                return users
        except FileNotFoundError:
            print(f"⚠️  用户画像文件不存在: {Config.USER_PROFILES_PATH}")
            return []
        except Exception as e:
            print(f"⚠️  加载用户画像失败: {e}")
            return []

    def list_users(self) -> List[Dict]:
        """返回所有用户（供登录 UI 使用）"""
        return self.users

    def get_profile(self, user_id: str) -> Optional[Dict]:
        """根据 user_id 获取完整画像"""
        for u in self.users:
            if u.get('user_id') == user_id:
                return u
        return None

    # ==================== 上下文组装 ====================

    def _get_active_scenes(self) -> List[Dict]:
        """取最近的时节 + 热点场景作为推荐上下文"""
        scenes: List[Dict] = []
        try:
            for source in ('seasonal', 'hotspot'):
                raw = self.service.get_scenes_by_source(source) or []
                # 按创建时间倒序取最近若干条
                raw = sorted(raw, key=lambda s: s.get('created_at', ''), reverse=True)
                scenes.extend(raw[:self.SCENES_PER_SOURCE])
        except Exception as e:
            print(f"⚠️  获取活跃场景失败: {e}")
        return scenes

    def _get_candidate_catalog(self, profile: Dict) -> List[Dict]:
        """按用户偏好品类过滤候选商品库（预算范围内优先），返回精简字段"""
        fav_cats = set(profile.get('preferences', {}).get('favorite_categories', []))
        price_range = profile.get('preferences', {}).get('price_range', [])
        p_min, p_max = (price_range[0], price_range[1]) if len(price_range) >= 2 else (None, None)

        products = self.product_matching.products or []

        # 1) 偏好品类命中
        candidates = [p for p in products if p.get('category') in fav_cats]
        # 2) 若命中过少，回退到全部商品（按品类排序，偏好品类在前）
        if len(candidates) < 10:
            candidates = sorted(
                products,
                key=lambda p: 0 if p.get('category') in fav_cats else 1
            )

        # 预算范围内优先排序
        def in_budget(p):
            price = p.get('price', 0)
            if p_min is not None and p_max is not None:
                return p_min <= price <= p_max
            return False

        candidates.sort(key=lambda p: 0 if in_budget(p) else 1)

        # 精简字段 + 截断
        slim = []
        for p in candidates[:self.MAX_CANDIDATES]:
            slim.append({
                'sku_id': p.get('sku_id'),
                'title': p.get('title'),
                'category': p.get('category'),
                'tags': p.get('tags', []),
                'price': p.get('price'),
            })
        return slim

    def _profile_text(self, profile: Dict) -> str:
        """把用户画像渲染成给 LLM 看的文本摘要（含历史兴趣）"""
        basics = profile.get('basics', {})
        prefs = profile.get('preferences', {})
        history = profile.get('history', {})

        # 历史 sku → 商品标题，让 LLM 理解"历史兴趣"
        purchased_titles = []
        for sku in history.get('purchased', []):
            prod = self.product_matching.get_product_by_sku(sku)
            if prod:
                purchased_titles.append(prod.get('title'))

        lines = [
            f"- 姓名/人设: {profile.get('name')}，{profile.get('persona')}",
            f"- 基础画像: {basics.get('age')}岁/{basics.get('gender')}/{basics.get('city')}/{basics.get('occupation')}",
            f"- 偏好品类: {', '.join(prefs.get('favorite_categories', []))}",
            f"- 预算区间: ¥{prefs.get('price_range', ['?', '?'])[0]} ~ ¥{prefs.get('price_range', ['?', '?'])[1]}",
            f"- 兴趣标签: {', '.join(profile.get('interests', []))}",
        ]
        if purchased_titles:
            lines.append(f"- 近期购买(历史兴趣): {'; '.join(purchased_titles)}")
        if history.get('search_keywords'):
            lines.append(f"- 近期搜索: {', '.join(history.get('search_keywords', []))}")
        return "\n".join(lines)

    def _scenes_text(self, scenes: List[Dict]) -> str:
        """把活跃场景渲染成文本"""
        if not scenes:
            return "（暂无活跃时节/热点场景）"
        lines = []
        for s in scenes:
            tag = s.get('source_type') or s.get('source', '场景')
            lines.append(
                f"- [{tag}] {s.get('scene_name')}：{s.get('trigger_event', '')}"
                f"（时间: {s.get('temporal_scope', '未知')}；关键词: {', '.join(s.get('potential_keywords', [])[:5])}）"
            )
        return "\n".join(lines)

    def _catalog_text(self, catalog: List[Dict]) -> str:
        """把候选商品库渲染成紧凑文本"""
        lines = []
        for c in catalog:
            tags = '/'.join(c.get('tags', [])[:4])
            lines.append(f"- sku={c.get('sku_id')} | {c.get('title')} | {c.get('category')} | {tags} | ¥{c.get('price')}")
        return "\n".join(lines)

    # ==================== 对话 + 推荐 ====================

    def _build_system_prompt(self, profile: Dict, scenes: List[Dict], catalog: List[Dict]) -> str:
        """构建系统提示"""
        return f"""你是「{profile.get('name')}」的专属 AI 购物助手，运行在一个时空场景智能供给电商系统中。
你的任务是通过自然对话，结合【用户画像】、【当前时节/热点场景】和【候选商品库】，给出个性化的商品推荐并说明理由。

【用户画像】
{self._profile_text(profile)}

【当前时节/热点场景】（推荐时可主动结合这些场景，让推荐"应时应景"）
{self._scenes_text(scenes)}

【候选商品库】（你【只能】从这个库中选择推荐商品的 sku_id，禁止编造库外商品）
{self._catalog_text(catalog)}

【对话与推荐规则】
1. 语气贴合用户人设，亲切、有同理心，像一个懂 ta 的朋友。reply 控制在 2-3 句话以内，把回复写得精炼，避免冗长。
2. 主动结合用户的兴趣/历史购买和当前时节/热点场景来推荐，让推荐显得"懂 ta、又应景"。
3. 只在确实相关时推荐商品，每次不超过 {self.MAX_RECOMMENDATIONS} 件；不相关时可以只聊天不给推荐。
4. 推荐理由要具体，最好点明"为什么适合 ta（画像/兴趣/历史）"以及"和当前什么场景相关"。
5. 你必须严格只返回一个 JSON 对象（不要 markdown、不要多余文字），格式如下：
{{
  "reply": "你对用户说的话（自然语言）",
  "recommendations": [
    {{"sku_id": "候选库中的sku", "reason": "针对这个用户的推荐理由"}}
  ]
}}
当无需推荐商品时，recommendations 返回空数组 []。"""

    def chat(self, user_id: str, history: List[Dict]) -> Dict[str, Any]:
        """执行一轮对话式推荐

        Args:
            user_id: 当前登录用户 id
            history: 对话历史，形如 [{"role": "user"/"assistant", "content": "..."}]，
                     末尾应为最新一条用户消息

        Returns:
            {
              "reply": 助手回复文本,
              "recommendations": [{"product": 完整商品, "reason": 理由}],
              "active_scenes": 本次参考的场景摘要列表
            }
        """
        profile = self.get_profile(user_id)
        if not profile:
            return {
                "reply": "未找到该用户画像，请重新登录。",
                "recommendations": [],
                "active_scenes": [],
            }

        scenes = self._get_active_scenes()
        catalog = self._get_candidate_catalog(profile)
        system_prompt = self._build_system_prompt(profile, scenes, catalog)

        messages = [{"role": "system", "content": system_prompt}] + (history or [])

        content = self.llm_client.chat(messages, temperature=0.7, max_tokens=2000)
        if not content:
            return {
                "reply": "（助手暂时没有响应，请稍后再试）",
                "recommendations": [],
                "active_scenes": self._scene_summary(scenes),
            }

        data = self._safe_parse_json(content)
        reply = data.get('reply') or content
        recommendations = self._resolve_recommendations(data.get('recommendations', []))

        return {
            "reply": reply,
            "recommendations": recommendations,
            "active_scenes": self._scene_summary(scenes),
        }

    def _safe_parse_json(self, content: str) -> Dict:
        """容错解析 LLM 返回的 JSON（先复用客户端解析，再正则兜底提取首个对象）"""
        data = self.llm_client._parse_json_response(content)
        if isinstance(data, dict) and data:
            return data
        # 兜底：从文本中抽取第一个 {...} 块
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            try:
                obj = json.loads(match.group())
                if isinstance(obj, dict):
                    return obj
            except Exception:
                pass
        return {}

    def _resolve_recommendations(self, raw_recs: Any) -> List[Dict]:
        """把 LLM 返回的 sku_id 还原为完整商品，过滤幻觉 sku 与重复"""
        if not isinstance(raw_recs, list):
            return []
        resolved = []
        seen = set()
        for rec in raw_recs[:self.MAX_RECOMMENDATIONS * 2]:
            if not isinstance(rec, dict):
                continue
            sku_id = str(rec.get('sku_id', '')).strip()
            if not sku_id or sku_id in seen:
                continue
            product = self.product_matching.get_product_by_sku(sku_id)
            if not product:
                continue  # 过滤掉库外的幻觉 sku
            seen.add(sku_id)
            resolved.append({
                'product': product,
                'reason': (rec.get('reason') or '').strip() or '契合你的兴趣与当前场景',
            })
            if len(resolved) >= self.MAX_RECOMMENDATIONS:
                break
        return resolved

    def _scene_summary(self, scenes: List[Dict]) -> List[Dict]:
        """给 UI 透明展示用的场景摘要"""
        return [
            {
                'source_type': s.get('source_type') or s.get('source', '场景'),
                'scene_name': s.get('scene_name'),
                'trigger_event': s.get('trigger_event', ''),
            }
            for s in scenes
        ]


if __name__ == "__main__":
    # 冒烟测试：打印画像 + 活跃场景 + 候选库，并在有 API Key 时模拟一轮对话
    import os
    from src.service import get_service

    svc = get_service()
    rec = Recommender(svc.llm_client, svc.product_matching, svc)

    print("\n=== 用户列表 ===")
    for u in rec.list_users():
        print(f"  {u['avatar_emoji']} {u['name']} ({u['user_id']})")

    for u in rec.list_users():
        uid = u['user_id']
        profile = rec.get_profile(uid)
        print(f"\n=== {u['name']} 画像摘要 ===")
        print(rec._profile_text(profile))

        scenes = rec._get_active_scenes()
        print(f"\n--- 活跃场景 ({len(scenes)} 条) ---")
        print(rec._scenes_text(scenes))

        catalog = rec._get_candidate_catalog(profile)
        print(f"\n--- 候选商品库 ({len(catalog)} 件) ---")
        for c in catalog[:5]:
            print(f"  {c['sku_id']} | {c['title']} | ¥{c['price']}")
        if len(catalog) > 5:
            print(f"  ... 共 {len(catalog)} 件")

    if not os.getenv("ZHIPU_API_KEY"):
        print("\n⚠️  未设置 ZHIPU_API_KEY，跳过在线对话测试")
    else:
        print("\n=== 模拟对话 (Marla) ===")
        result = rec.chat("marla", [{"role": "user", "content": "周末想出去玩，帮我推荐点东西"}])
        print(f"回复: {result['reply']}")
        print(f"参考场景: {[s['scene_name'] for s in result['active_scenes']]}")
        for r in result['recommendations']:
            print(f"  💡 {r['product']['title']} — {r['reason']}")
