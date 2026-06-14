"""
配置管理模块
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """应用配置类"""

    # ==================== API 配置 ====================
    ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")
    ZHIPU_BASE_URL = os.getenv("ZHIPU_BASE_URL", "https://open.bigmodel.cn/api/anthropic")

    # ==================== 数据路径 ====================
    # 项目根目录
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data")

    # 数据文件路径
    PRODUCT_DB_PATH = os.path.join(DATA_DIR, "mock_products.json")
    HOT_TOPICS_PATH = os.path.join(DATA_DIR, "hot_topics.json")
    SCENARIOS_PATH = os.path.join(DATA_DIR, "scenarios.json")
    FESTIVALS_PATH = os.path.join(DATA_DIR, "festivals.json")

    # ==================== 热搜抓取配置 ====================
    BAIDU_HOT_URL = "https://top.baidu.com/board?tab=realtime"
    ZHIHU_HOT_URL = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total"
    FETCH_INTERVAL = 1800  # 30分钟
    HOT_FETCH_LIMIT = 10  # 每个平台获取前N条

    # ==================== LLM 配置 ====================
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "glm-5.1")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))

    # ==================== 商品匹配配置 ====================
    MAX_MATCH_PRODUCTS = int(os.getenv("MAX_MATCH_PRODUCTS", "5"))
    MIN_CONFIDENCE = float(os.getenv("MIN_CONFIDENCE", "0.3"))

    # ==================== 超时配置 ====================
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))

    @classmethod
    def validate(cls):
        """验证必要配置"""
        if not cls.ZHIPU_API_KEY:
            raise ValueError("ZHIPU_API_KEY 未设置，请在 .env 文件中配置")


# 验证配置
try:
    Config.validate()
except ValueError as e:
    print(f"⚠️  配置警告: {e}")
