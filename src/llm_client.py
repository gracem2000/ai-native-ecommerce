"""
LLM 客户端模块
使用智谱 AI 原生 SDK (zai-sdk)
"""
from zai import ZhipuAiClient
import json
from typing import Dict, Any, Optional, List
from src.config import Config


class GLMClient:
    """智谱 GLM 客户端封装

    使用智谱 AI 原生 SDK 调用 GLM 模型
    """

    def __init__(self, api_key: Optional[str] = None):
        """初始化客户端

        Args:
            api_key: API密钥，如果不提供则从配置中读取
        """
        self.api_key = api_key or Config.ZHIPU_API_KEY
        self.model = Config.DEFAULT_MODEL
        self.temperature = Config.TEMPERATURE
        self.max_tokens = Config.MAX_TOKENS

        if not self.api_key:
            raise ValueError("API Key 未设置，请在配置中提供 ZHIPU_API_KEY")

        try:
            self.client = ZhipuAiClient(api_key=self.api_key)
            print(f"✅ LLM 客户端初始化成功 (模型: {self.model})")
        except Exception as e:
            print(f"❌ LLM 客户端初始化失败: {e}")
            self.client = None

    def generate_scene(self, hot_topic: str, custom_prompt: Optional[str] = None) -> Dict[str, Any]:
        """将热点话题转化为购物场景

        Args:
            hot_topic: 热点话题标题
            custom_prompt: 可选的自定义提示，用于重新生成场景

        Returns:
            结构化的场景数据
        """
        if not self.client:
            print("⚠️  LLM 客户端未初始化，返回空场景")
            return self._empty_scene(hot_topic)

        # 使用自定义提示或默认提示
        prompt = custom_prompt if custom_prompt else self._build_scene_prompt(hot_topic)

        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]

        try:
            print(f"🤖 正在处理热点: {hot_topic[:30]}...")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )

            # 获取回复内容
            content = response.choices[0].message.content
            scene_data = self._parse_json_response(content)

            if scene_data:
                # 修正时间范围的年份
                scene_data = self._fix_temporal_scope_year(scene_data)
                print(f"✅ 场景生成成功: {scene_data.get('scene_name', 'Unknown')}")
                return scene_data
            else:
                print(f"⚠️  JSON 解析失败，使用原始响应")
                return self._fallback_scene(hot_topic, content)

        except Exception as e:
            print(f"❌ LLM 调用失败: {e}")
            import traceback
            traceback.print_exc()
            return self._empty_scene(hot_topic)

    def chat(self, messages: List[Dict], temperature: Optional[float] = None, max_tokens: Optional[int] = None) -> str:
        """通用多轮对话

        复用底层 chat.completions.create 调用，支持任意 messages 列表（多轮历史）。
        供对话式购物助手等场景使用。

        Args:
            messages: 对话消息列表，形如 [{"role": "user", "content": "..."}]
            temperature: 可选温度，默认使用配置值
            max_tokens: 可选最大 token 数，默认使用配置值

        Returns:
            模型回复的文本内容；客户端未初始化或调用失败时返回空字符串
        """
        if not self.client:
            print("⚠️  LLM 客户端未初始化，无法进行对话")
            return ""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens if max_tokens is not None else self.max_tokens,
                temperature=temperature if temperature is not None else self.temperature,
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            print(f"❌ LLM 对话调用失败: {e}")
            import traceback
            traceback.print_exc()
            return ""

    def _build_scene_prompt(self, hot_topic: str) -> str:
        """构建场景挖掘的 Prompt

        Args:
            hot_topic: 热点话题

        Returns:
            完整的 Prompt
        """
        # 获取当前日期
        from datetime import datetime
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_year = datetime.now().year

        return f"""你是一个电商场景挖掘专家。请将以下热点话题转化为购物场景。

当前日期: {current_date}
热点话题: {hot_topic}

请分析这个热点话题可能引发的购物需求，并以 JSON 格式输出，包含以下字段:
- scene_name: 场景名称（简洁明了，4-8个字）
- scene_type: 场景类型（赛事/热点/节日/季节/生活等）
- trigger_event: 触发事件（简短描述）
- temporal_scope: 时间范围（注意：必须是{current_year}年的日期，格式如"{current_date} 至 {current_year}-07-15"，如果是持续性场景可写"全年"）
- geo_scope: 地理范围（如"全国"或具体城市）
- user_intent: 用户意图描述（1-2句话）
- potential_keywords: 潜在商品关键词列表（5-8个关键词，用逗号分隔）
- target_population: 目标人群（如"男性球迷、聚会人群"）

重要提示：
1. 时间范围必须使用当前年份（{current_year}）的日期
2. 如果是热点事件，时间范围从今天开始，持续1-4周
3. 如果是季节性场景，使用当前年份的相关季节

只返回JSON内容，不要其他说明文字。

示例输出:
{{
  "scene_name": "世界杯球迷零食补给站",
  "scene_type": "赛事/热点",
  "trigger_event": "世界杯小组赛开赛",
  "temporal_scope": "{current_date} 至 {current_year}-07-15",
  "geo_scope": "全国",
  "user_intent": "看球时需要边吃边喝，避免饿肚子影响观赛体验",
  "potential_keywords": ["啤酒", "薯片", "小龙虾", "护肝片", "熬夜能量"],
  "target_population": "男性球迷、聚会人群"
}}"""

    def _fix_temporal_scope_year(self, scene_data: Dict[str, Any]) -> Dict[str, Any]:
        """修正时间范围的年份为当前年份

        Args:
            scene_data: 场景数据

        Returns:
            修正后的场景数据
        """
        from datetime import datetime
        import re

        current_year = datetime.now().year
        temporal_scope = scene_data.get('temporal_scope', '')

        # 如果时间范围为"全年"或类似，直接返回
        if not temporal_scope or '全年' in temporal_scope or '长期' in temporal_scope:
            return scene_data

        # 使用正则表达式替换所有4位年份为当前年份
        # 匹配格式：YYYY-MM-DD 或 YYYY/MM/DD 等
        def replace_year(match):
            return f"{current_year}-{match.group(2)}-{match.group(3)}" if len(match.groups()) >= 3 else f"{current_year}"

        # 匹配 2024-04-01 格式
        pattern = r'(\d{4})[-/](\d{1,2})[-/](\d{1,2})'
        fixed_scope = re.sub(pattern, f'{current_year}-\\2-\\3', temporal_scope)

        # 匹配 2024年4月 格式
        pattern_cn = r'(\d{4})年(\d{1,2})月'
        fixed_scope = re.sub(pattern_cn, f'{current_year}年\\2月', fixed_scope)

        # 如果修正后的时间范围与原范围不同，更新它
        if fixed_scope != temporal_scope:
            print(f"📅 修正时间范围: {temporal_scope} -> {fixed_scope}")
            scene_data['temporal_scope'] = fixed_scope

        return scene_data

    def _parse_json_response(self, content: str) -> Dict[str, Any]:
        """解析 LLM 返回的 JSON

        Args:
            content: LLM 返回的文本

        Returns:
            解析后的字典
        """
        try:
            # 清理可能的 markdown 标记
            content = content.strip()
            if content.startswith('```json'):
                content = content[7:]
            if content.startswith('```'):
                content = content[3:]
            if content.endswith('```'):
                content = content[:-3]

            content = content.strip()
            return json.loads(content)

        except json.JSONDecodeError:
            return {}

    def _empty_scene(self, hot_topic: str) -> Dict[str, Any]:
        """返回空场景（当处理失败时）

        Args:
            hot_topic: 原始热点话题

        Returns:
            空场景数据
        """
        return {
            'scene_name': f'场景: {hot_topic[:20]}',
            'scene_type': '未知',
            'trigger_event': hot_topic,
            'temporal_scope': '未知',
            'geo_scope': '未知',
            'user_intent': '暂无描述',
            'potential_keywords': [],
            'target_population': '未知'
        }

    def _fallback_scene(self, hot_topic: str, raw_response: str) -> Dict[str, Any]:
        """回退场景（当 JSON 解析失败时）

        Args:
            hot_topic: 原始热点话题
            raw_response: 原始响应

        Returns:
            包含原始响应的场景数据
        """
        return {
            'scene_name': f'场景: {hot_topic[:20]}',
            'scene_type': '需人工审核',
            'trigger_event': hot_topic,
            'temporal_scope': '待确定',
            'geo_scope': '待确定',
            'user_intent': raw_response[:100] if raw_response else '暂无描述',
            'potential_keywords': [],
            'target_population': '待确定',
            'raw_response': raw_response
        }

    def health_check(self) -> bool:
        """检查客户端健康状态

        Returns:
            是否可用
        """
        return self.client is not None

    def generate_multiple_scenes(self, topic: str, count: int = 5) -> list:
        """基于一个主题生成多个不同的购物场景

        Args:
            topic: 主题（如"端午节"、"春节"）
            count: 需要生成的场景数量

        Returns:
            场景列表
        """
        if not self.client:
            print("⚠️  LLM 客户端未初始化，返回空列表")
            return []

        from datetime import datetime
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_year = datetime.now().year

        prompt = f"""你是一个电商场景挖掘专家。请基于"{topic}"这个主题，生成 {count} 个不同角度的购物场景。

当前日期: {current_date}
主题: {topic}

请从不同角度分析这个主题可能引发的购物需求，例如：
- 礼品赠送场景
- 家庭聚会/出游场景
- DIY/自制场景
- 服饰穿搭场景
- 美食/餐饮场景
- 祈福/文化活动场景

请以 JSON 数组格式输出 {count} 个场景，每个场景包含:
- scene_name: 场景名称（简洁明了，4-8个字）
- scene_type: 场景类型（节日/热点/生活/文化等）
- trigger_event: 触发事件（简短描述）
- temporal_scope: 时间范围（注意：必须是{current_year}年的日期，格式如"{current_date} 至 {current_year}-07-15"）
- geo_scope: 地理范围（如"全国"或具体城市）
- user_intent: 用户意图描述（1-2句话）
- potential_keywords: 潜在商品关键词列表（5-8个关键词，用逗号分隔）
- target_population: 目标人群

重要提示：
1. 时间范围必须使用当前年份（{current_year}）的日期
2. 每个场景要有明显的区分度，避免重复
3. 场景名称要体现不同角度，如"端午礼品馈赠"、"端午家庭出游"、"端午粽子DIY"等

只返回JSON数组内容，不要其他说明文字。

示例输出格式:
[
  {{
    "scene_name": "端午礼品馈赠",
    "scene_type": "节日",
    "trigger_event": "端午节临近，走亲访友需备礼",
    "temporal_scope": "{current_date} 至 {current_year}-06-22",
    "geo_scope": "全国",
    "user_intent": "端午节期间需要准备体面的礼品送给长辈、朋友，表达心意与祝福",
    "potential_keywords": ["粽子礼盒", "咸鸭蛋", "茶叶礼盒", "滋补保健品", "端午香囊"],
    "target_population": "探亲访友人群、职场送礼人群"
  }},
  ... 更多场景
]"""

        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]

        try:
            print(f"🤖 正在为「{topic}」生成 {count} 个场景...")

            # 增加max_tokens以支持多个场景
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens * 3,  # 增加token限制
                temperature=0.8,  # 稍微提高温度以增加多样性
            )

            # 获取回复内容
            content = response.choices[0].message.content

            # 解析JSON数组
            scenes_data = self._parse_json_array_response(content)

            if scenes_data and len(scenes_data) > 0:
                # 修正每个场景的时间范围年份
                scenes_data = [self._fix_temporal_scope_year(scene) for scene in scenes_data]
                print(f"✅ 成功生成 {len(scenes_data)} 个场景")
                for idx, scene in enumerate(scenes_data, 1):
                    print(f"   [{idx}] {scene.get('scene_name', 'Unknown')}")
                return scenes_data
            else:
                print(f"⚠️  JSON 解析失败")
                return []

        except Exception as e:
            print(f"❌ LLM 调用失败: {e}")
            import traceback
            traceback.print_exc()
            return []

    def _parse_json_array_response(self, content: str) -> list:
        """解析 LLM 返回的 JSON 数组

        Args:
            content: LLM 返回的文本

        Returns:
            解析后的列表
        """
        try:
            # 清理可能的 markdown 标记
            content = content.strip()
            if content.startswith('```json'):
                content = content[7:]
            if content.startswith('```'):
                content = content[3:]
            if content.endswith('```'):
                content = content[:-3]

            content = content.strip()
            return json.loads(content)

        except (json.JSONDecodeError, ValueError):
            # 尝试从内容中提取JSON数组
            import re
            array_match = re.search(r'\[.*\]', content, re.DOTALL)
            if array_match:
                try:
                    return json.loads(array_match.group())
                except:
                    pass
            return []


if __name__ == "__main__":
    # 测试代码
    import os

    if not os.getenv("ZHIPU_API_KEY"):
        print("⚠️  请设置 ZHIPU_API_KEY 环境变量")
    else:
        client = GLMClient()

        # 测试场景生成
        test_topic = "2026世界杯今日开幕 梅西领衔阿根廷队"
        scene = client.generate_scene(test_topic)

        print("\n=== 生成的场景 ===")
        print(json.dumps(scene, ensure_ascii=False, indent=2))
