# ⚡ 时空场景自动供给系统

[![Version](https://img.shields.io/badge/version-1.1.0-blue)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/python-3.10+-green)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-orange)](LICENSE)

> 基于 LLM 的电商场景智能供给系统，展示从"热点感知"到"交易闭环"的 AI-Native 能力

---

## 📋 项目简介

本项目是一个 AI-Native 演示系统，通过引入智谱 GLM 大模型，重构传统电商供给链路。将 LLM 作为系统的"感知器官"和"推理大脑"，实现对外部热点的毫秒级响应，自动构建时空场景并完成商品匹配。

### 核心能力

- **🔥 热点感知**: 自动抓取百度热搜等外部热点信息
- **📅 季节感知**: 基于时间、节日自动生成季节性购物场景
- **🎯 场景挖掘**: LLM 将非结构化的新闻转化为结构化的购物场景
- **🛍️ 商品匹配**: 基于场景关键词自动关联商品库
- **🔄 智能去重**: 基于内容相似度自动过滤重复场景
- **📚 场景管理**: 统一的场景库管理界面

---

## 🏗️ 项目结构

```
.
├── data/
│   ├── mock_products.json          # 模拟商品库
│   ├── hot_topics.json              # 热搜数据缓存
│   ├── scenarios.json               # 生成的场景数据
│   └── festivals.json               # 节日数据
├── src/
│   ├── __init__.py
│   ├── config.py                    # 配置管理
│   ├── hot_perception.py            # 热点采集模块
│   ├── seasonal_perception.py       # 季节性感知模块
│   ├── llm_client.py                # GLM-5.1 客户端封装
│   ├── scene_mining.py              # 场景挖掘模块
│   ├── product_matching.py          # 商品匹配模块
│   └── service.py                   # 服务层统一入口
├── ui/
│   ├── __init__.py
│   └── app.py                       # Streamlit 前端应用
├── requirements.txt
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

   创建 `.env` 文件，填入你的 API Key:
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
| `DEFAULT_MODEL` | 使用的模型 | `glm-5.1` |
| `TEMPERATURE` | LLM 温度参数 | `0.7` |
| `MAX_TOKENS` | LLM 最大 Token 数 | `2000` |

### 热搜配置

- **百度热搜**: 自动抓取 Top 10
- **抓取间隔**: 30 分钟（可在代码中调整）

---

## 📖 使用指南

### 界面功能

应用首页展示三大场景来源入口：

- **📅 时节场景** - 基于传统节日、二十四节气自动生成周期性购物场景（支持多场景生成）
- **🔥 热点追踪** - 实时抓取百度热搜，LLM 自动转化为购物场景（自动保存）
- **✍️ 人工提报** - 手动提报场景主题，系统自动生成多个场景（如端午送礼、端午出游等）
- **📚 场景库管理** - 统一管理所有场景，支持编辑、删除、筛选

### 时节场景

- 选择日期范围和每个节日生成场景数（1-15个）
- 系统为每个节日/节气生成多个不同角度的购物场景
- 例如：端午节可生成 → 端午送礼、端午出游、自制粽子、端午祈福等多个场景
- 智能去重后自动保存，可直接在场景库管理中编辑

### 热点追踪

- 设置热点数量和生成场景数量
- 点击"开始抓取"自动：
  1. 抓取百度实时热搜
  2. LLM 生成购物场景
  3. 匹配相关商品
  4. 智能去重后自动保存
- 显示生成结果：新增场景数、跳过重复数

### 人工提报

- 输入场景主题（如"端午节"、"春节"）
- 勾选"生成多个场景"并设置数量（3-15个）
- 系统自动生成多个不同角度的场景并保存
- 例如：输入"世界杯"可生成 → 观赛零食、球队周边、聚会用品等场景

### 场景库管理

统一管理所有场景，支持：
- 按来源筛选（时节/热点/人工）
- 关键词搜索
- 多种排序方式
- 编辑、复制、删除操作

### Python API 使用

```python
from src.service import get_service

# 获取服务实例
service = get_service()

# 生成时节场景（每个事件生成多个场景）
result = service.generate_seasonal_scenes(auto_save=True, scenes_per_event=5)
print(f"新增: {result['saved']}, 跳过: {result['skipped']}")

# 运行热点追踪管道（自动保存）
result = service.run_full_pipeline_with_progress(
    hot_limit=10,
    scene_limit=5,
    auto_save=True
)

# 人工提报场景（生成多个场景）
result = service.submit_scene(
    scene_name="端午节",
    generate_multiple=True,
    scene_count=5
)

# 批量保存场景
save_result = service.save_scenes_batch(scenes)

# 获取统计数据
source_stats = service.get_source_statistics()
seasonal_stats = service.get_seasonal_statistics()
```

---

## 🎯 核心功能说明

### 1. 热点采集 (HotPerception)

- 支持平台：百度热搜
- 数据清洗：去除重复、格式化热度值
- 数据缓存：自动保存到 `data/hot_topics.json`

### 2. 季节感知 (SeasonalPerception)

- 基于当前时间、季节自动生成场景
- 支持节日场景（春节、国庆、中秋等）
- 数据来源：`data/festivals.json`

### 3. 场景挖掘 (SceneMining)

- **多场景生成**: 一个主题可生成多个不同角度的场景
- **智能去重**: 基于内容相似度自动过滤重复场景
  - 场景名称相似度（75%）
  - 触发事件相似度（75%）
  - 关键词重叠度（60%）
  - 时间窗口判断（24小时内）
- **LLM 驱动**: 使用 GLM-5.1 理解热点并生成场景
- **结构化输出**: 场景名称、类型、时间范围、关键词等
- **数据持久化**: 自动保存到 `data/scenarios.json`

### 4. 商品匹配 (ProductMatching)

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

## 📋 更新日志

查看 [CHANGELOG.md](CHANGELOG.md) 了解版本更新历史。

---

## 🙏 致谢

- [智谱 AI](https://open.bigmodel.cn/) - 提供 GLM-5.1 API
- [Streamlit](https://streamlit.io/) - 前端框架
- [Anthropic](https://www.anthropic.com/) - Claude API SDK

---

**Contact**: For questions or feedback, please open an issue on GitHub.
