# CLAUDE.md - 时空场景自动供给系统

## 项目概述

这是一个 **AI-Native 电商场景智能供给系统**，通过引入智谱 GLM-5.1 大模型，重构传统电商供给链路。将 LLM 作为系统的"感知器官"和"推理大脑"，实现对外部热点的毫秒级响应，自动构建时空场景并完成商品匹配。

### 核心业务流程
```
外部热搜 → 热点采集 → LLM场景挖掘 → 关键词提取 → 商品匹配 → 前端展示
```

### 三大核心能力
- **热点感知能力** - 实时抓取全网热点话题（百度热搜、知乎热榜）
- **场景理解能力** - LLM 将非结构化新闻转化为购物场景
- **商品匹配能力** - 基于场景关键词自动关联商品库

---

## 项目结构

```
JD/
├── data/                              # 数据目录
│   ├── mock_products.json            # 模拟商品库 (30个示例商品)
│   ├── hot_topics.json               # 缓存的热搜数据
│   ├── scenarios.json                # 生成的场景数据
│   ├── festivals.json                 # 节日数据
│   └── hot_topics.json               # 热点数据
├── src/                              # 核心业务逻辑
│   ├── config.py                     # 配置管理
│   ├── hot_perception.py              # 热点采集模块
│   ├── seasonal_perception.py         # 季节性场景感知
│   ├── llm_client.py                  # GLM-5.1 客户端封装
│   ├── scene_mining.py                # 场景挖掘模块 (LLM核心)
│   ├── product_matching.py            # 商品匹配模块
│   └── service.py                     # 服务层统一入口
├── ui/                               # Streamlit 前端
│   └── app.py                        # 主应用界面
├── .env                              # 环境变量配置（不提交）
├── .env.example                      # 环境变量模板
├── requirements.txt                   # Python 依赖
├── README.md                         # 项目说明
├── project.md                        # 项目背景文档
└── DEVELOPMENT_GUIDE.md              # 开发指南
```

---

## 技术栈

| 层级 | 技术选择 | 说明 |
|------|----------|------|
| **LLM** | 智谱 GLM-5.1 | 场景理解和推理 |
| **Python** | 3.10+ | 主要开发语言 |
| **前端** | Streamlit | Web 界面 |
| **数据采集** | Requests, BeautifulSoup4 | 热搜抓取 |
| **配置管理** | python-dotenv | 环境变量 |
| **数据存储** | JSON | 模拟数据存储 |

---

## 核心模块说明

### 1. 配置管理 ([src/config.py](src/config.py))
- 管理环境变量（API Key、模型参数）
- 定义数据路径
- 热搜抓取配置（间隔、数量限制）

### 2. 热点采集 ([src/hot_perception.py](src/hot_perception.py))
- **功能**：抓取百度热搜、知乎热榜
- **输出**：清洗后的新闻标题列表（Top 10）
- **缓存**：自动保存到 `data/hot_topics.json`

### 3. 季节性感知 ([src/seasonal_perception.py](src/seasonal_perception.py))
- **功能**：基于时间和节日生成季节性场景
- **数据源**：`data/festivals.json`

### 4. LLM 客户端 ([src/llm_client.py](src/llm_client.py))
- **功能**：封装智谱 GLM-5.1 API 调用
- **关键方法**：`generate_scene()` - 将热点转化为购物场景
- **Prompt策略**：使用 JSON 格式强制约束输出

### 5. 场景挖掘 ([src/scene_mining.py](src/scene_mining.py))
- **功能**：使用 LLM 将非结构化新闻转化为结构化场景
- **输出 Schema**：
  ```json
  {
    "scene_name": "世界杯球迷零食补给站",
    "scene_type": "赛事/热点",
    "trigger_event": "世界杯小组赛开赛",
    "temporal_scope": "2026-06-14 至 2026-07-15",
    "geo_scope": "全国",
    "user_intent": "看球时需要边吃边喝，避免饿肚子影响观赛体验",
    "potential_keywords": ["啤酒", "薯片", "小龙虾", "护肝片", "熬夜能量"],
    "target_population": "男性球迷、聚会人群"
  }
  ```

### 6. 商品匹配 ([src/product_matching.py](src/product_matching.py))
- **功能**：基于场景关键词匹配商品库
- **匹配策略**：
  - 标题完全匹配: 1.0 分
  - 标签匹配: 0.8 分
  - 类别匹配: 0.5 分
- **输出**：按相关性排序的商品列表

### 7. 服务层 ([src/service.py](src/service.py))
- **功能**：统一入口，编排完整业务流程
- **核心方法**：`run_full_pipeline()` - 运行完整管道

---

## 常用命令

### 开发环境启动
```bash
# 进入项目目录
cd /Users/sylve/Desktop/ai_agent/JD

# 激活虚拟环境（如果使用）
source venv/bin/activate  # macOS/Linux

# 启动 Streamlit 应用
streamlit run ui/app.py
```

### 测试单个模块
```bash
# 测试热点采集
python src/hot_perception.py

# 测试季节性感知
python src/seasonal_perception.py

# 测试 LLM 客户端
python src/llm_client.py

# 测试场景挖掘
python src/scene_mining.py

# 测试商品匹配
python src/product_matching.py
```

### Python API 使用
```python
from src.service import get_service

# 获取服务实例
service = get_service()

# 运行完整管道
result = service.run_full_pipeline(hot_limit=10, scene_limit=5)

# 查看结果
print(f"生成了 {result['total_scenes']} 个场景")
```

---

## 环境变量配置

项目使用 `.env` 文件管理环境变量（参考 `.env.example`）：

```bash
# 智谱 AI API Key（必需）
ZHIPU_API_KEY=your_zhipu_api_key_here

# 可选配置
ZHIPU_BASE_URL=https://open.bigmodel.cn/api/anthropic
DEFAULT_MODEL=glm-5.1
TEMPERATURE=0.7
MAX_TOKENS=2000
```

---

## 开发约定

### 代码风格
- 使用 Python 3.10+ 类型注解
- 遵循 PEP 8 规范
- 函数添加 docstring 文档

### 添加新的热点源
在 `src/hot_perception.py` 中添加新方法：
```python
def fetch_new_source_hot(self, limit: int = 10) -> List[Dict]:
    """抓取新的热点源"""
    # 实现抓取逻辑
    pass
```

### 扩展商品库
编辑 `data/mock_products.json`，添加新商品：
```json
{
  "sku_id": "10031",
  "title": "新商品名称",
  "category": "商品类别",
  "tags": ["标签1", "标签2"],
  "price": 99.0,
  "stock": 100,
  "image_url": "/images/product.jpg"
}
```

### 自定义 Prompt
编辑 `src/llm_client.py` 中的 `_build_scene_prompt` 方法。

---

## 项目亮点

1. **AI-Native 思维**：不是"在原系统上加 AI"，而是"用 AI 重构系统"
2. **解决真实痛点**：直击传统电商"反应慢、看不懂新词"的顽疾
3. **全链路闭环**：涵盖数据采集、LLM 推理、业务匹配、前端展示全流程
4. **零人工干预**：从热点爆发到场景生成，全过程自动化

---

## 部署信息

- **本地开发**：`streamlit run ui/app.py`
- **Streamlit Cloud**：可通过 Streamlit Secrets 管理 API Key
- **访问地址**：http://localhost:8501（本地）

---

## 作者信息

- **项目作者**：Grace
- **项目定位**：AI-Native 演示系统，展示 LLM 在电商场景的应用
- **文档版本**：1.0
- **最后更新**：2026-06-14
