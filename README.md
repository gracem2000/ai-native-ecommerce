# ⚡ 时空场景自动供给系统

> 基于 LLM 的电商场景智能供给系统，展示从"热点感知"到"交易闭环"的 AI-Native 能力

---

## 📋 项目简介

本项目是一个 AI-Native 演示系统，通过引入 GLM 大模型，重构传统电商供给链路。将 LLM 作为系统的"感知器官"和"推理大脑"，实现对外部热点的毫秒级响应，自动构建时空场景并完成商品匹配。

### 核心能力

- **🔥 热点感知**: 自动抓取百度热搜、知乎热榜等外部热点信息
- **🎯 场景挖掘**: LLM 将非结构化的新闻转化为结构化的购物场景
- **🛍️ 商品匹配**: 基于场景关键词自动关联商品库

---

## 🏗️ 项目结构

```
.
├── data/
│   └── mock_products.json          # 模拟商品库
├── src/
│   ├── __init__.py
│   ├── config.py                    # 配置管理
│   ├── hot_perception.py            # 热点采集模块
│   ├── llm_client.py                # GLM-4 客户端封装
│   ├── scene_mining.py              # 场景挖掘模块
│   ├── product_matching.py          # 商品匹配模块
│   └── service.py                   # 服务层统一入口
├── ui/
│   ├── __init__.py
│   └── app.py                       # Streamlit 前端应用
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🚀 快速开始

### 环境要求

- Python 3.10+
- pip

### 安装步骤

1. **克隆项目**
   ```bash
   cd /path/to/project
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   # 或
   venv\Scripts\activate     # Windows
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **配置环境变量**
   ```bash
   cp .env.example .env
   ```

   编辑 `.env` 文件，填入你的 API Key:
   ```
   ZHIPU_API_KEY=your_zhipu_api_key_here
   ```

5. **运行应用**
   ```bash
   streamlit run ui/app.py
   ```

   应用将在浏览器中打开：http://localhost:8501

---

## ⚙️ 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `ZHIPU_API_KEY` | 智谱 AI API Key（必需） | - |
| `ZHIPU_BASE_URL` | 智谱 API 地址 | `https://open.bigmodel.cn/api/anthropic` |
| `DEFAULT_MODEL` | 使用的模型 | `glm-4` |
| `TEMPERATURE` | LLM 温度参数 | `0.7` |
| `MAX_TOKENS` | LLM 最大 Token 数 | `2000` |

### 热搜配置

- **百度热搜**: 自动抓取 Top 10
- **知乎热榜**: 自动抓取 Top 10
- **抓取间隔**: 30 分钟（可在代码中调整）

---

## 📖 使用指南

### 方式 1: 使用 Web 界面

1. 启动应用后，在侧边栏点击 **"🔄 运行完整管道"**
2. 系统将自动：
   - 抓取最新热点信息
   - 使用 LLM 生成购物场景
   - 匹配相关商品
3. 在三个标签页中查看结果：
   - **🔥 热点监控**: 查看抓取的热搜榜单
   - **🎯 场景挖掘**: 查看 AI 生成的购物场景
   - **🛍️ 商品匹配**: 查看匹配的商品推荐

### 方式 2: 使用 Python API

```python
from src.service import get_service

# 获取服务实例
service = get_service()

# 运行完整管道
result = service.run_full_pipeline(hot_limit=10, scene_limit=5)

# 查看结果
print(f"生成了 {result['total_scenes']} 个场景")
for scene in result['scenes']:
    print(f"- {scene['scene_name']}")
    print(f"  关键词: {', '.join(scene['potential_keywords'])}")
```

### 方式 3: 单独测试各模块

```bash
# 测试热点采集
python src/hot_perception.py

# 测试 LLM 客户端
python src/llm_client.py

# 测试场景挖掘
python src/scene_mining.py

# 测试商品匹配
python src/product_matching.py
```

---

## 🎯 核心功能说明

### 1. 热点采集 (HotPerception)

- 支持平台：百度热搜、知乎热榜
- 数据清洗：去除重复、格式化热度值
- 数据缓存：自动保存到 `data/hot_topics.json`

### 2. 场景挖掘 (SceneMining)

- LLM 驱动：使用 GLM-4 理解热点并生成场景
- 结构化输出：场景名称、类型、时间范围、关键词等
- 数据持久化：自动保存到 `data/scenarios.json`

### 3. 商品匹配 (ProductMatching)

- 多维度匹配：标题、标签、类别
- 相关性排序：按匹配度排序返回结果
- 商品库：30 个示例商品，覆盖多个品类

---

## 🛠️ 开发指南

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

## 📊 数据示例

### 场景数据示例

```json
{
  "scene_id": "scene_20260614_120000",
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

---

## ❓ 常见问题

**Q: LLM 调用失败怎么办？**
A: 检查 `ZHIPU_API_KEY` 是否正确配置，并确保账户有足够的 API 额度。

**Q: 热点抓取失败？**
A: 某些平台可能更新了页面结构，需要更新 CSS 选择器。

**Q: 商品匹配不准确？**
A: 可以优化商品标签，或调整 `product_matching.py` 中的相关性算法。

**Q: 如何定时运行？**
A: 可以使用 APScheduler 或系统 cron 任务定时调用服务。

---

## 🔒 安全说明

- **API Key**: 请勿将 `.env` 文件提交到版本控制
- **数据缓存**: 缓存文件包含敏感信息，注意权限控制
- **部署**: 使用 Streamlit Cloud 部署时，使用 Secrets 管理 API Key

---

## 📝 License

MIT License

---

## 🙏 致谢

- [智谱 AI](https://open.bigmodel.cn/) - 提供 GLM-4 API
- [Streamlit](https://streamlit.io/) - 前端框架
- [Anthropic](https://www.anthropic.com/) - Claude API SDK

---

**Contact**: For questions or feedback, please open an issue on GitHub.
