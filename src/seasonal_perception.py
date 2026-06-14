"""
时节感知模块
负责生成节日、节气相关的购物场景
"""
import json
from datetime import datetime, timedelta
from typing import List, Dict
from src.config import Config
from src.llm_client import GLMClient


class SeasonalPerception:
    """时节感知类 - 生成节日、节气相关场景"""

    def __init__(self, llm_client: GLMClient = None):
        """初始化时节感知器

        Args:
            llm_client: LLM客户端，如果不提供则自动创建
        """
        self.llm = llm_client or GLMClient()
        self.festivals_data = self._load_festivals()

    def _load_festivals(self) -> Dict:
        """加载节日数据

        Returns:
            节日数据字典
        """
        try:
            with open(Config.FESTIVALS_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️  节日数据文件未找到: {Config.FESTIVALS_PATH}")
            return {'traditional_festivals': [], 'modern_festivals': [], 'solar_terms': []}
        except Exception as e:
            print(f"⚠️  加载节日数据失败: {e}")
            return {'traditional_festivals': [], 'modern_festivals': [], 'solar_terms': []}

    def get_current_seasonal_events(self, days_before: int = 7, days_after: int = 30) -> List[Dict]:
        """获取当前时节相关的所有事件（节日、节气）

        Args:
            days_before: 向前查找天数
            days_after: 向后查找天数

        Returns:
            时节事件列表
        """
        today = datetime.now()
        start_date = today - timedelta(days=days_before)
        end_date = today + timedelta(days=days_after)

        events = []

        # 合并所有节日和节气
        all_events = (
            self.festivals_data.get('traditional_festivals', []) +
            self.festivals_data.get('modern_festivals', []) +
            self.festivals_data.get('solar_terms', [])
        )

        for event in all_events:
            event_date = self._parse_event_date(event['date'])
            if start_date <= event_date <= end_date:
                events.append({
                    **event,
                    'date_obj': event_date,
                    'days_until': (event_date - today).days
                })

        # 按距离天数排序
        events.sort(key=lambda x: abs(x['days_until']))

        return events

    def generate_seasonal_scenes(self, progress_callback=None) -> List[Dict]:
        """生成时节场景

        Args:
            progress_callback: 进度回调函数

        Returns:
            生成的场景列表
        """
        print("\n📅 开始时节场景生成...")

        # 获取当前时节事件
        events = self.get_current_seasonal_events()

        if not events:
            print("⚠️  当前时节无相关事件")
            return []

        scenes = []
        total_events = len(events)

        for idx, event in enumerate(events, 1):
            event_name = event['name']
            days_until = event['days_until']

            # 构建场景名称
            if days_until < 0:
                scene_name = f"{event_name}进行时"
            elif days_until == 0:
                scene_name = f"{event_name}当天"
            else:
                scene_name = f"{event_name}临近"

            print(f"[{idx}/{total_events}] 生成场景: {scene_name}")

            if progress_callback:
                progress_callback('processing', idx, total_events, scene_name)

            # 使用LLM生成场景
            scene_data = self.llm.generate_scene(scene_name)

            if scene_data and scene_data.get('scene_name'):
                # 创建时节场景对象
                from src.scene_mining import SceneMining
                mining = SceneMining(llm_client=self.llm)

                # 计算时间范围
                event_date = event['date_obj']
                temporal_scope = self._calculate_temporal_scope(event_date, days_until)

                scene = mining._create_scene_object(
                    source_topic=f"时节事件: {event_name}",
                    scene_data=scene_data,
                    source='seasonal',
                    source_detail=event_name
                )

                # 覆盖时节相关字段
                scene['temporal_scope'] = temporal_scope
                scene['seasonal_event'] = {
                    'name': event_name,
                    'date': event['date'],
                    'days_until': days_until,
                    'type': event.get('type', 'traditional')
                }

                scenes.append(scene)
                print(f"   ✅ 场景: {scene['scene_name']}")
            else:
                print(f"   ⚠️  场景生成失败")

        print(f"\n📊 时节场景生成完成: {len(scenes)}/{total_events}")

        # 保存场景
        if scenes:
            from src.scene_mining import SceneMining
            mining = SceneMining(llm_client=self.llm)
            mining._save_scenes(scenes)

        return scenes

    def _parse_event_date(self, date_str: str) -> datetime:
        """解析事件日期字符串

        Args:
            date_str: 日期字符串，格式为 MM-DD

        Returns:
            日期对象（当年）
        """
        try:
            month, day = map(int, date_str.split('-'))
            # 获取当前年份的日期
            today = datetime.now()
            event_date = datetime(today.year, month, day)

            # 如果事件已过，使用明年日期
            if event_date < today:
                event_date = datetime(today.year + 1, month, day)

            return event_date
        except Exception as e:
            print(f"⚠️  日期解析失败: {date_str}, {e}")
            return datetime.now()

    def _calculate_temporal_scope(self, event_date: datetime, days_until: int) -> str:
        """计算时间范围

        Args:
            event_date: 事件日期
            days_until: 距离天数

        Returns:
            时间范围描述
        """
        if days_until < 0:
            # 事件已过，返回已过去的时间范围
            start = event_date - timedelta(days=7)
            end = event_date + timedelta(days=3)
            return f"{start.strftime('%Y-%m-%d')} 至 {end.strftime('%Y-%m-%d')}"
        elif days_until == 0:
            # 当天
            return event_date.strftime('%Y-%m-%d')
        else:
            # 未来事件
            start = event_date - timedelta(days=7)
            end = event_date + timedelta(days=3)
            return f"{start.strftime('%Y-%m-%d')} 至 {end.strftime('%Y-%m-%d')}"

    def get_upcoming_events(self, days: int = 30) -> List[Dict]:
        """获取未来N天内的时节事件

        Args:
            days: 查询天数

        Returns:
            时节事件列表
        """
        today = datetime.now()
        end_date = today + timedelta(days=days)

        events = []

        all_events = (
            self.festivals_data.get('traditional_festivals', []) +
            self.festivals_data.get('modern_festivals', []) +
            self.festivals_data.get('solar_terms', [])
        )

        for event in all_events:
            event_date = self._parse_event_date(event['date'])
            if today <= event_date <= end_date:
                events.append({
                    **event,
                    'date_obj': event_date,
                    'days_until': (event_date - today).days
                })

        events.sort(key=lambda x: x['days_until'])

        return events

    def get_seasonal_statistics(self) -> Dict:
        """获取时节统计信息

        Returns:
            统计信息字典
        """
        upcoming_events = self.get_upcoming_events(days=30)

        return {
            'total_festivals': len(self.festivals_data.get('traditional_festivals', [])) +
                               len(self.festivals_data.get('modern_festivals', [])),
            'total_solar_terms': len(self.festivals_data.get('solar_terms', [])),
            'upcoming_count': len(upcoming_events),
            'upcoming_events': upcoming_events[:5]  # 返回前5个
        }


if __name__ == "__main__":
    # 测试代码
    perception = SeasonalPerception()

    print("=== 时节统计 ===")
    stats = perception.get_seasonal_statistics()
    print(f"节日总数: {stats['total_festivals']}")
    print(f"节气总数: {stats['total_solar_terms']}")
    print(f"未来30天事件: {stats['upcoming_count']}")

    print("\n=== 未来事件 ===")
    for event in stats['upcoming_events']:
        print(f"{event['name']} - {event['days_until']}天后")
