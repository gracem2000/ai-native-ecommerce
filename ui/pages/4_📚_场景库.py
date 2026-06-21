"""场景库页（多页应用，含删除/批量删除/编辑弹窗守卫）"""
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

common.init_page("场景库", icon="📚")

# 库弹窗守卫（删除/批量删除/库内编辑），渲染了弹窗则跳过常规库列表
if not common.handle_library_modals():
    common.render_header()
    common.render_scene_library()
