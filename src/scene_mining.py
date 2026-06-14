"""
场景挖掘模块
使用 LLM 将热点话题转化为购物场景
"""
import json
from datetime import datetime
from typing import List, Dict, Optional
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

    def _create_scene_object(self, source_topic: str, scene_data: Dict, source: str = 'hotspot', source_detail: str = '') -> Dict:
        """创建场景对象

        Args:
            source_topic: 原始热点话题
            scene_data: LLM 生成的场景数据
            source: 场景来源 (seasonal|hotspot|manual)
            source_detail: 来源详情描述

        Returns:
            完整的场景对象
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # 来源映射到中文
        source_type_map = {
            'seasonal': '时节',
            'hotspot': '热点',
            'manual': '人工'
        }

        return {
            'scene_id': f"scene_{timestamp}",
            'source': source,
            'source_type': source_type_map.get(source, '热点'),
            'source_detail': source_detail or source_topic,
            'source_topic': source_topic,
            'created_at': datetime.now().isoformat(),
            'scene_name': scene_data.get('scene_name', '未知场景'),
            'scene_type': scene_data.get('scene_type', '未知'),
            'trigger_event': scene_data.get('trigger_event', ''),
            'temporal_scope': scene_data.get('temporal_scope', '未知'),
            'geo_scope': scene_data.get('geo_scope', '未知'),
            'user_intent': scene_data.get('user_intent', ''),
            'potential_keywords': scene_data.get('potential_keywords', []),
            'target_population': scene_data.get('target_population', '未知'),
            'confidence': 0.8  # 默认置信度
        }

    def _save_scenes(self, scenes: List[Dict]):
        """保存场景到文件

        Args:
            scenes: 要保存的场景列表
        """
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

            # 合并场景（去重）
            existing_scene_ids = {s['scene_id'] for s in existing_scenes}
            new_scenes = [s for s in scenes if s['scene_id'] not in existing_scene_ids]

            if new_scenes:
                merged_scenes = existing_scenes + new_scenes

                with open(Config.SCENARIOS_PATH, 'w', encoding='utf-8') as f:
                    json.dump(merged_scenes, f, ensure_ascii=False, indent=2)

                print(f"💾 场景数据已保存 ({len(new_scenes)} 条新增)")
            else:
                print("💾 所有场景已存在，无需保存")

        except Exception as e:
            print(f"⚠️  保存场景失败: {e}")

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
