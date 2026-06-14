"""
热点采集模块
负责抓取百度热搜等外部热点信息
"""
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from typing import List, Dict
from src.config import Config


class HotPerception:
    """热点采集类 - 负责抓取全网热搜榜单

    支持: 百度热搜
    """

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def fetch_baidu_hot(self, limit: int = 20) -> List[Dict]:
        """抓取百度热搜

        Args:
            limit: 获取前N条热搜

        Returns:
            热搜话题列表
        """
        try:
            response = requests.get(
                Config.BAIDU_HOT_URL,
                headers=self.headers,
                timeout=Config.REQUEST_TIMEOUT
            )
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')

            topics = []
            # 百度热搜的CSS选择器
            title_links = soup.select('a[class*="title_dIF3"]')

            for idx, link in enumerate(title_links[:limit], 1):
                title = link.text.strip()
                # 热度值：使用排名作为热度（排名越高热度越大）
                heat = (len(title_links) - idx + 1) * 10000

                # 尝试获取热度数值（如果有）
                heat_elem = link.find_next_sibling(['div', 'span'], class_=lambda x: x and 'heat' in x.lower() if x else False)
                if heat_elem:
                    try:
                        heat_text = heat_elem.text.strip()
                        # 提取数字
                        import re
                        heat_match = re.search(r'(\d+)', heat_text)
                        if heat_match:
                            heat = int(heat_match.group(1))
                    except:
                        pass

                topics.append({
                    'rank': idx,
                    'title': title,
                    'heat': heat,
                    'source': 'baidu',
                    'url': f"https://www.baidu.com/s?wd={title}",
                    'fetched_at': datetime.now().isoformat()
                })

            print(f"✅ 百度热搜: 抓取 {len(topics)} 条")
            return topics

        except Exception as e:
            print(f"❌ 抓取百度热搜失败: {e}")
            return []

    def fetch_all_hot_topics(self, limit: int = None) -> Dict:
        """抓取所有热搜

        Args:
            limit: 获取前N条，默认使用配置中的值

        Returns:
            热搜数据
        """
        if limit is None:
            limit = Config.HOT_FETCH_LIMIT

        print("\n🔍 开始抓取热点信息...")

        baidu_topics = self.fetch_baidu_hot(limit)

        result = {
            'fetch_time': datetime.now().isoformat(),
            'baidu_hot': baidu_topics,
            'all_hot': baidu_topics  # 直接使用百度热搜作为全部热点
        }

        # 保存到文件
        self._save_to_file(result)

        print(f"📊 共抓取 {len(baidu_topics)} 条热点信息")
        return result

    def _save_to_file(self, data: Dict):
        """保存热搜数据到文件

        Args:
            data: 要保存的数据
        """
        try:
            # 确保目录存在
            import os
            os.makedirs(os.path.dirname(Config.HOT_TOPICS_PATH), exist_ok=True)

            with open(Config.HOT_TOPICS_PATH, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"💾 热搜数据已保存到 {Config.HOT_TOPICS_PATH}")
        except Exception as e:
            print(f"⚠️  保存文件失败: {e}")

    def load_cached_topics(self) -> Dict:
        """加载缓存的热搜数据

        Returns:
            缓存的热搜数据，如果没有则返回空字典
        """
        try:
            with open(Config.HOT_TOPICS_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except Exception as e:
            print(f"⚠️  加载缓存失败: {e}")
            return {}


if __name__ == "__main__":
    # 测试代码
    perception = HotPerception()
    result = perception.fetch_all_hot_topics(limit=5)

    print("\n=== 百度热搜 ===")
    for topic in result['baidu_hot']:
        print(f"#{topic['rank']} {topic['title']} (热度: {topic['heat']})")
