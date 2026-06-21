# 🎯 场景供给和智能导购 AI 电商演示系统

[![Version](https://img.shields.io/badge/version-1.3.0-blue)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/python-3.10+-green)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-orange)](LICENSE)

> AI-Native 电商演示系统 — 场景智能供给 + 对话式个性化导购，展示 LLM 重构电商链路的完整能力

---

## 📋 项目简介

**🎯 场景供给和智能导购 AI 电商演示系统** — 通过引入智谱 GLM-5.1 大模型，重构传统电商供给链路。将 LLM 作为系统的"感知器官"和"推理大脑"，实现对外部热点的毫秒级响应，自动构建时空场景并完成商品匹配。同时提供面向终端用户的对话式个性化导购体验。

### 核心能力

系统由**两大功能**组成：

**功能一 · 场景供给中心**（后端供给演示）

- **🔥 热点感知**: 自动抓取百度热搜等外部热点信息
- **📅 季节感知**: 基于时间、节日自动生成季节性购物场景
- **🎯 场景挖掘**: LLM 将非结构化的新闻转化为结构化的购物场景
- **🛍️ 商品匹配**: 基于场景关键词自动关联商品库
- **🔄 智能去重**: 基于内容相似度自动过滤重复场景
- **📚 场景管理**: 统一的场景库管理界面

**功能二 · AI 购物助手**（面向用户的前端体验）

- **🤖 对话式导购**: 用户以 Marla / Steve 身份登录，与 AI 助手多轮自然对话
- **🎯 个性化推荐**: 结合用户画像、历史兴趣与当下时节/热点场景，生成带推荐理由的商品推荐
- **🃏 商品卡片**: 推荐结果以品类图标 + 渐变封面的卡片形式呈现

---

## 🏗️ 项目结构

```
.
├── data/
│   ├── mock_products.json          # 模拟商品库 (419 个商品，12+ 品类)
│   ├── hot_topics.json              # 热搜数据缓存（运行时更新）
│   ├── scenarios.json               # 场景库 (74 条结构化场景)
│   ├── festivals.json               # 节日数据 (40 个事件，农历已转阳历)
│   └── user_profiles.json           # 虚拟用户画像 (Marla / Steve)
├── src/
│   ├── __init__.py
│   ├── config.py                    # 配置管理
│   ├── hot_perception.py            # 热点采集模块（百度热搜）
│   ├── seasonal_perception.py       # 时节感知模块（节日+节气+农历转阳历）
│   ├── llm_client.py                # GLM-5.1 客户端（场景生成 + 通用多轮对话）
│   ├── scene_mining.py              # 场景挖掘（LLM 核心 + 智能去重 + 文本清洗）
│   ├── product_matching.py          # 商品匹配（关键词多维打分）
│   ├── recommender.py               # 个性化推荐引擎（对话式导购 + 场景化推荐）
│   └── service.py                   # 服务层统一入口（含政治内容过滤）
├── ui/                               # Streamlit 多页应用
│   ├── __init__.py
│   ├── app.py                       # 入口（首页）
│   ├── common.py                    # 共享模块（渲染函数 + 导航 + 初始化）
│   ├── style.css                    # 全局样式
│   └── pages/                       # 6 个独立页面
│       ├── 1_📅_时节场景.py
│       ├── 2_🔥_热点追踪.py
│       ├── 3_✍️_人工提报.py
│       ├── 4_📚_场景库.py
│       ├── 5_🤖_AI推荐.py
│       └── 6_💬_AI对话.py
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
| `MIN_CONFIDENCE` | 商品匹配最低置信度 | `0.2` |

### 热搜配置

- **百度热搜**: 自动抓取 Top 10
- **政治过滤**: 自动跳过敏感热点，避免触发 LLM 安全拦截
- **抓取间隔**: 30 分钟（可在代码中调整）

---

## 📖 使用指南

### 界面功能

应用首页分为三大区块（从上到下）：**三大场景来源**、**AI 场景导购**、**核心能力**，对应系统的两大功能。

**功能一 · 场景供给中心**

- **📅 时节场景** - 基于传统节日、二十四节气自动生成周期性购物场景（支持多场景生成）
- **🔥 热点追踪** - 实时抓取百度热搜，LLM 自动转化为购物场景（自动保存）
- **✍️ 人工提报** - 手动提报场景主题，系统自动生成多个场景（如端午送礼、端午出游等）
- **📚 场景库管理** - 统一管理所有场景，支持编辑、删除、筛选

**功能二 · AI 购物助手**（AI 场景导购入口 → 登录后进入对话页）

- 以 **Marla** 或 **Steve** 身份登录，进入专属对话界面
- 与 AI 购物助手多轮自然对话，侧栏展示当前用户画像与"本次推荐参考的场景"
- 系统结合用户画像、历史兴趣与当下时节/热点场景，给出带**推荐理由**的个性化商品推荐
- 推荐结果以品类图标 + 渐变封面的商品卡片形式呈现，支持切换用户与清空对话

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

# 功能二：AI 购物助手（对话式个性化推荐）
recommender = service.get_recommender()
result = recommender.chat(
    user_id="marla",
    history=[{"role": "user", "content": "周末想出游，推荐点东西"}],
)
print(result["reply"])              # 助手回复
for r in result["recommendations"]: # 带理由的推荐商品
    print(r["product"]["title"], "->", r["reason"])
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
- 商品库：419 个示例商品，覆盖 12+ 个品类

### 5. 个性化推荐引擎 (Recommender) —— 功能二核心

- **对话式导购**：基于 LLM 多轮对话，复用 `GLMClient.chat()` 通用对话能力
- **上下文组装**：融合用户画像（基础/偏好/兴趣/历史购买）+ 当前活跃时节/热点场景 + 按偏好品类过滤的候选商品库
- **约束选品**：LLM 只能从候选商品库的 `sku_id` 中推荐，并通过 `get_product_by_sku` 还原完整商品，杜绝幻觉商品
- **推荐理由**：每件推荐商品都附带结合画像兴趣与当下场景的理由
- 数据来源：`data/user_profiles.json`（Marla / Steve 两位虚拟用户）

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

---

**项目作者**：Grace | **定位**：AI-Native 电商演示系统 | **开发方式**：Vibe Coding（Claude Code） | **版本**：1.3.0

---

**Contact**: For questions or feedback, please open an issue on GitHub.
