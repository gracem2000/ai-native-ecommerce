"""
服务层模块
统一的服务入口，协调各模块完成业务流程
"""
from typing import Dict, List, Optional, Callable
from src.hot_perception import HotPerception
from src.scene_mining import SceneMining
from src.product_matching import ProductMatching
from src.llm_client import GLMClient
from src.seasonal_perception import SeasonalPerception
from src.config import Config


class ScenarioService:
    """场景服务类 - 统一入口

    协调热点采集、场景挖掘、商品匹配三大核心模块
    """

    def __init__(self):
        """初始化服务"""
        print("\n🚀 初始化时空场景自动供给系统...")

        # 初始化各模块
        self.hot_perception = HotPerception()
        self.llm_client = GLMClient()
        self.scene_mining = SceneMining(llm_client=self.llm_client)
        self.product_matching = ProductMatching()
        self.seasonal_perception = SeasonalPerception(llm_client=self.llm_client)

        print("✅ 系统初始化完成\n")

    def run_full_pipeline(
        self,
        hot_limit: int = None,
        scene_limit: int = None
    ) -> Dict:
        """运行完整管道

        Args:
            hot_limit: 每个平台获取的热点数量
            scene_limit: 最多生成多少个场景

        Returns:
            完整的处理结果
        """
        if hot_limit is None:
            hot_limit = Config.HOT_FETCH_LIMIT
        if scene_limit is None:
            scene_limit = 5

        print("=" * 50)
        print("开始执行完整业务流程")
        print("=" * 50)

        # 1. 抓取热搜（百度 + 知乎）
        print("\n【步骤 1/3】抓取热点信息...")
        hot_data = self.hot_perception.fetch_all_hot_topics(limit=hot_limit)

        # 2. 获取合并后的热点标题（按热度排序）
        hot_titles = [t['title'] for t in hot_data.get('all_hot', [])]

        if not hot_titles:
            print("⚠️  未获取到热点信息，流程终止")
            return self._empty_result()

        # 3. 场景挖掘
        print(f"\n【步骤 2/3】场景挖掘 (处理 {min(len(hot_titles), scene_limit)} 条热点)...")
        scenes = self.scene_mining.mine_from_hot_topics(hot_titles, limit=scene_limit)

        if not scenes:
            print("⚠️  未生成任何场景，流程终止")
            return self._empty_result(hot_data=hot_data)

        # 4. 商品匹配
        print(f"\n【步骤 3/3】商品匹配 (为 {len(scenes)} 个场景匹配商品)...")
        for idx, scene in enumerate(scenes, 1):
            print(f"   [{idx}/{len(scenes)}] 匹配商品: {scene['scene_name']}")
            keywords = scene.get('potential_keywords', [])
            matched = self.product_matching.match_products(keywords)
            scene['matched_products'] = matched

        # 汇总结果
        result = {
            'success': True,
            'hot_topics': hot_data,
            'scenes': scenes,
            'total_scenes': len(scenes),
            'summary': {
                'baidu_count': len(hot_data.get('baidu_hot', [])),
                'total_hot': len(hot_data.get('all_hot', [])),
                'scenes_generated': len(scenes),
                'products_matched': sum(len(s.get('matched_products', [])) for s in scenes)
            }
        }

        print("\n" + "=" * 50)
        print("✅ 业务流程执行完成")
        print("=" * 50)
        print(f"📊 处理结果:")
        print(f"   - 热点信息: {result['summary']['total_hot']} 条")
        print(f"   - 生成场景: {result['summary']['scenes_generated']} 个")
        print(f"   - 匹配商品: {result['summary']['products_matched']} 个")
        print("=" * 50 + "\n")

        return result

    def run_full_pipeline_with_progress(
        self,
        hot_limit: int = None,
        scene_limit: int = None,
        progress_callback: Optional[Callable] = None
    ) -> Dict:
        """运行完整管道，支持进度回调

        Args:
            hot_limit: 每个平台获取的热点数量
            scene_limit: 最多生成多少个场景
            progress_callback: 进度回调函数，签名为 callback(event_type, *args)

        Returns:
            完整的处理结果
        """
        if hot_limit is None:
            hot_limit = Config.HOT_FETCH_LIMIT
        if scene_limit is None:
            scene_limit = 5

        results = {'hot_topics': {}, 'scenes': [], 'summary': {}}

        # 步骤1: 抓取热点
        if progress_callback:
            progress_callback('step', 1, 4, '【步骤 1/4】抓取热点信息...')
            progress_callback('info', '🔍 开始抓取热点信息...')

        print("\n【步骤 1/4】抓取热点信息...")
        hot_data = self.hot_perception.fetch_all_hot_topics(limit=hot_limit)

        # 传递热点抓取结果
        if progress_callback:
            progress_callback('baidu_result', len(hot_data.get('baidu_hot', [])))
            progress_callback('total_hot', len(hot_data.get('all_hot', [])))
            progress_callback('info', f"📊 共抓取 {len(hot_data.get('all_hot', []))} 条热点信息")

        results['hot_topics'] = hot_data

        # 获取热点标题
        hot_titles = [t['title'] for t in hot_data.get('all_hot', [])]

        if not hot_titles:
            if progress_callback:
                progress_callback('error', '未获取到热点信息')
            return self._empty_result(hot_data=hot_data)

        # 步骤2: 逐个处理热点
        if progress_callback:
            progress_callback('step', 2, 4, f'【步骤 2/4】场景挖掘 (处理 {min(len(hot_titles), scene_limit)} 条热点)...')

        print(f"\n【步骤 2/4】场景挖掘 (处理 {min(len(hot_titles), scene_limit)} 条热点)...")

        scenes_to_process = hot_titles[:scene_limit]
        for idx, topic in enumerate(scenes_to_process, 1):
            if progress_callback:
                progress_callback('processing', idx, len(scenes_to_process), topic)

            print(f"   [{idx}/{len(scenes_to_process)}] 处理: {topic[:50]}...")

            # LLM 处理开始
            if progress_callback:
                progress_callback('llm_start', topic)

            scene_data = self.scene_mining.llm.generate_scene(topic)
            if scene_data and scene_data.get('scene_name'):
                scene = self.scene_mining._create_scene_object(topic, scene_data)
                results['scenes'].append(scene)
                print(f"   ✅ 场景: {scene['scene_name']}")

                if progress_callback:
                    progress_callback('scene_generated', scene, f"✅ 场景: {scene['scene_name']}")
            else:
                print(f"   ⚠️  场景生成失败，跳过")
                if progress_callback:
                    progress_callback('scene_failed', topic, f"⚠️ 生成失败: {topic[:30]}...")

        if not results['scenes']:
            if progress_callback:
                progress_callback('error', '未生成任何场景')
            return self._empty_result(hot_data=hot_data)

        # 步骤3: 商品匹配
        if progress_callback:
            progress_callback('step', 3, 4, f'【步骤 3/4】商品匹配 (为 {len(results["scenes"])} 个场景匹配商品)...')

        print(f"\n【步骤 3/4】商品匹配 (为 {len(results['scenes'])} 个场景匹配商品)...")

        for idx, scene in enumerate(results['scenes'], 1):
            print(f"   [{idx}/{len(results['scenes'])}] 匹配商品: {scene['scene_name']}")
            keywords = scene.get('potential_keywords', [])

            if progress_callback:
                progress_callback('matching_start', scene['scene_name'], len(keywords))

            matched = self.product_matching.match_products(keywords)
            scene['matched_products'] = matched

            if progress_callback:
                progress_callback('matching_done', scene['scene_name'], len(matched))

        # 步骤4: 完成
        if progress_callback:
            progress_callback('step', 4, 4, '【步骤 4/4】处理完成!')
            progress_callback('complete', '✅ 所有处理已完成!')

        # 汇总结果
        results['summary'] = {
            'baidu_count': len(hot_data.get('baidu_hot', [])),
            'total_hot': len(hot_data.get('all_hot', [])),
            'scenes_generated': len(results['scenes']),
            'products_matched': sum(len(s.get('matched_products', [])) for s in results['scenes'])
        }

        results['success'] = True
        results['total_scenes'] = len(results['scenes'])

        print("\n" + "=" * 50)
        print("✅ 业务流程执行完成")
        print("=" * 50)
        print(f"📊 处理结果:")
        print(f"   - 热点信息: {results['summary']['total_hot']} 条")
        print(f"   - 生成场景: {results['summary']['scenes_generated']} 个")
        print(f"   - 匹配商品: {results['summary']['products_matched']} 个")
        print("=" * 50 + "\n")

        return results

    def submit_scene(self, scene_name: str) -> Dict:
        """人工提报场景并自动补全

        Args:
            scene_name: 场景名称

        Returns:
            包含生成场景或错误信息的字典
        """
        print(f"\n✍️ 人工提报场景: {scene_name}")

        # 使用 LLM 生成完整场景
        scene_data = self.scene_mining.llm.generate_scene(scene_name)

        if not scene_data or not scene_data.get('scene_name'):
            print("❌ 场景生成失败")
            return {'success': False, 'error': '场景生成失败，请稍后重试'}

        # 创建场景对象
        scene = self.scene_mining._create_scene_object(
            source_topic=f"人工提报: {scene_name}",
            scene_data=scene_data,
            source='manual',
            source_detail=scene_name
        )

        print(f"✅ 场景生成成功: {scene['scene_name']}")

        # 匹配商品
        keywords = scene.get('potential_keywords', [])
        matched = self.product_matching.match_products(keywords)
        scene['matched_products'] = matched

        print(f"🛍️ 匹配到 {len(matched)} 个相关商品")

        return {
            'success': True,
            'scene': scene
        }

    def save_scene(self, scene: Dict) -> bool:
        """保存单个场景到场景库

        Args:
            scene: 场景对象

        Returns:
            是否保存成功
        """
        try:
            self.scene_mining._save_scenes([scene])
            print(f"💾 场景已保存: {scene.get('scene_name', 'Unknown')}")
            return True
        except Exception as e:
            print(f"❌ 保存场景失败: {e}")
            return False

    def delete_scene(self, scene_id: str) -> bool:
        """删除场景

        Args:
            scene_id: 场景ID

        Returns:
            是否删除成功
        """
        try:
            # 加载所有场景
            all_scenes = self.scene_mining.load_scenes()

            # 过滤掉要删除的场景
            updated_scenes = [s for s in all_scenes if s.get('scene_id') != scene_id]

            # 保存更新后的场景列表
            if len(updated_scenes) < len(all_scenes):
                import json
                with open(Config.SCENARIOS_PATH, 'w', encoding='utf-8') as f:
                    json.dump(updated_scenes, f, ensure_ascii=False, indent=2)

                print(f"🗑️ 场景已删除: {scene_id}")
                return True
            else:
                print(f"⚠️ 未找到场景: {scene_id}")
                return False

        except Exception as e:
            print(f"❌ 删除场景失败: {e}")
            return False

    def get_scenes_by_source(self, source: str) -> List[Dict]:
        """按来源获取场景

        Args:
            source: 场景来源 (seasonal|hotspot|manual)

        Returns:
            该来源的场景列表
        """
        all_scenes = self.scene_mining.load_scenes()
        return [s for s in all_scenes if s.get('source') == source]

    def get_source_statistics(self) -> Dict:
        """获取各来源的统计数据

        Returns:
            各来源的统计信息
        """
        all_scenes = self.scene_mining.load_scenes()

        stats = {
            'seasonal': {'count': 0, 'scenes': []},
            'hotspot': {'count': 0, 'scenes': []},
            'manual': {'count': 0, 'scenes': []}
        }

        for scene in all_scenes:
            source = scene.get('source', 'hotspot')
            if source in stats:
                stats[source]['count'] += 1
                stats[source]['scenes'].append(scene)

        return stats

    def generate_seasonal_scenes(self, progress_callback=None) -> List[Dict]:
        """生成时节场景

        Args:
            progress_callback: 进度回调函数

        Returns:
            生成的场景列表
        """
        return self.seasonal_perception.generate_seasonal_scenes(progress_callback)

    def get_seasonal_statistics(self) -> Dict:
        """获取时节统计信息

        Returns:
            时节统计信息
        """
        return self.seasonal_perception.get_seasonal_statistics()

    def _empty_result(self, hot_data: Optional[Dict] = None) -> Dict:
        """返回空结果

        Args:
            hot_data: 可选的热点数据

        Returns:
            空结果字典
        """
        return {
            'success': False,
            'hot_topics': hot_data or {},
            'scenes': [],
            'total_scenes': 0,
            'summary': {
                'baidu_count': 0,
                'total_hot': 0,
                'scenes_generated': 0,
                'products_matched': 0
            },
            'error': '未生成有效场景'
        }

    def get_hot_topics_only(self, limit: int = None) -> Dict:
        """仅获取热点信息（不进行场景挖掘）

        Args:
            limit: 每个平台获取的热点数量

        Returns:
            热点数据
        """
        if limit is None:
            limit = Config.HOT_FETCH_LIMIT

        return self.hot_perception.fetch_all_hot_topics(limit=limit)

    def get_cached_result(self) -> Dict:
        """获取缓存的处理结果

        Returns:
            缓存的结果数据
        """
        import json
        import os

        result = {
            'hot_topics': self.hot_perception.load_cached_topics(),
            'scenes': self.scene_mining.load_scenes(),
            'products': self.product_matching.products
        }

        return result

    def health_check(self) -> Dict:
        """系统健康检查

        Returns:
            健康状态报告
        """
        checks = {
            'config': Config.ZHIPU_API_KEY is not None,
            'llm_client': self.llm_client.health_check(),
            'product_db': len(self.product_matching.products) > 0
        }

        all_healthy = all(checks.values())

        return {
            'healthy': all_healthy,
            'checks': checks,
            'details': {
                'products_loaded': len(self.product_matching.products),
                'llm_model': Config.DEFAULT_MODEL
            }
        }


# 创建全局服务实例
_service_instance = None


def get_service() -> ScenarioService:
    """获取服务实例（单例模式）

    Returns:
        ScenarioService 实例
    """
    global _service_instance
    if _service_instance is None:
        _service_instance = ScenarioService()
    return _service_instance


if __name__ == "__main__":
    # 测试代码
    service = ScenarioService()

    # 健康检查
    health = service.health_check()
    print("=== 健康检查 ===")
    print(json.dumps(health, ensure_ascii=False, indent=2))

    # 运行完整流程（使用缓存数据测试）
    print("\n=== 运行完整流程 ===")
    result = service.run_full_pipeline(hot_limit=5, scene_limit=3)
