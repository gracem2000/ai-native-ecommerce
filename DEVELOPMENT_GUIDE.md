# 时空场景自动供给系统 - 完整开发指南

> 项目定位：基于 LLM 的电商场景智能供给系统，展示从"热点感知"到"交易闭环"的 AI-Native 能力

---

## 📋 目录

1. [项目概览](#项目概览)
2. [技术栈](#技术栈)
3. [项目结构](#项目结构)
4. [数据模型设计](#数据模型设计)
5. [核心模块实现](#核心模块实现)
6. [API 设计](#api-设计)
7. [前端设计](#前端设计)
8. [开发步骤](#开发步骤)
9. [部署指南](#部署指南)

---

## 项目概览

### 核心业务流程

```
外部热搜 → 热点采集 → LLM场景挖掘 → 关键词提取 → 商品匹配 → 前端展示
```

### 三大核心能力

1. **热点感知能力** - 实时抓取全网热点话题
2. **场景理解能力** - LLM将非结构化新闻转化为购物场景
3. **商品匹配能力** - 基于场景关键词自动关联商品库

---

## 技术栈

| 层级 | 技术选择 | 说明 |
|------|----------|------|
| **后端框架** | Python 3.10+ | 主要开发语言 |
| **LLM** | 智谱 GLM-5.1 | 场景理解和推理 |
| **数据采集** | Requests, BeautifulSoup4 | 热搜抓取 |
| **数据处理** | Pandas | CSV数据处理 |
| **数据存储** | JSON | 模拟商品库 |
| **前端框架** | Streamlit | 快速构建Demo界面 |
| **定时任务** | APScheduler | 定时抓取热搜 |
| **配置管理** | python-dotenv | 环境变量管理 |

---

## 项目结构

```
smart-scenario-system/
├── data/
│   ├── mock_products.json          # 模拟商品库
│   ├── hot_topics.json              # 缓存的热搜数据
│   └── scenarios.json              # 生成的场景数据
├── src/
│   ├── __init__.py
│   ├── config.py                    # 配置管理
│   ├── hot_perception.py            # 热点采集模块
│   ├── scene_mining.py              # 场景挖掘模块 (LLM)
│   ├── product_matching.py         # 商品匹配模块
│   ├── llm_client.py                # GLM-5.1 客户端封装
│   └── utils.py                     # 工具函数
├── ui/
│   ├── __init__.py
│   ├── app.py                       # Streamlit 主应用
│   ├── pages/
│   │   ├── 1_热点监控.py
│   │   ├── 2_场景挖掘.py
│   │   └── 3_商品匹配.py
│   └── components/
│       ├── __init__.py
│       └── visualizations.py        # 可视化组件
├── tests/
│   ├── test_hot_perception.py
│   ├── test_scene_mining.py
│   └── test_product_matching.py
├── requirements.txt
├── .env.example
├── .gitignore
├── project.md
├── DEVELOPMENT_GUIDE.md            # 本文档
└── README.md
```

---

## 数据模型设计

### 1. 商品数据模型 (mock_products.json)

```json
{
  "products": [
    {
      "sku_id": "10001",
      "title": "青岛啤酒经典10度500ml*24听",
      "category": "酒水饮料",
      "tags": ["啤酒", "聚会", "世界杯", "看球"],
      "price": 79.9,
      "stock": 1000,
      "image_url": "/images/beer.jpg"
    },
    {
      "sku_id": "10002",
      "title": "乐事薯片原味黄瓜味混合装",
      "category": "休闲零食",
      "tags": ["薯片", "零食", "看剧", "聚会"],
      "price": 45.0,
      "stock": 500,
      "image_url": "/images/chips.jpg"
    },
    {
      "sku_id": "10003",
      "title": "Swisse 斯维诗 护肝片 180片",
      "category": "医疗保健",
      "tags": ["护肝", "熬夜", "解酒", "保健"],
      "price": 128.0,
      "stock": 300,
      "image_url": "/images/liver.jpg"
    },
    {
      "sku_id": "10004",
      "title": "泡泡玛特 Labubu 世界杯系列盲盒",
      "category": "潮玩手办",
      "tags": ["盲盒", "拉布布", "世界杯", "收藏"],
      "price": 399.0,
      "stock": 50,
      "image_url": "/images/labubu.jpg"
    }
  ]
}
```

### 2. 场景数据模型 (参考 CSV 格式)

```json
{
  "scene_id": "scene_20260614_001",
  "scene_name": "世界杯球迷零食补给站",
  "scene_type": "赛事/热点",
  "trigger_event": "世界杯小组赛开赛",
  "temporal_scope": {
    "start_date": "2026-06-14",
    "end_date": "2026-07-15",
    "time_ranges": ["18:00-24:00"]
  },
  "geo_scope": "全国",
  "user_intent": "看球时需要边吃边喝，避免饿肚子影响观赛体验",
  "potential_keywords": ["啤酒", "薯片", "小龙虾", "护肝片", "熬夜能量"],
  "target_population": "男性球迷、聚会人群",
  "confidence": 0.95,
  "created_at": "2026-06-14T10:00:00Z",
  "source": "llm_generated",
  "matched_products": ["10001", "10002", "10003"]
}
```

### 3. 热搜数据模型

```json
{
  "fetch_time": "2026-06-14T10:00:00Z",
  "source": "baidu_hot",
  "topics": [
    {
      "rank": 1,
      "title": "2026世界杯今日开幕 梅西领衔阿根廷队",
      "heat": 500000,
      "url": "https://..."
    }
  ]
}
```

---

## 核心模块实现

### 模块 1: 配置管理 (src/config.py)

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API 配置
    ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")
    ZHIPU_BASE_URL = "https://open.bigmodel.cn/api/anthropic"

    # 数据路径
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    PRODUCT_DB_PATH = os.path.join(DATA_DIR, "mock_products.json")
    HOT_TOPICS_PATH = os.path.join(DATA_DIR, "hot_topics.json")
    SCENARIOS_PATH = os.path.join(DATA_DIR, "scenarios.json")

    # 热搜抓取配置
    BAIDU_HOT_URL = "https://top.baidu.com/board?tab=realtime"
    ZHIHU_HOT_URL = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total"
    FETCH_INTERVAL = 1800  # 30分钟
    HOT_FETCH_LIMIT = 10  # 每个平台获取前N条

    # LLM 配置
    DEFAULT_MODEL = "glm-5.1"
    TEMPERATURE = 0.7
    MAX_TOKENS = 2000

    # 商品匹配配置
    MAX_MATCH_PRODUCTS = 5
    MIN_CONFIDENCE = 0.3
```

### 模块 2: 热点采集 (src/hot_perception.py)

```python
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from typing import List, Dict
from src.config import Config

class HotPerception:
    """热点采集模块 - 负责抓取全网热搜榜单

    支持: 百度热搜、知乎热榜
    """

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def fetch_baidu_hot(self, limit: int = 10) -> List[Dict]:
        """抓取百度热搜

        Args:
            limit: 获取前N条热搜

        Returns:
            热搜话题列表
        """
        try:
            response = requests.get(Config.BAIDU_HOT_URL, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')

            topics = []
            items = soup.select('.category-wrap_iQLoo.horizontal_1eKy4 .item-wrap_3og7X')

            for idx, item in enumerate(items[:limit], 1):
                title_elem = item.select_one('.title_dIF3r')
                if title_elem:
                    heat_score = item.get('data-score', '0')
                    topics.append({
                        'rank': idx,
                        'title': title_elem.text.strip(),
                        'heat': int(heat_score) if heat_score.isdigit() else 0,
                        'source': 'baidu',
                        'url': f"https://www.baidu.com/s?wd={title_elem.text.strip()}"
                    })

            print(f"✅ 百度热搜: 抓取 {len(topics)} 条")
            return topics

        except Exception as e:
            print(f"❌ 抓取百度热搜失败: {e}")
            return []

    def fetch_zhihu_hot(self, limit: int = 10) -> List[Dict]:
        """抓取知乎热榜

        Args:
            limit: 获取前N条热榜

        Returns:
            热榜话题列表
        """
        try:
            # 知乎热榜 API
            url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total"
            params = {'limit': limit}

            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            data = response.json()

            topics = []
            hot_list = data.get('data', [])

            for idx, item in enumerate(hot_list[:limit], 1):
                target = item.get('target', {})
                title = target.get('title', '')
                heat = item.get('detail_text', '').replace('万热度', '').replace('热度', '')

                topics.append({
                    'rank': idx,
                    'title': title,
                    'heat': self._parse_heat(heat),
                    'source': 'zhihu',
                    'url': f"https://www.zhihu.com/question/{target.get('id', '')}"
                })

            print(f"✅ 知乎热榜: 抓取 {len(topics)} 条")
            return topics

        except Exception as e:
            print(f"❌ 抓取知乎热榜失败: {e}")
            return []

    def _parse_heat(self, heat_str: str) -> int:
        """解析热度字符串为数字"""
        try:
            heat_str = heat_str.replace('万', '0000').replace('亿', '00000000')
            return int(float(heat_str))
        except:
            return 0

    def fetch_all_hot_topics(self, limit: int = 10) -> Dict:
        """抓取所有热搜并合并

        Args:
            limit: 每个平台获取前N条

        Returns:
            合并后的热搜数据
        """
        print("\n🔍 开始抓取热点信息...")

        baidu_topics = self.fetch_baidu_hot(limit)
        zhihu_topics = self.fetch_zhihu_hot(limit)

        # 合并所有热搜
        all_topics = baidu_topics + zhihu_topics
        all_topics.sort(key=lambda x: x['heat'], reverse=True)

        result = {
            'fetch_time': datetime.now().isoformat(),
            'baidu_hot': baidu_topics,
            'zhihu_hot': zhihu_topics,
            'all_hot': all_topics[:20]  # 取热度Top20
        }

        # 保存到文件
        self._save_to_file(result)

        print(f"📊 共抓取 {len(all_topics)} 条热点信息")
        return result

    def _save_to_file(self, data: Dict):
        """保存到文件"""
        try:
            with open(Config.HOT_TOPICS_PATH, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存文件失败: {e}")
```

### 模块 3: LLM 客户端 (src/llm_client.py)

```python
import anthropic
from src.config import Config
from typing import Dict, Any

class GLMClient:
    """智谱 GLM-5.1 客户端封装"""

    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=Config.ZHIPU_API_KEY,
            base_url=Config.ZHIPU_BASE_URL
        )
        self.model = Config.DEFAULT_MODEL

    def generate_scene(self, hot_topic: str) -> Dict[str, Any]:
        """
        将热点话题转化为购物场景

        Args:
            hot_topic: 热点话题标题

        Returns:
            结构化的场景数据
        """
        prompt = f"""你是一个电商场景挖掘专家。请将以下热点话题转化为购物场景。

热点话题: {hot_topic}

请以 JSON 格式输出，包含以下字段:
- scene_name: 场景名称（简洁明了）
- scene_type: 场景类型（赛事/热点/节日/季节等）
- trigger_event: 触发事件
- temporal_scope: 时间范围
- geo_scope: 地理范围
- user_intent: 用户意图描述
- potential_keywords: 潜在商品关键词列表（5-8个）
- target_population: 目标人群

只返回JSON，不要其他内容。"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=Config.MAX_TOKENS,
                temperature=Config.TEMPERATURE,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            import json
            content = response.content[0].text
            # 清理可能的 markdown 标记
            if content.startswith('```json'):
                content = content[7:]
            if content.startswith('```'):
                content = content[3:]
            if content.endswith('```'):
                content = content[:-3]

            return json.loads(content.strip())

        except Exception as e:
            print(f"LLM 调用失败: {e}")
            return {}
```

### 模块 4: 场景挖掘 (src/scene_mining.py)

```python
import json
from datetime import datetime
from typing import List, Dict
from src.llm_client import GLMClient
from src.config import Config

class SceneMining:
    """场景挖掘模块 - 使用 LLM 将热点转化为购物场景"""

    def __init__(self):
        self.llm = GLMClient()

    def mine_from_hot_topics(self, hot_topics: List[str]) -> List[Dict]:
        """
        从热搜列表中挖掘场景

        Args:
            hot_topics: 热点话题列表

        Returns:
            场景列表
        """
        scenes = []

        for topic in hot_topics[:5]:  # 处理 Top 5
            print(f"正在处理: {topic}")

            scene_data = self.llm.generate_scene(topic)

            if scene_data:
                scene = {
                    'scene_id': f"scene_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    'source_topic': topic,
                    'created_at': datetime.now().isoformat(),
                    **scene_data
                }
                scenes.append(scene)

        # 保存场景
        self._save_scenes(scenes)
        return scenes

    def _save_scenes(self, scenes: List[Dict]):
        """保存场景到文件"""
        existing_scenes = []

        try:
            with open(Config.SCENARIOS_PATH, 'r', encoding='utf-8') as f:
                existing_scenes = json.load(f)
        except FileNotFoundError:
            pass

        merged_scenes = existing_scenes + scenes

        with open(Config.SCENARIOS_PATH, 'w', encoding='utf-8') as f:
            json.dump(merged_scenes, f, ensure_ascii=False, indent=2)
```

### 模块 5: 商品匹配 (src/product_matching.py)

```python
import json
from typing import List, Dict, Tuple
from src.config import Config

class ProductMatching:
    """商品匹配模块 - 基于场景关键词匹配商品"""

    def __init__(self):
        self.products = self._load_products()

    def _load_products(self) -> List[Dict]:
        """加载商品库"""
        try:
            with open(Config.PRODUCT_DB_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('products', [])
        except FileNotFoundError:
            print(f"商品库文件不存在: {Config.PRODUCT_DB_PATH}")
            return []

    def match_products(self, keywords: List[str], top_k: int = 5) -> List[Dict]:
        """
        基于关键词匹配商品

        Args:
            keywords: 场景关键词列表
            top_k: 返回商品数量

        Returns:
            匹配的商品列表，按相关性排序
        """
        scored_products = []

        for product in self.products:
            score = self._calculate_relevance(product, keywords)
            if score > Config.MIN_CONFIDENCE:
                scored_products.append({
                    **product,
                    'relevance_score': score
                })

        # 按相关性排序
        scored_products.sort(key=lambda x: x['relevance_score'], reverse=True)

        return scored_products[:top_k]

    def _calculate_relevance(self, product: Dict, keywords: List[str]) -> float:
        """
        计算商品与关键词的相关性分数

        策略:
        1. 标题完全匹配: 1.0 分
        2. 标签匹配: 0.8 分
        3. 类别匹配: 0.5 分
        """
        score = 0.0

        for keyword in keywords:
            keyword = keyword.lower()

            # 标题匹配
            if keyword in product['title'].lower():
                score += 1.0

            # 标签匹配
            for tag in product.get('tags', []):
                if keyword in tag.lower():
                    score += 0.8

            # 类别匹配
            if keyword in product.get('category', '').lower():
                score += 0.5

        return min(score, 1.0)  # 最高1.0分
```

---

## API 设计

### 核心服务类 (src/service.py)

```python
from src.hot_perception import HotPerception
from src.scene_mining import SceneMining
from src.product_matching import ProductMatching

class ScenarioService:
    """场景服务 - 统一入口"""

    def __init__(self):
        self.hot_perception = HotPerception()
        self.scene_mining = SceneMining()
        self.product_matching = ProductMatching()

    def run_full_pipeline(self, hot_limit: int = 10) -> Dict:
        """运行完整管道

        Args:
            hot_limit: 每个平台获取的热点数量

        Returns:
            完整的处理结果
        """
        # 1. 抓取热搜（百度 + 知乎）
        hot_data = self.hot_perception.fetch_all_hot_topics(limit=hot_limit)

        # 2. 获取合并后的热点标题（按热度排序）
        hot_titles = [t['title'] for t in hot_data.get('all_hot', [])]

        # 3. 场景挖掘
        scenes = self.scene_mining.mine_from_hot_topics(hot_titles)

        # 4. 商品匹配
        for scene in scenes:
            keywords = scene.get('potential_keywords', [])
            matched = self.product_matching.match_products(keywords)
            scene['matched_products'] = matched

        return {
            'hot_topics': hot_data,
            'scenes': scenes,
            'total_scenes': len(scenes),
            'summary': {
                'baidu_count': len(hot_data.get('baidu_hot', [])),
                'zhihu_count': len(hot_data.get('zhihu_hot', [])),
                'total_hot': len(hot_data.get('all_hot', []))
            }
        }
```

---

## 前端设计

### 主应用 (ui/app.py)

```python
import streamlit as st
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.service import ScenarioService

st.set_page_config(
    page_title="时空场景自动供给系统",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("⚡ 时空场景自动供给系统")
st.markdown("从热点感知到交易闭环的 AI-Native 演示")

# 侧边栏
with st.sidebar:
    st.header("⚙️ 系统控制")

    st.subheader("抓取设置")
    hot_limit = st.slider("每平台热点数量", 5, 20, 10)

    if st.button("🔄 运行完整管道", type="primary"):
        with st.spinner("正在抓取热点并生成场景..."):
            service = ScenarioService()
            result = service.run_full_pipeline(hot_limit=hot_limit)
            st.session_state.result = result
        st.success(f"✅ 成功生成 {result['total_scenes']} 个场景!")

# 主内容区
if 'result' in st.session_state:
    result = st.session_state.result

    # 显示汇总信息
    summary = result.get('summary', {})
    st.info(f"""
    📊 **数据汇总**:
    - 百度热搜: {summary.get('baidu_count', 0)} 条
    - 知乎热榜: {summary.get('zhihu_count', 0)} 条
    - 总热点数: {summary.get('total_hot', 0)} 条
    - 生成场景: {result['total_scenes']} 个
    """)

    tab1, tab2, tab3 = st.tabs(["🔥 热点监控", "🎯 场景挖掘", "🛍️ 商品匹配"])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🔴 百度热搜")
            for topic in result['hot_topics'].get('baidu_hot', []):
                st.markdown(f"**#{topic['rank']}** {topic['title']}")

        with col2:
            st.subheader("🔵 知乎热榜")
            for topic in result['hot_topics'].get('zhihu_hot', []):
                st.markdown(f"**#{topic['rank']}** {topic['title']}")

    with tab2:
        st.subheader("AI 生成的购物场景")
        for scene in result['scenes']:
            with st.expander(f"📌 {scene['scene_name']}"):
                st.write(f"**触发事件**: {scene.get('trigger_event')}")
                st.write(f"**目标人群**: {scene.get('target_population')}")
                st.write(f"**关键词**: {', '.join(scene.get('potential_keywords', []))}")

    with tab3:
        st.subheader("匹配商品推荐")
        for scene in result['scenes']:
            st.markdown(f"### 📌 {scene['scene_name']}")
            products = scene.get('matched_products', [])
            if products:
                cols = st.columns(min(len(products), 3))
                for idx, product in enumerate(products):
                    with cols[idx % 3]:
                        st.markdown(f"**{product['title']}**")
                        st.metric("价格", f"¥{product['price']}", f"相关性: {product['relevance_score']:.2f}")
```

---

## 开发步骤

### Phase 1: 环境搭建 (Day 1)

1. 创建项目目录结构
2. 配置虚拟环境
3. 安装依赖包

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # macOS/Linux

# 安装依赖
pip install -r requirements.txt
```

### Phase 2: 数据准备 (Day 1)

1. 创建 mock 商品库
2. 准备示例热搜数据

### Phase 3: 核心模块开发 (Day 2-3)

1. **热点采集模块**
   - 实现百度热搜抓取
   - 实现数据清洗

2. **LLM 集成**
   - 封装 GLM-5.1 客户端
   - 编写场景挖掘 Prompt

3. **场景挖掘模块**
   - 实现 LLM 调用逻辑
   - 实现结果解析和存储

4. **商品匹配模块**
   - 实现关键词匹配算法
   - 实现相关性排序

### Phase 4: 前端开发 (Day 4)

1. 创建 Streamlit 应用
2. 设计多页面布局
3. 添加可视化组件

### Phase 5: 测试与优化 (Day 5)

1. 单元测试
2. 集成测试
3. 性能优化

### Phase 6: 部署 (Day 6)

1. GitHub 代码托管
2. Streamlit Cloud 部署
3. 密钥配置

---

## 部署指南

### 本地开发

```bash
# 1. 配置环境变量
cp .env.example .env
# 编辑 .env 填入 ZHIPU_API_KEY

# 2. 运行应用
streamlit run ui/app.py
```

### Streamlit Cloud 部署

1. **GitHub 仓库**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Streamlit Secrets**
   在 Streamlit Cloud 的 Settings → Secrets 中添加:
   ```
   ZHIPU_API_KEY=your_api_key_here
   ```

3. **部署配置**
   - Repository: your-username/smart-scenario-system
   - Branch: main
   - Main file: ui/app.py

---

## 依赖包 (requirements.txt)

```
streamlit==1.31.0
anthropic==0.18.0
requests==2.31.0
beautifulsoup4==4.12.0
pandas==2.0.0
python-dotenv==1.0.0
apscheduler==3.10.0
```

---

## 环境变量模板 (.env.example)

```
# 智谱 AI 配置
ZHIPU_API_KEY=your_zhipu_api_key_here

# 可选: Anthropic 官方 API (如果使用)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

---

## 扩展功能建议

1. **定时任务**: 使用 APScheduler 实现自动定时抓取
2. **数据持久化**: 集成 SQLite 或 MongoDB 存储历史数据
3. **可视化增强**: 添加时间轴、关系图等可视化
4. **A/B 测试**: 对比不同 Prompt 的效果
5. **监控告警**: 添加异常监控和告警机制

---

## 常见问题

**Q: LLM 输出格式不稳定怎么办?**
A: 使用 JSON Mode 或添加 Few-shot Examples

**Q: 商品匹配准确率低?**
A: 优化相关性算法，加入更多特征（类别、品牌等）

**Q: Streamlit 部署后加载慢?**
A: 添加缓存机制，使用 `@st.cache_data`

---

Document Version: 1.0
Created: 2026-06-14
Author: Development Team
