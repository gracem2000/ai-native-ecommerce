"""
时空场景自动供给系统 - 多页应用入口（首页）

运行：streamlit run ui/app.py
架构：Streamlit 原生多页（pages/）+ st.switch_page；共享逻辑见 ui/common.py
"""
import sys
import os

# 让 ui/ 与项目根可被 import（common / src）
_HERE = os.path.dirname(os.path.abspath(__file__))              # ui/
_ROOT = os.path.dirname(_HERE)                                   # JD/
for _p in (_HERE, _ROOT):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import common  # noqa: E402

# 首页：页面配置 + 样式 + 侧边栏，然后渲染首页内容
common.init_page("首页", icon="🏠")
common.render_homepage()
