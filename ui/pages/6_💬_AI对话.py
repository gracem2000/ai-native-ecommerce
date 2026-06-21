"""AI 对话：购物助手对话页（多页应用）"""
import sys
import os

_HERE = os.path.dirname(os.path.abspath(__file__))   # ui/pages/
_UI = os.path.dirname(_HERE)                          # ui/
_ROOT = os.path.dirname(_UI)                          # JD/
for _p in (_UI, _ROOT):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import streamlit as st  # noqa: E402
import common           # noqa: E402

common.init_page("AI 购物助手", icon="💬")
common.render_chatbot()
