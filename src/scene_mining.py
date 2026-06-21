"""
场景挖掘模块
使用 LLM 将热点话题转化为购物场景
"""
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from difflib import SequenceMatcher
import random
import string
from src.llm_client import GLMClient
from src.config import Config


class SceneMining:
    """场景挖掘类 - 使用 LLM 将热点转化为购物场景"""

    def __init__(self, llm_client: Optional[GLMClient] = None):
        """初始化场景挖掘器

        Args:
            llm_client: LLM 客户端，如果不提供则自动创建
        """
        self.llm = llm_client or GLMClient()
        self.scenes = []
        # 去重阈值配置
        self.SIMILARITY_THRESHOLD = 0.75  # 相似度阈值
        self.TIME_WINDOW_HOURS = 24  # 时间窗口（小时）
        # 场景计数器，用于生成唯一ID
        self._scene_counter = 0

    def _generate_unique_scene_id(self) -> str:
        """生成唯一的场景ID

        Returns:
            唯一的场景ID
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        # 使用毫秒级时间戳 + 随机字符串确保唯一性
        microseconds = datetime.now().microsecond
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        self._scene_counter += 1
        return f"scene_{timestamp}_{microseconds}_{random_str}_{self._scene_counter}"

    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """计算两个文本的相似度

        Args:
            text1: 第一个文本
            text2: 第二个文本

        Returns:
            相似度分数 (0-1)
        """
        if not text1 or not text2:
            return 0.0
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

    def _calculate_keyword_overlap(self, keywords1: List[str], keywords2: List[str]) -> float:
        """计算关键词重叠度

        Args:
            keywords1: 第一个关键词列表
            keywords2: 第二个关键词列表

        Returns:
            重叠度分数 (0-1)
        """
        if not keywords1 or not keywords2:
            return 0.0

        set1 = set(kw.lower() for kw in keywords1)
        set2 = set(kw.lower() for kw in keywords2)

        intersection = set1 & set2
        union = set1 | set2

        return len(intersection) / len(union) if union else 0.0

    def _is_within_time_window(self, scene1: Dict, scene2: Dict) -> bool:
        """检查两个场景是否在时间窗口内

        Args:
            scene1: 第一个场景
            scene2: 第二个场景

        Returns:
            是否在时间窗口内
        """
        try:
            time1 = datetime.fromisoformat(scene1.get('created_at', ''))
            time2 = datetime.fromisoformat(scene2.get('created_at', ''))
            time_diff = abs(time1 - time2)
            return time_diff <= timedelta(hours=self.TIME_WINDOW_HOURS)
        except:
            return True  # 如果无法解析时间，保守处理

    def _is_scene_similar(self, new_scene: Dict, existing_scene: Dict) -> Tuple[bool, str]:
        """检查两个场景是否相似

        Args:
            new_scene: 新场景
            existing_scene: 已存在的场景

        Returns:
            (是否相似, 相似原因)
        """
        # 1. 检查场景名称相似度
        name_similarity = self._calculate_text_similarity(
            new_scene.get('scene_name', ''),
            existing_scene.get('scene_name', '')
        )

        if name_similarity >= self.SIMILARITY_THRESHOLD:
            return True, f"场景名称相似 ({name_similarity:.2%})"

        # 2. 检查触发事件相似度
        trigger_similarity = self._calculate_text_similarity(
            new_scene.get('trigger_event', ''),
            existing_scene.get('trigger_event', '')
        )

        if trigger_similarity >= self.SIMILARITY_THRESHOLD:
            return True, f"触发事件相似 ({trigger_similarity:.2%})"

        # 3. 检查关键词重叠度（高权重）
        keyword_overlap = self._calculate_keyword_overlap(
            new_scene.get('potential_keywords', []),
            existing_scene.get('potential_keywords', [])
        )

        if keyword_overlap >= 0.6:  # 关键词重叠60%以上认为相似
            return True, f"关键词重叠度高 ({keyword_overlap:.2%})"

        # 4. 综合判断：如果名称+触发事件都中等相似，且在时间窗口内
        if (name_similarity >= 0.5 and trigger_similarity >= 0.5 and
            self._is_within_time_window(new_scene, existing_scene)):
            return True, f"综合相似且时间相近 (名称:{name_similarity:.2%}, 事件:{trigger_similarity:.2%})"

        return False, ""

    def _check_duplicate_scene(self, new_scene: Dict, existing_scenes: List[Dict]) -> Tuple[bool, Optional[Dict], str]:
        """检查新场景是否与已有场景重复

        Args:
            new_scene: 新场景
            existing_scenes: 已有场景列表

        Returns:
            (是否重复, 重复的场景对象, 原因)
        """
        for existing_scene in existing_scenes:
            is_similar, reason = self._is_scene_similar(new_scene, existing_scene)
            if is_similar:
                return True, existing_scene, reason
        return False, None, ""

    def mine_from_hot_topics(
        self,
        hot_topics: List[str],
        limit: int = 5
    ) -> List[Dict]:
        """从热搜列表中挖掘场景

        Args:
            hot_topics: 热点话题列表
            limit: 最多处理多少条热搜

        Returns:
            场景列表
        """
        print(f"\n🎯 开始场景挖掘，共 {len(hot_topics)} 条热搜")

        scenes = []
        processed_count = 0

        for idx, topic in enumerate(hot_topics[:limit], 1):
            print(f"\n[{idx}/{min(limit, len(hot_topics))}] 处理: {topic[:50]}...")

            scene_data = self.llm.generate_scene(topic)

            if scene_data and scene_data.get('scene_name'):
                scene = self._create_scene_object(topic, scene_data, source='hotspot', source_detail=topic)
                scenes.append(scene)
                processed_count += 1
                print(f"   ✅ 场景: {scene['scene_name']}")
            else:
                print(f"   ⚠️  场景生成失败，跳过")

        # 保存场景
        if scenes:
            self._save_scenes(scenes)
            self.scenes.extend(scenes)

        print(f"\n📊 场景挖掘完成: 成功 {processed_count}/{limit} 条")
        return scenes

    @staticmethod
    def _normalize_keywords(raw_keywords) -> list:
        """规范化关键词：兼容 LLM 返回的逗号分隔字符串 or 数组，去单字/去空"""
        if isinstance(raw_keywords, str):
            raw_keywords = [k.strip() for k in raw_keywords.split(',') if k.strip()]
        if not isinstance(raw_keywords, list):
            return []
        result = []
        for k in raw_keywords:
            k = SceneMining._sanitize(str(k))
            if len(k) >= 2:   # 过滤单字（如 "钢"、"笔"）
                result.append(k)
        return result

    @staticmethod
    def _sanitize(text: str) -> str:
        """清理文本：去首尾空格/换行/tab、折叠多余空格、去特殊符号/热搜尾标签"""
        if not isinstance(text, str):
            return text
        import re
        text = text.strip()
        text = re.sub(r'[\r\n\t]+', ' ', text)
        text = re.sub(r' {2,}', ' ', text)
        # 去半角特殊符号
        text = re.sub(r'[#@￥$%^&*|\\/`~\[\]{}⟨⟩「」『』【】()（）]', '', text)
        # 去首尾多余标点
        text = re.sub(r'^[：:。，,；;！!？?"\'…—\-\.\s]+', '', text)
        text = re.sub(r'[：:。，,；;！!？?"\'…—\-\.\s]+$', '', text)
        # 去热搜尾部标签（空格 + 单字如 热/新/沸/爆/荐 等）
        text = re.sub(r'\s+[热新沸腾爆荐顶]$', '', text)
        text = text.strip()
        return text

    def _create_scene_object(self, source_topic: str, scene_data: Dict, source: str = 'hotspot', source_detail: str = '') -> Dict:
        """创建场景对象（所有文本字段均经过 sanitize 处理）"""
        source_type_map = {
            'seasonal': '时节',
            'hotspot': '热点',
            'manual': '人工'
        }
        # 原文保留一份（调试用），展示用字段做清理
        raw_topic = str(source_topic or '')
        raw_detail = str(source_detail or '')
        return {
            'scene_id': self._generate_unique_scene_id(),
            'source': source,
            'source_type': source_type_map.get(source, '热点'),
            'source_detail': self._sanitize(raw_detail or raw_topic),
            'source_topic': self._sanitize(raw_topic),
            'created_at': datetime.now().isoformat(),
            'scene_name': self._sanitize(scene_data.get('scene_name', '未知场景')),
            'scene_type': self._sanitize(scene_data.get('scene_type', '未知')),
            'trigger_event': self._sanitize(scene_data.get('trigger_event', '')),
            'temporal_scope': self._sanitize(str(scene_data.get('temporal_scope', '未知'))),
            'geo_scope': self._sanitize(str(scene_data.get('geo_scope', '未知'))),
            'user_intent': self._sanitize(scene_data.get('user_intent', '')),
            'potential_keywords': self._normalize_keywords(
                scene_data.get('potential_keywords', [])
            ),
            'target_population': self._sanitize(scene_data.get('target_population', '未知')),
            'confidence': 0.8
        }

    def _save_scenes(self, scenes: List[Dict], auto_deduplicate: bool = True) -> Dict[str, any]:
        """保存场景到文件（支持智能去重）

        Args:
            scenes: 要保存的场景列表
            auto_deduplicate: 是否启用智能去重

        Returns:
            保存结果字典，包含：
            - saved: 成功保存的场景数量
            - skipped: 跳过的场景数量
            - skipped_scenes: 跳过的场景详情列表
        """
        result = {
            'saved': 0,
            'skipped': 0,
            'skipped_scenes': []
        }

        try:
            import os
            os.makedirs(os.path.dirname(Config.SCENARIOS_PATH), exist_ok=True)

            # 读取现有场景
            existing_scenes = []
            try:
                with open(Config.SCENARIOS_PATH, 'r', encoding='utf-8') as f:
                    existing_scenes = json.load(f)
            except FileNotFoundError:
                pass

            # 过滤要保存的场景
            new_scenes = []

            for scene in scenes:
                if auto_deduplicate:
                    # 智能去重检查
                    is_duplicate, duplicate_scene, reason = self._check_duplicate_scene(scene, existing_scenes)

                    if is_duplicate:
                        result['skipped'] += 1
                        result['skipped_scenes'].append({
                            'scene_name': scene.get('scene_name', 'Unknown'),
                            'duplicate_of': duplicate_scene.get('scene_name', 'Unknown'),
                            'reason': reason
                        })
                        print(f"⚠️  跳过重复场景: {scene.get('scene_name')} - {reason}")
                        continue

                # 检查 scene_id 去重（最后的防线）
                existing_scene_ids = {s['scene_id'] for s in existing_scenes + new_scenes}
                if scene['scene_id'] not in existing_scene_ids:
                    new_scenes.append(scene)
                else:
                    # scene_id 重复，计入跳过统计
                    result['skipped'] += 1
                    result['skipped_scenes'].append({
                        'scene_name': scene.get('scene_name', 'Unknown'),
                        'duplicate_of': '已有场景（ID重复）',
                        'reason': '场景ID已存在（可能是同时生成导致）'
                    })
                    print(f"⚠️  跳过重复场景: {scene.get('scene_name')} - 场景ID已存在")

            # 保存新场景
            if new_scenes:
                merged_scenes = existing_scenes + new_scenes

                with open(Config.SCENARIOS_PATH, 'w', encoding='utf-8') as f:
                    json.dump(merged_scenes, f, ensure_ascii=False, indent=2)

                print(f"💾 场景数据已保存 ({len(new_scenes)} 条新增)")
                result['saved'] = len(new_scenes)
            else:
                print("💾 所有场景已存在或重复，无需保存")

            # 如果有跳过的场景，打印汇总
            if result['skipped'] > 0:
                print(f"📊 去重汇总: 跳过 {result['skipped']} 个重复场景")

        except Exception as e:
            print(f"⚠️  保存场景失败: {e}")

        return result

    def load_scenes(self) -> List[Dict]:
        """加载所有已保存的场景

        Returns:
            场景列表
        """
        try:
            with open(Config.SCENARIOS_PATH, 'r', encoding='utf-8') as f:
                scenes = json.load(f)
                print(f"📂 已加载 {len(scenes)} 条场景")
                return scenes
        except FileNotFoundError:
            print("📂 暂无保存的场景")
            return []
        except Exception as e:
            print(f"⚠️  加载场景失败: {e}")
            return []

    def get_recent_scenes(self, limit: int = 10) -> List[Dict]:
        """获取最近的场景

        Args:
            limit: 返回数量

        Returns:
            场景列表
        """
        scenes = self.load_scenes()
        # 按创建时间倒序排列
        scenes.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        return scenes[:limit]

    def clear_scenes(self):
        """清空所有场景"""
        try:
            with open(Config.SCENARIOS_PATH, 'w', encoding='utf-8') as f:
                json.dump([], f)
            print("🗑️  场景数据已清空")
        except Exception as e:
            print(f"⚠️  清空场景失败: {e}")


if __name__ == "__main__":
    # 测试代码
    mining = SceneMining()

    # 模拟热搜数据
    test_topics = [
        "2026世界杯今日开幕 梅西领衔阿根廷队",
        "突发降温 南方多地迎来冷空气",
        "春节档电影票房破纪录"
    ]

    scenes = mining.mine_from_hot_topics(test_topics, limit=3)

    print("\n=== 生成的场景 ===")
    for scene in scenes:
        print(f"\n📌 {scene['scene_name']}")
        print(f"   触发事件: {scene['trigger_event']}")
        print(f"   关键词: {', '.join(scene['potential_keywords'])}")
