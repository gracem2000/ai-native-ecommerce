"""人工提报表（多页应用，含编辑模式守卫）"""
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

common.init_page("人工提报", icon="✍️")

# 编辑模式守卫（原 main() 内逻辑）：进入人工提报编辑/复制场景
if st.session_state.get('show_edit_mode') and st.session_state.get('pending_scene'):
    common.render_header()
    common.render_scene_editor(st.session_state.pending_scene)
else:
    common.render_header()
    common.render_manual_scenes()
