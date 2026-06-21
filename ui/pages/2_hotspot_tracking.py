"""热点追踪页（多页应用）"""
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

common.init_page("热点追踪", icon="🔥")
common.render_header()
common.render_hotspot_scenes()
