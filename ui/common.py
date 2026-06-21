"""
时空场景自动供给系统 - Streamlit 前端应用
参考智谱AI开放平台设计风格
"""
import streamlit as st
import sys
import os
import json
from datetime import datetime
from typing import Dict

# 添加项目根目录到路径（供 from src... 的惰性导入）
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 加载外部CSS样式（所有样式统一在 style.css，含红框/BaseWeb 选择框规则）
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "style.css")
    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except:
        # 如果CSS文件不存在，使用内联样式
        pass


def bootstrap_paths():
    """页面文件(ui/pages/*.py)与入口调用：把 ui/ 与项目根加入 sys.path，便于 import common / src"""
    _here = os.path.dirname(os.path.abspath(__file__))          # ui/
    _root = os.path.dirname(_here)                               # JD/
    for _p in (_here, _root):
        if _p not in sys.path:
            sys.path.insert(0, _p)


def init_page(title, icon="🎯"):
    """每个页面脚本的第一个 st 调用：页面配置 + 样式 + 侧边栏(品牌头+系统状态)"""
    st.set_page_config(
        page_title=title,
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    load_css()
    render_sidebar()


def normalize_keywords(keywords) -> list:
    """统一处理关键词格式，支持列表或逗号分隔的字符串

    Args:
        keywords: 列表格式 ["投影仪", "球衣"] 或字符串格式 "投影仪,球衣"

    Returns:
        清理后的关键词列表
    """
    if isinstance(keywords, str):
        keywords = [k.strip() for k in keywords.split(',') if k.strip()]
    # 去除关键词中的空格
    return [k.replace(' ', '') for k in keywords if k]


@st.cache_resource
def get_service():
    """获取服务实例（缓存）"""
    from src.service import get_service
    return get_service()


def render_homepage():
    """渲染高端首页展示"""
    service = get_service()

    # 获取统计数据
    source_stats = service.get_source_statistics()
    seasonal_stats = service.get_seasonal_statistics()
    health = service.health_check()
    product_count = health['details']['products_loaded']
    total_scenes = source_stats['seasonal']['count'] + source_stats['hotspot']['count'] + source_stats['manual']['count']

    # 主标题区域 - 紧凑设计
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0 1.5rem 0;">
        <h1 style="font-size: 1.5rem; margin-bottom: 0.5rem; color: #1f2937; font-weight: 600;">电商场景智能供给与智能导购系统</h1>
        <p style="font-size: 0.95rem; color: #6b7280; max-width: 500px; margin: 0 auto; line-height: 1.5;">
            将 LLM 作为"感知大脑"，自动完成从场景识别到商品推荐的智能闭环
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 统计数据卡片 - 紧凑设计
    st.markdown(f'''
    <div style="
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem auto 2rem auto;
        max-width: 900px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    ">
        <div style="display: flex; justify-content: space-around; text-align: center;">
            <div>
                <div style="font-size: 0.75rem; color: #6b7280;">场景总数</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #1f2937;">{total_scenes}</div>
            </div>
            <div style="width: 1px; background: #e5e7eb;"></div>
            <div>
                <div style="font-size: 0.75rem; color: #6b7280;">时节场景</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #1f2937;">{source_stats['seasonal']['count']}</div>
            </div>
            <div style="width: 1px; background: #e5e7eb;"></div>
            <div>
                <div style="font-size: 0.75rem; color: #6b7280;">热点场景</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #1f2937;">{source_stats['hotspot']['count']}</div>
            </div>
            <div style="width: 1px; background: #e5e7eb;"></div>
            <div>
                <div style="font-size: 0.75rem; color: #6b7280;">人工提报</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #1f2937;">{source_stats['manual']['count']}</div>
            </div>
            <div style="width: 1px; background: #e5e7eb;"></div>
            <div>
                <div style="font-size: 0.75rem; color: #6b7280;">商品库</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #1f2937;">{product_count}</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('<h2 style="text-align: center; margin: 1rem 0 1.5rem 0; font-size: 1.5rem;">智能场景供给</h2>', unsafe_allow_html=True)

    # 三大来源入口卡片 - 现代化设计（恢复 master 版本）
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f'''
        <div class="hero-card">
            <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">📅</div>
            <h3 style="color: #1f2937; margin: 0 0 0.5rem 0; font-size: 1.3rem;">时节场景</h3>
            <p style="color: #6b7280; margin: 0 0 1rem 0; font-size: 0.85rem;">
                基于传统节日、二十四节气<br/>
                自动生成周期性购物场景
            </p>
            <div style="display: flex; gap: 1rem; font-size: 0.75rem; color: #6b7280; margin-bottom: 1rem;">
                <span>📊 {seasonal_stats['total_festivals']} 个节日</span>
                <span>📊 {seasonal_stats['total_solar_terms']} 个节气</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        if st.button("→ 进入时节场景", key="seasonal_entry", use_container_width=True):
            st.switch_page("pages/1_seasonal_scenes.py")

    with col2:
        st.markdown(f'''
        <div class="hero-card">
            <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">🔥</div>
            <h3 style="color: #1f2937; margin: 0 0 0.5rem 0; font-size: 1.3rem;">热点追踪</h3>
            <p style="color: #6b7280; margin: 0 0 1rem 0; font-size: 0.85rem;">
                定期抓取热搜事件<br/>
                LLM 自动转化为购物场景
            </p>
            <div style="display: flex; gap: 1rem; font-size: 0.75rem; color: #6b7280; margin-bottom: 1rem;">
                <span>🔄 小时级别更新</span>
                <span>🤖 AI智能理解</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        if st.button("→ 进入热点追踪", key="hotspot_entry", use_container_width=True):
            st.switch_page("pages/2_hotspot_tracking.py")

    with col3:
        st.markdown(f'''
        <div class="hero-card">
            <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">✍️</div>
            <h3 style="color: #1f2937; margin: 0 0 0.5rem 0; font-size: 1.3rem;">人工提报</h3>
            <p style="color: #6b7280; margin: 0 0 1rem 0; font-size: 0.85rem;">
                运营人员手动提报场景<br/>
                系统自动补全完整信息
            </p>
            <div style="display: flex; gap: 1rem; font-size: 0.75rem; color: #6b7280; margin-bottom: 1rem;">
                <span>📝 灵活提报</span>
                <span>🤖 智能补全</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        if st.button("→ 进入人工提报", key="manual_entry", use_container_width=True):
            st.switch_page("pages/3_manual_submit.py")

    st.markdown('<div style="height: 1px; background: linear-gradient(90deg, transparent, #e5e7eb, transparent); margin: 2rem 0;"></div>', unsafe_allow_html=True)

    # ===== AI 场景导购（功能二：AI 购物助手）=====
    st.markdown('<h2 style="text-align: center; margin: 1rem 0 1.5rem 0; font-size: 1.5rem;">智能导购</h2>', unsafe_allow_html=True)

    # 左右两列等大对齐：左 = AI推荐，右 = AI对话
    ai_col1, ai_col2 = st.columns(2)

    with ai_col1:
        st.markdown('''
        <div class="hero-card" style="text-align:left; min-height: 15rem;">
            <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">🤖</div>
            <h3 style="color: #1f2937; margin: 0 0 0.5rem 0; font-size: 1.3rem;">AI推荐</h3>
            <p style="color: #6b7280; margin: 0 0 1rem 0; font-size: 0.88rem; line-height: 1.6;">
                系统融合你的<b>用户画像</b>与当下热门的<b>时节</b>、<b>热点场景</b>，由大模型实时推理，为你智能生成千人千面的个性化商品推荐列表——让每一次推荐都精准契合你的真实需求与当下时机。
            </p>
        </div>
        ''', unsafe_allow_html=True)
        if st.button("→ 开始AI推荐", key="home_ai_recommend", type="primary", use_container_width=True):
            st.switch_page("pages/5_ai_recommend.py")

    with ai_col2:
        st.markdown('''
        <div class="hero-card" style="text-align:left; min-height: 15rem;">
            <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">💬</div>
            <h3 style="color: #1f2937; margin: 0 0 0.5rem 0; font-size: 1.3rem;">AI对话</h3>
            <p style="color: #6b7280; margin: 0 0 1rem 0; font-size: 0.88rem; line-height: 1.6;">
                像和朋友聊天一样，与 AI 购物助手进行多轮自然语言对话。无论是寻找购物灵感、咨询好物还是解答疑问，它都能像懂你的朋友一样，给出贴心、专业的建议。
            </p>
        </div>
        ''', unsafe_allow_html=True)
        if st.button("→ 开始AI对话", key="home_ai_chat", type="primary", use_container_width=True):
            st.switch_page("pages/6_ai_chat.py")

    st.markdown('<div style="height: 1px; background: linear-gradient(90deg, transparent, #e5e7eb, transparent); margin: 2rem 0;"></div>', unsafe_allow_html=True)

    # 系统特性 - 现代化卡片设计
    st.markdown('<h2 style="text-align: center; margin: 2rem 0; font-size: 1.5rem;">核心能力</h2>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('''
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <h4 style="color: #1f2937; margin: 0.5rem 0; font-size: 1.3rem;">实时数据更新</h4>
            <p style="color: #6b7280; font-size: 0.875rem; margin: 0;">热点数据实时抓取和更新</p>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        st.markdown('''
        <div class="feature-card">
            <div class="feature-icon">🧠</div>
            <h4 style="color: #1f2937; margin: 0.5rem 0; font-size: 1.3rem;">智能场景生成</h4>
            <p style="color: #6b7280; font-size: 0.875rem; margin: 0;">基于 LLM 的场景理解和生成</p>
        </div>
        ''', unsafe_allow_html=True)

    with col3:
        st.markdown('''
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <h4 style="color: #1f2937; margin: 0.5rem 0; font-size: 1.3rem;">精准商品匹配</h4>
            <p style="color: #6b7280; font-size: 0.875rem; margin: 0;">场景驱动的智能商品推荐</p>
        </div>
        ''', unsafe_allow_html=True)

    # 底部技术信息
    st.markdown('<div style="height: 1px; background: linear-gradient(90deg, transparent, #e5e7eb, transparent); margin: 2rem 0;"></div>', unsafe_allow_html=True)

    st.markdown('''
    <div style="text-align: center; padding: 1rem 0;">
        <p style="color: #9ca3af; font-size: 0.875rem;">
            Powered by <span style="font-weight: 600; color: #3b82f6;">智谱 GLM-5.1</span> · 场景供给和智能导购演示系统
        </p>
    </div>
    ''', unsafe_allow_html=True)


def render_header():
    """渲染页面标题（用于非首页）"""
    st.markdown('''
    <div style="text-align: center; padding: 0 0 0.5rem 0;">
        <h1 style="
            font-size: 1.8rem;
            font-weight: 700;
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
        ">AI场景供给系统</h1>
    </div>
    ''', unsafe_allow_html=True)


def render_sidebar():
    """渲染侧边栏 - 现代化导航设计"""
    with st.sidebar:
        # 品牌区域
        st.markdown('''
        <div style="
            background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
            padding: 1.5rem;
            border-radius: 12px;
            margin: 2rem -1rem 1.5rem -1rem;
            color: white;
        ">
            <div style="font-size: 1.5rem; font-weight: 700; display: flex; align-items: center; gap: 0.5rem;">
                <span>🎯</span>
                <span>场景供给和智能导购</span>
            </div>
            <div style="font-size: 0.8rem; opacity: 0.8; margin-top: 0.5rem;">
                AI 电商演示系统
            </div>
        </div>
        ''', unsafe_allow_html=True)

        # ===== 自定义导航（软件层映射，替代 Streamlit 自动多页列表） =====
        st.markdown('<div style="color: #6b7280; font-size: 0.75rem; font-weight: 600; margin: 0.5rem 0 0.5rem 0; text-transform: uppercase;">导航</div>', unsafe_allow_html=True)

        if st.button("🏠 首页", use_container_width=True, key="custom_nav_home"):
            st.switch_page("app.py")

        st.markdown('<div style="color: #6b7280; font-size: 0.75rem; font-weight: 600; margin: 0.75rem 0 0.4rem 0; text-transform: uppercase;">智能场景供给</div>', unsafe_allow_html=True)

        if st.button("📅 时节场景", use_container_width=True, key="custom_nav_seasonal"):
            st.switch_page("pages/1_seasonal_scenes.py")
        if st.button("🔥 热点追踪", use_container_width=True, key="custom_nav_hotspot"):
            st.switch_page("pages/2_hotspot_tracking.py")
        if st.button("✍️ 人工提报", use_container_width=True, key="custom_nav_manual"):
            st.switch_page("pages/3_manual_submit.py")
        if st.button("📚 场景库管理", use_container_width=True, key="custom_nav_library"):
            st.switch_page("pages/4_scene_library.py")

        st.markdown('<div style="color: #6b7280; font-size: 0.75rem; font-weight: 600; margin: 0.75rem 0 0.4rem 0; text-transform: uppercase;">智能导购</div>', unsafe_allow_html=True)

        if st.button("🤖 AI推荐", use_container_width=True, key="custom_nav_ai_rec"):
            st.switch_page("pages/5_ai_recommend.py")
        if st.button("💬 AI对话", use_container_width=True, key="custom_nav_ai_chat"):
            st.switch_page("pages/6_ai_chat.py")

        st.markdown("---")

        # 系统状态
        st.markdown('<div style="color: #6b7280; font-size: 0.75rem; font-weight: 600; margin-bottom: 0.5rem; text-transform: uppercase;">系统状态</div>', unsafe_allow_html=True)

        try:
            service = get_service()
            health = service.health_check()

            # 状态指示器
            status_color = "#10b981" if health['healthy'] else "#f59e0b"
            status_text = "正常运行" if health['healthy'] else "部分异常"
            st.markdown(f'''
            <div style="
                display: flex;
                align-items: center;
                gap: 0.5rem;
                padding: 0.75rem;
                background: {"#d1fae5" if health['healthy'] else "#fef3c7"};
                border-radius: 8px;
                margin-bottom: 0.5rem;
            ">
                <span style="
                    width: 8px;
                    height: 8px;
                    background: {status_color};
                    border-radius: 50%;
                    animation: pulse 2s infinite;
                "></span>
                <span style="font-size: 0.875rem; font-weight: 500;">{status_text}</span>
            </div>
            ''', unsafe_allow_html=True)

            # 统计卡片
            st.markdown(f'''
            <div style="
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 0.75rem;
                margin: 0.25rem 0;
            ">
                <div style="font-size: 0.75rem; color: #6b7280;">商品库</div>
                <div style="font-size: 1.25rem; font-weight: 600; color: #1f2937;">{health['details']['products_loaded']} 个</div>
            </div>
            <div style="
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 0.75rem;
                margin: 0.25rem 0;
            ">
                <div style="font-size: 0.75rem; color: #6b7280;">LLM模型</div>
                <div style="font-size: 0.875rem; font-weight: 600; color: #1f2937;">{health['details']['llm_model']}</div>
            </div>
            ''', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ 系统异常: {e}")

        # 底部信息
        st.markdown("---")
        st.markdown('''
        <div style="
            text-align: center;
            font-size: 0.75rem;
            color: #9ca3af;
            padding: 1rem 0;
        ">
            Powered by<br/>
            <span style="font-weight: 600;">智谱 GLM-5.1</span>
        </div>
        ''', unsafe_allow_html=True)


def run_pipeline(hot_limit: int, scene_limit: int):
    """运行完整管道（带详细进度展示，自动保存场景）"""
    try:
        service = get_service()

        # 创建进度展示区域
        progress_area = st.empty()
        detail_area = st.empty()
        scene_area = st.empty()

        results = {'hot_topics': {}, 'scenes': [], 'summary': {}}

        # 使用列表存储详细的处理日志
        progress_logs = []
        current_step = ""
        current_step_num = 0
        total_steps = 4

        def render_progress():
            """渲染进度信息（终端风格日志面板 + 胶囊状态标签）"""
            with progress_area.container():
                # 当前步骤用细长胶囊标签（替代原来占面积的 st.info 大蓝框）
                if current_step:
                    st.markdown(
                        f'<div class="log-status">{current_step}</div>',
                        unsafe_allow_html=True,
                    )

                if progress_logs:
                    # 开日志面板
                    lines_html = ""
                    for log in progress_logs[-15:]:
                        # 按前缀分级、剥离 markdown 标记，交给 CSS 上色 + 缩进
                        cls = "log-line"
                        if log.startswith("###"):
                            cls = "log-heading"
                            log = log[4:]
                        elif log.startswith("📌"):
                            cls = "log-step"
                        elif log.startswith("✅"):
                            cls = "log-success"
                        elif log.startswith("❌") or log.startswith("⚠️"):
                            cls = "log-error"
                        elif log.startswith("🤖"):
                            cls = "log-llm"
                        elif log.startswith("   ") or log.startswith("    "):
                            cls = "log-detail"
                        # 清理残留的 markdown 加粗标记
                        log = log.replace("**", "")
                        lines_html += f'<div class="{cls}">{log}</div>'

                    st.markdown(
                        f'<div class="log-panel">{lines_html}</div>',
                        unsafe_allow_html=True,
                    )

        def handle_progress(event_type, *args):
            """处理进度回调"""
            nonlocal current_step, current_step_num

            if event_type == 'step':
                step_num, total, message = args
                current_step_num = step_num
                current_step = message
                progress_logs.append(f"### {message}")
                render_progress()

            elif event_type == 'info':
                message = args[0]
                progress_logs.append(f"📋 {message}")
                render_progress()

            elif event_type == 'baidu_result':
                count = args[0]
                progress_logs.append(f"✅ **百度热搜**: 抓取 {count} 条")
                render_progress()

            elif event_type == 'total_hot':
                count = args[0]
                progress_logs.append(f"📊 **共抓取**: {count} 条热点信息")
                progress_logs.append("---")
                render_progress()

            elif event_type == 'processing':
                idx, total, topic = args
                progress_logs.append(f"📌 **[{idx}/{total}]** 处理: {topic}")
                render_progress()

            elif event_type == 'llm_start':
                topic = args[0]
                progress_logs.append(f"🤖 正在处理热点: {topic[:40]}...")
                render_progress()

            elif event_type == 'scene_generated':
                scene, message = args
                progress_logs.append(f"   ✅ {message}")

                # 在场景区域展示生成的场景
                with scene_area.container():
                    st.markdown(f"### ✅ {scene.get('scene_name')}")
                    st.caption(f"类型: {scene.get('scene_type', '未知')}")
                    st.caption(f"时间: {scene.get('temporal_scope', '未知')}")
                    st.caption(f"地理: {scene.get('geo_scope', '未知')}")
                    st.write(f"**用户意图**: {scene.get('user_intent', '暂无')[:100]}...")
                    keywords = normalize_keywords(scene.get('potential_keywords', []))
                    if keywords:
                        st.write("**关键词**:", ", ".join(keywords[:5]))

                render_progress()

            elif event_type == 'scene_failed':
                topic, message = args
                progress_logs.append(f"   ⚠️ {message}")
                render_progress()

            elif event_type == 'matching_start':
                scene_name, keyword_count = args
                progress_logs.append(f"   [{scene_name}] 匹配商品 (关键词: {keyword_count} 个)")
                render_progress()

            elif event_type == 'matching_done':
                scene_name, matched_count = args
                progress_logs.append(f"   ✅ 匹配到 {matched_count} 个商品")
                render_progress()

            elif event_type == 'complete':
                message = args[0]
                progress_logs.append(f"### {message}")
                progress_logs.append("---")
                render_progress()

            elif event_type == 'error':
                message = args[0]
                progress_logs.append(f"❌ **错误**: {message}")
                render_progress()

        # 执行带进度的管道（自动保存）
        results = service.run_full_pipeline_with_progress(
            hot_limit=hot_limit,
            scene_limit=scene_limit,
            progress_callback=handle_progress,
            auto_save=True  # 自动保存场景
        )

        # 清空展示区域
        progress_area.empty()
        scene_area.empty()

        # 显示最终摘要
        saved = results.get('saved', 0)
        skipped = results.get('skipped', 0)
        skipped_scenes = results.get('skipped_scenes', [])

        st.success(f"✅ 处理完成! 新增 {saved} 个场景，跳过 {skipped} 个重复场景")

        # 显示去重详情
        if skipped_scenes:
            with st.expander(f"🔍 查看跳过的重复场景 ({len(skipped_scenes)}个)", expanded=False):
                for skipped in skipped_scenes:
                    st.markdown(f"**{skipped['scene_name']}**")
                    st.caption(f"与「{skipped['duplicate_of']}」重复: {skipped['reason']}")

        # 显示新增场景列表
        if saved > 0:
            with st.expander(f"📋 查看新增的场景 ({saved}个)", expanded=True):
                for scene in results.get('scenes', []):
                    # 检查场景是否被保存（通过检查是否在skipped_scenes中）
                    is_saved = not any(s['scene_name'] == scene['scene_name'] for s in skipped_scenes)
                    if is_saved:
                        st.markdown(f"**📌 {scene.get('scene_name')}**")
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.caption(f"类型: {scene.get('scene_type', '未知')}")
                        with col_b:
                            st.caption(f"时间: {scene.get('temporal_scope', '未知')}")
                        st.write(f"**用户意图**: {scene.get('user_intent', '暂无')[:100]}...")
                        keywords = normalize_keywords(scene.get('potential_keywords', []))
                        if keywords:
                            st.write("**关键词**:", ", ".join(keywords[:5]))
                        st.markdown("---")
        else:
            st.info("📋 所有生成的场景都与已有场景重复，未新增场景")

    except Exception as e:
        st.error(f"❌ 执行失败: {e}")
        import traceback
        traceback.print_exc()



def render_summary(result: dict):
    """渲染汇总信息"""
    summary = result.get('summary', {})

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🔥 实时热搜", summary.get('baidu_count', 0))

    with col2:
        st.metric("🎯 生成场景", summary.get('scenes_generated', 0))

    with col3:
        st.metric("🛍️ 匹配商品", summary.get('products_matched', 0))

    if 'last_update' in st.session_state:
        st.caption(f"最后更新: {st.session_state.last_update}")


def render_hot_topics(result: dict):
    """渲染热点监控页面"""
    st.subheader("🔥 实时热搜榜单")

    hot_data = result.get('hot_topics', {})
    baidu_topics = hot_data.get('baidu_hot', [])

    if baidu_topics:
        # 使用卡片式布局展示热搜
        st.markdown("### 🔴 百度热搜 Top 20")

        # 按行展示，每行3个
        cols_per_row = 3
        for idx in range(0, min(len(baidu_topics), 20), cols_per_row):
            cols = st.columns(cols_per_row)
            for col_idx in range(cols_per_row):
                topic_idx = idx + col_idx
                if topic_idx < len(baidu_topics) and topic_idx < 20:
                    topic = baidu_topics[topic_idx]
                    with cols[col_idx]:
                        # 热搜卡片
                        rank_color = "🥇" if topic['rank'] == 1 else "🥈" if topic['rank'] == 2 else "🥉" if topic['rank'] == 3 else f"#{topic['rank']}"

                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 0.5rem; color: white;">
                            <div style="font-size: 1.2rem; font-weight: bold;">{rank_color} {topic['title'][:15]}...</div>
                            <div style="font-size: 0.9rem; opacity: 0.9;">热度: {topic['heat']:,}</div>
                        </div>
                        """, unsafe_allow_html=True)
    else:
        st.info("暂无热搜数据，请先运行完整管道")


def render_scenes(result: dict):
    """渲染场景挖掘页面"""
    st.subheader("🎯 AI 生成的购物场景")

    scenes = result.get('scenes', [])

    if not scenes:
        st.info("暂无场景数据，请先运行完整管道")
        return

    for scene in scenes:
        with st.expander(f"📌 {scene['scene_name']}", expanded=False):
            # 场景基本信息
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"**场景类型**: {scene.get('scene_type', '未知')}")
                st.markdown(f"**触发事件**: {scene.get('trigger_event', '未知')}")

            with col2:
                st.markdown(f"**时间范围**: {scene.get('temporal_scope', '未知')}")
                st.markdown(f"**地理范围**: {scene.get('geo_scope', '未知')}")

            # 用户意图
            st.markdown("---")
            st.markdown(f"**🎯 用户意图**: {scene.get('user_intent', '暂无描述')}")
            st.markdown(f"**👥 目标人群**: {scene.get('target_population', '未知')}")

            # 关键词标签
            keywords = normalize_keywords(scene.get('potential_keywords', []))
            if keywords:
                st.markdown("**🔑 关键词**:")
                for keyword in keywords:
                    st.markdown(f'<span class="keyword-tag">{keyword}</span>', unsafe_allow_html=True)

            # 来源信息
            st.caption(f"来源热点: {scene.get('source_topic', '未知')}")


def render_products(result: dict):
    """渲染商品匹配页面"""
    st.subheader("🛍️ 匹配商品推荐")

    scenes = result.get('scenes', [])

    if not scenes:
        st.info("暂无场景数据，请先运行完整管道")
        return

    for scene in scenes:
        st.markdown(f"### 📌 {scene['scene_name']}")

        products = scene.get('matched_products', [])

        if products:
            # 按列显示商品
            cols_per_row = 3
            for idx in range(0, len(products), cols_per_row):
                cols = st.columns(cols_per_row)
                for col_idx, product in enumerate(products[idx:idx + cols_per_row]):
                    with cols[col_idx]:
                        st.markdown(f"""
                        <div class="product-card">
                            <strong>{product['title']}</strong><br/>
                            <small>{product['category']}</small><br/>
                            <span style="color: #e74c3c; font-weight: bold;">¥{product['price']}</span><br/>
                            <small>相关性: {product['relevance_score']:.2f}</small>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("该场景暂无匹配商品")


# ==================== 商品卡片组件（品类 emoji + 渐变封面） ====================
# image_url 指向的图片文件实际不存在，故用品类 emoji + 渐变色块作封面，无需任何图片资源
CATEGORY_EMOJI = {
    "酒水饮料": "🍺", "休闲零食": "🍪", "食品饮料": "🍜",
    "数码电器": "📱", "运动户外": "🏕️", "服饰鞋帽": "👕",
    "美妆护肤": "💄", "母婴用品": "🍼", "家居生活": "🏠",
    "时尚配饰": "💎", "医疗保健": "💊", "潮玩手办": "🎁", "成人用品": "🔒",
}
CATEGORY_GRADIENT = {
    "酒水饮料": "linear-gradient(135deg,#f59e0b,#ef4444)",
    "休闲零食": "linear-gradient(135deg,#f59e0b,#f97316)",
    "食品饮料": "linear-gradient(135deg,#f97316,#ef4444)",
    "数码电器": "linear-gradient(135deg,#3b82f6,#1e3a8a)",
    "运动户外": "linear-gradient(135deg,#10b981,#0d9488)",
    "服饰鞋帽": "linear-gradient(135deg,#8b5cf6,#6d28d9)",
    "美妆护肤": "linear-gradient(135deg,#ec4899,#db2777)",
    "母婴用品": "linear-gradient(135deg,#f472b6,#f9a8d4)",
    "家居生活": "linear-gradient(135deg,#0ea5e9,#22d3ee)",
    "时尚配饰": "linear-gradient(135deg,#eab308,#f59e0b)",
    "医疗保健": "linear-gradient(135deg,#14b8a6,#0ea5e9)",
    "潮玩手办": "linear-gradient(135deg,#a855f7,#ec4899)",
    "成人用品": "linear-gradient(135deg,#64748b,#475569)",
}


def _category_cover(category):
    """根据品类返回 (emoji, 渐变背景)"""
    return (
        CATEGORY_EMOJI.get(category, "📦"),
        CATEGORY_GRADIENT.get(category, "linear-gradient(135deg,#3b82f6,#8b5cf6)"),
    )


def render_product_card(product, reason=None):
    """渲染单个商品卡片（品类 emoji + 渐变封面），用于 AI 购物助手推荐"""
    emoji, gradient = _category_cover(product.get("category", ""))
    tags = product.get("tags") or []
    tags_html = "".join(f'<span class="keyword-tag">{t}</span>' for t in tags[:3])
    reason_html = f'<div class="rec-reason">💡 {reason}</div>' if reason else ""
    st.markdown(f'''
    <div class="product-card rec-card">
        <div class="product-cover" style="background:{gradient};">
            <span class="product-cover-emoji">{emoji}</span>
            <span class="product-cover-cat">{product.get('category', '')}</span>
        </div>
        <div class="product-card-body">
            <div class="product-title">{product.get('title', '')}</div>
            <div class="product-price">¥{product.get('price', '')}</div>
            <div class="product-tags">{tags_html}</div>
            {reason_html}
        </div>
    </div>
    ''', unsafe_allow_html=True)


def render_scene_product_card(product, scene_tag=None, attr_tags=None, highlights=None, reason=None):
    """渲染「AI 推荐」页的场景化商品卡片

    结构（从上到下）：
      1) 商品信息区 Header —— 与对话页商品卡片一致（品类 emoji + 渐变封面 + 标题/价格/标签）
      2) 场景标签（浅绿）+ 属性标签（浅蓝）
      3) 💡 AI 提炼产品亮点（列表）
      4) 🎯 AI 推荐理由（样式与对话页推荐理由一致）
    """
    emoji, gradient = _category_cover(product.get("category", ""))
    tags = product.get("tags") or []
    tags_html = "".join(f'<span class="keyword-tag">{t}</span>' for t in tags[:3])

    scene_html = f'<span class="scene-tag">#{scene_tag}</span>' if scene_tag else ""
    attr_html = "".join(f'<span class="attr-tag">#{t}</span>' for t in (attr_tags or [])[:4])
    tag_row_html = f'<div class="tag-row">{scene_html}{attr_html}</div>' if (scene_html or attr_html) else ""

    if highlights:
        hl_items = "".join(f"<li>{h}</li>" for h in highlights)
        highlights_html = (
            f'<div class="ai-highlights">'
            f'<span class="ai-section-title">💡 AI 提炼产品亮点</span>'
            f'<ul>{hl_items}</ul></div>'
        )
    else:
        highlights_html = ""

    reason_html = (
        f'<div class="ai-reason">'
        f'<span class="ai-section-title">🎯 AI 推荐理由</span>'
        f'<div>{reason}</div></div>'
    ) if reason else ""

    st.markdown(f'''
    <div class="product-card rec-card scene-rec-card">
        <div class="product-cover" style="background:{gradient};">
            <span class="product-cover-emoji">{emoji}</span>
            <span class="product-cover-cat">{product.get('category', '')}</span>
        </div>
        <div class="product-card-body">
            <div class="product-title">{product.get('title', '')}</div>
            <div class="product-price">¥{product.get('price', '')}</div>
            <div class="product-tags">{tags_html}</div>
            {tag_row_html}
            {highlights_html}
            {reason_html}
        </div>
    </div>
    ''', unsafe_allow_html=True)


def render_scene_submission():
    """渲染场景提报页面"""
    st.subheader("✍️ 人工提报场景")

    st.markdown("""
    输入场景名称/主题，系统将自动补全完整信息，包括：
    - 场景描述和用户意图
    - 时间和空间范围
    - 目标人群和潜在商品

    💡 支持一次生成多个场景，如输入"端午节"可生成：端午送礼、端午出游、自制粽子等多个场景
    """)

    with st.form("scene_submission_form"):
        scene_name = st.text_input(
            "场景名称/主题",
            placeholder="例如：端午节、春节、世界杯观赛、高考季...",
            help="输入场景主题，可生成多个不同角度的场景"
        )

        # 多场景选项
        col1, col2 = st.columns(2)
        with col1:
            generate_multiple = st.checkbox("生成多个场景", value=True, help="勾选后将为该主题生成多个不同角度的购物场景")

        with col2:
            scene_count = st.slider("场景数量", min_value=3, max_value=15, value=5,
                                   help="生成场景的数量，每个场景从不同角度切入")

        submitted = st.form_submit_button("🚀 生成场景", type="primary", use_container_width=True)

        if submitted and scene_name:
            # ── 终端风格日志面板（与热点 / 时节一致）──
            log_area = st.empty()
            with log_area.container():
                st.markdown(f'<div class="log-status">⏳ 正在生成场景信息…</div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="log-panel">'
                    f'<div class="log-step">📌 主题：{scene_name}'
                    f'（{"多场景" if generate_multiple else "单场景"}模式，{"预计 " + str(scene_count) + " 个" if generate_multiple else ""}）</div>'
                    f'<div class="log-llm">🤖 LLM 正在理解主题并生成购物场景…</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            try:
                service = get_service()
                result = service.submit_scene(scene_name, generate_multiple=generate_multiple, scene_count=scene_count)

                if result['success']:
                    if generate_multiple and 'scenes' in result:
                        # 多场景模式：批量保存
                        scenes = result['scenes']
                        save_result = service.save_scenes_batch(scenes)

                        # 更新日志面板为完成态
                        with log_area.container():
                            st.markdown(f'<div class="log-status">✅ 完成</div>', unsafe_allow_html=True)
                            st.markdown(
                                f'<div class="log-panel">'
                                f'<div class="log-step">📌 主题：{scene_name}（生成 {len(scenes)} 个场景）</div>'
                                f'<div class="log-success">✅ 成功生成 {len(scenes)} 个场景'
                                f' — 新增 {save_result["saved"]} 个，跳过 {save_result["skipped"]} 个重复</div>'
                                f'</div>',
                                unsafe_allow_html=True,
                            )

                            # 显示生成的场景
                            with st.expander("📋 查看生成的场景", expanded=True):
                                for scene in scenes:
                                    st.markdown(f"**📌 {scene.get('scene_name')}**")
                                    col_a, col_b = st.columns(2)
                                    with col_a:
                                        st.caption(f"类型: {scene.get('scene_type', '未知')}")
                                    with col_b:
                                        st.caption(f"时间: {scene.get('temporal_scope', '未知')}")
                                    keywords = normalize_keywords(scene.get('potential_keywords', []))
                                    if keywords:
                                        st.write("**关键词**:", ", ".join(keywords[:5]))
                                    st.markdown("---")

                            # 显示去重信息
                            if save_result['skipped_scenes']:
                                with st.expander(f"🔍 查看跳过的重复场景 ({len(save_result['skipped_scenes'])}个)", expanded=False):
                                    for skipped in save_result['skipped_scenes']:
                                        st.markdown(f"**{skipped['scene_name']}**")
                                        st.caption(f"与「{skipped['duplicate_of']}」重复: {skipped['reason']}")
                    else:
                        # 单场景模式：进入编辑
                        st.session_state.pending_scene = result['scene']
                        st.session_state.show_edit_mode = True
                        st.success("✅ 场景生成成功！请查看并编辑后保存")
                        st.rerun()
                else:
                    st.error(f"❌ {result.get('error', '生成失败')}")
            except Exception as e:
                    st.error(f"❌ 处理异常: {e}")


def render_scene_editor(scene: Dict):
    """渲染场景编辑预览页面"""
    st.subheader("👁️ 场景预览与编辑")

    st.markdown("---")
    st.markdown(f"### 📌 {scene.get('scene_name', '未命名场景')}")

    # 显示匹配的商品预览
    matched_products = scene.get('matched_products', [])
    if matched_products:
        st.markdown(f"**已匹配 {len(matched_products)} 个相关商品**")
        cols = st.columns(min(4, len(matched_products)))
        for idx, product in enumerate(matched_products[:8]):
            with cols[idx % 4]:
                st.caption(f"{product.get('title', 'Unknown')[:15]}... ¥{product.get('price', 0)}")

    st.markdown("---")

    with st.form("edit_scene_form"):
        st.markdown("#### 📝 编辑场景信息")

        col1, col2 = st.columns(2)

        with col1:
            edited_scene_name = st.text_input("场景名称", scene.get('scene_name', ''))
            edited_scene_type = st.text_input("场景类型", scene.get('scene_type', ''))
            edited_trigger = st.text_input("触发事件", scene.get('trigger_event', ''))

        with col2:
            edited_temporal = st.text_input("时间范围", scene.get('temporal_scope', ''))
            edited_geo = st.text_input("地理范围", scene.get('geo_scope', ''))
            edited_target = st.text_input("目标人群", scene.get('target_population', ''))

        edited_intent = st.text_area("用户意图", scene.get('user_intent', ''), height=100)

        edited_keywords = st.text_input(
            "关键词（逗号分隔）",
            ','.join(scene.get('potential_keywords', [])),
            help="用逗号分隔多个关键词"
        )

        st.markdown("---")

        btn_col1, btn_col2, btn_col3 = st.columns(3)

        with btn_col1:
            save = st.form_submit_button("💾 保存到场景库", type="primary", use_container_width=True)

        with btn_col2:
            delete = st.form_submit_button("🗑️ 放弃", use_container_width=True)

        with btn_col3:
            cancel = st.form_submit_button("❌ 取消", use_container_width=True)

        if save:
            # 更新场景数据
            updated_scene = {
                **scene,
                'scene_name': edited_scene_name,
                'scene_type': edited_scene_type,
                'trigger_event': edited_trigger,
                'temporal_scope': edited_temporal,
                'geo_scope': edited_geo,
                'user_intent': edited_intent,
                'target_population': edited_target,
                'potential_keywords': [k.strip() for k in edited_keywords.split(',') if k.strip()]
            }

            # 保存到场景库
            try:
                service = get_service()
                if service.save_scene(updated_scene):
                    st.success("✅ 场景已保存到场景库!")
                    st.session_state.show_edit_mode = False
                    st.session_state.pending_scene = None

                    # 刷新缓存数据
                    cached = service.get_cached_result()
                    st.session_state.cached_data = cached

                    st.rerun()
                else:
                    st.error("❌ 保存失败，请稍后重试")
            except Exception as e:
                st.error(f"❌ 保存异常: {e}")

        elif delete:
            st.session_state.show_edit_mode = False
            st.session_state.pending_scene = None
            st.info("🗑️ 已放弃此场景")
            st.rerun()

        elif cancel:
            st.session_state.show_edit_mode = False
            st.session_state.pending_scene = None
            st.rerun()


def render_scene_content(scene: Dict):
    """渲染场景内容（不使用 expander，用于嵌套场景）

    Args:
        scene: 场景对象
    """
    source_icon = {
        'seasonal': '📅',
        'hotspot': '🔥',
        'manual': '✍️'
    }.get(scene.get('source', 'hotspot'), '🔥')

    # 场景标题
    st.markdown(f"### {source_icon} {scene.get('scene_name', '未命名')}")

    # 场景基本信息
    col1, col2, col3 = st.columns(3)

    with col1:
        st.caption(f"类型: {scene.get('scene_type', '未知')}")

    with col2:
        st.caption(f"时间: {scene.get('temporal_scope', '未知')}")

    with col3:
        st.caption(f"地理: {scene.get('geo_scope', '未知')}")

    # 用户意图
    st.markdown(f"**🎯 用户意图**: {scene.get('user_intent', '暂无描述')}")

    # 关键词标签
    keywords = scene.get('potential_keywords', [])
    if keywords:
        st.markdown("**🔑 关键词:**")
        keyword_tags = " ".join([f'<span class="keyword-tag">{keyword}</span>' for keyword in keywords])
        st.markdown(keyword_tags, unsafe_allow_html=True)

    # 来源信息
    source_detail = scene.get('source_detail', '')
    if source_detail:
        st.caption(f"来源: {source_detail}")

    # 时节特有信息
    if scene.get('seasonal_event'):
        event = scene['seasonal_event']
        st.caption(f"时节事件: {event.get('name')} - {event.get('days_until', 0)}天后")


def render_scene_card(scene: Dict, expanded: bool = False):
    """渲染单个场景卡片（使用 expander）

    Args:
        scene: 场景对象
        expanded: 是否默认展开
    """
    source_icon = {
        'seasonal': '📅',
        'hotspot': '🔥',
        'manual': '✍️'
    }.get(scene.get('source', 'hotspot'), '🔥')

    with st.expander(f"{source_icon} {scene.get('scene_name', '未命名')}", expanded=expanded):
        # 场景基本信息
        col1, col2, col3 = st.columns(3)

        with col1:
            st.caption(f"类型: {scene.get('scene_type', '未知')}")

        with col2:
            st.caption(f"时间: {scene.get('temporal_scope', '未知')}")

        with col3:
            st.caption(f"地理: {scene.get('geo_scope', '未知')}")

        # 用户意图
        st.markdown(f"**🎯 用户意图**: {scene.get('user_intent', '暂无描述')}")

        # 关键词标签
        keywords = normalize_keywords(scene.get('potential_keywords', []))
        if keywords:
            st.markdown("**🔑 关键词:**")
            keyword_tags = " ".join([f'<span class="keyword-tag">{keyword}</span>' for keyword in keywords])
            st.markdown(keyword_tags, unsafe_allow_html=True)

        # 来源信息
        source_detail = scene.get('source_detail', '')
        if source_detail:
            st.caption(f"来源: {source_detail}")

        # 时节特有信息
        if scene.get('seasonal_event'):
            event = scene['seasonal_event']
            st.caption(f"时节事件: {event.get('name')} - {event.get('days_until', 0)}天后")

        # 匹配的商品（按品类分组显示）
        matched_products = scene.get('matched_products', [])
        if matched_products:
            st.markdown("---")
            product_summary = scene.get('product_summary', {})
            if product_summary:
                st.markdown(f"**🛍️ 关联商品**: 共 {product_summary.get('total_count', 0)} 个商品，{product_summary.get('category_count', 0)} 个品类")

            # 检测数据格式：按品类分组 vs 简单列表
            if matched_products and isinstance(matched_products, list) and len(matched_products) > 0:
                # 检查是否是分组格式（有 category 和 product_count 字段）
                is_grouped = 'category' in matched_products[0] and 'product_count' in matched_products[0]

                if is_grouped:
                    # 按品类显示商品（新格式）
                    for category_group in matched_products:
                        st.markdown(f"**📦 {category_group['category']}** ({category_group['product_count']} 个)")
                        for product in category_group['products'][:5]:  # 每个品类最多显示5个
                            st.markdown(f"  - **{product['title']}** ¥{product['price']} (相关度: {product.get('relevance_score', 'N/A')})")
                        if category_group['product_count'] > 5:
                            st.caption(f"  ... 还有 {category_group['product_count'] - 5} 个商品")
                else:
                    # 简单商品列表（旧格式），直接显示
                    st.markdown("**🛍️ 关联商品**:")
                    for product in matched_products[:10]:
                        st.markdown(f"  - **{product['title']}** ¥{product['price']} (相关度: {product.get('relevance_score', 'N/A')})")
                    if len(matched_products) > 10:
                        st.caption(f"  ... 还有 {len(matched_products) - 10} 个商品")
        else:
            # 没有匹配到商品
            st.caption("🛍️ 暂无关联商品（商品库中无匹配商品）")


def render_scene_review_mode():
    """渲染场景审核模式"""
    service = get_service()

    st.markdown("### 🔍 场景审核")

    # 获取当前处理的场景
    if 'seasonal_events' not in st.session_state:
        st.warning("⚠️ 未找到待审核的场景")
        if st.button("返回时节场景", use_container_width=True):
            st.session_state.show_review_mode = False
            st.rerun()
        return

    events = st.session_state.seasonal_events
    current_index = st.session_state.get('current_event_index', 0)
    total_events = len(events)

    # 如果当前事件已处理完
    if current_index >= total_events:
        st.success("✅ 所有场景审核完成！")
        st.session_state.show_review_mode = False
        st.session_state.pending_seasonal_scenes = []
        if st.button("返回时节场景", use_container_width=True):
            st.rerun()
        return

    # 获取当前事件
    current_event = events[current_index]

    # 显示事件信息（在生成场景之前就显示）
    st.markdown("---")
    st.markdown(f"### 📅 处理时节事件: {current_event['name']}")
    st.caption(f"日期: {current_event['date']} | 距离: {current_event['days_until']} 天")

    # 显示进度
    st.markdown(f"**进度**: {current_index + 1}/{total_events}")
    st.progress((current_index + 1) / total_events)

    # 检查是否已有生成的场景
    pending_scenes = st.session_state.get('pending_seasonal_scenes', [])
    scene_key = f"{current_event['name']}_{current_event['date']}"

    # 查找当前场景
    current_scene = None
    for scene in pending_scenes:
        if scene.get('scene_key') == scene_key:
            current_scene = scene
            break

    # 如果场景还未生成，先生成（带明显提示）
    if current_scene is None:
        # 显示生成状态占位符
        # 显示生成状态占位符
        status_placeholder = st.empty()
        with status_placeholder.container():
            st.info(f"🤖 正在为「{current_event['name']}」生成购物场景，请稍候...")
            st.progress(0, "调用 LLM 生成场景...")

        try:
            from src.seasonal_perception import SeasonalPerception
            seasonal = SeasonalPerception()

            # 构建场景名称
            days_until = current_event['days_until']
            event_name = current_event['name']

            if days_until < 0:
                scene_name = f"{event_name}进行时"
            elif days_until == 0:
                scene_name = f"{event_name}当天"
            else:
                scene_name = f"{event_name}临近"

            # 更新进度
            with status_placeholder.container():
                st.info(f"🤖 正在为「{current_event['name']}」生成购物场景，请稍候...")
                st.progress(0.3, "调用 LLM 生成场景...")

            # 使用LLM生成场景（支持自定义提示）
            llm = service.llm_client
            regenerate_prompt = st.session_state.get('regenerate_prompt', '')
            scene_data = llm.generate_scene(scene_name, custom_prompt=regenerate_prompt if regenerate_prompt else None)

            if scene_data and scene_data.get('scene_name'):
                # 更新进度
                with status_placeholder.container():
                    st.info(f"🤖 正在为「{current_event['name']}」生成购物场景，请稍候...")
                    st.progress(0.6, "场景生成成功，正在匹配商品...")

                # 创建场景对象
                from src.scene_mining import SceneMining
                mining = SceneMining(llm_client=llm)

                # 计算时间范围
                event_date = current_event['date_obj']
                temporal_scope = seasonal._calculate_temporal_scope(event_date, days_until)

                scene = mining._create_scene_object(
                    source_topic=f"时节事件: {event_name}",
                    scene_data=scene_data,
                    source='seasonal',
                    source_detail=event_name
                )

                # 覆盖时节相关字段
                scene['temporal_scope'] = temporal_scope
                scene['seasonal_event'] = {
                    'name': event_name,
                    'date': current_event['date'],
                    'days_until': days_until,
                    'type': current_event.get('type', 'traditional')
                }
                scene['scene_key'] = scene_key

                # 匹配商品
                keywords = scene.get('potential_keywords', [])
                matched = service.product_matching.match_products(keywords)
                scene['matched_products'] = matched

                # 添加到待审核列表
                pending_scenes.append(scene)
                st.session_state.pending_seasonal_scenes = pending_scenes
                current_scene = scene

                # 清除状态占位符
                status_placeholder.empty()
                st.success(f"✅「{current_event['name']}」场景生成成功！")
            else:
                status_placeholder.empty()
                st.error(f"❌「{current_event['name']}」场景生成失败")

        except Exception as e:
            status_placeholder.empty()
            st.error(f"❌ 生成失败: {e}")

    # 如果场景已生成，显示审核界面
    if current_scene:
        st.markdown("---")

        # 场景预览
        with st.expander("👁️ 场景预览", expanded=True):
            render_scene_content(current_scene)

        # 操作按钮
        st.markdown("---")
        st.markdown("### 🎯 场景操作")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("✅ 储存场景", type="primary", use_container_width=True, key=f"save_{scene_key}"):
                # 保存场景
                try:
                    # 清除编辑模式状态
                    st.session_state.edit_mode = False
                    st.session_state.editing_scene = None
                    st.session_state.regenerate_scene = False

                    if service.save_scene(current_scene):
                        st.success(f"✅ 场景「{current_scene['scene_name']}」已保存！")
                        # 移动到下一个
                        st.session_state.current_event_index = current_index + 1
                        st.rerun()
                    else:
                        st.error("❌ 保存失败")
                except Exception as e:
                    st.error(f"❌ 保存异常: {e}")

        with col2:
            if st.button("✏️ 编辑场景", use_container_width=True, key=f"edit_{scene_key}"):
                # 进入编辑模式
                st.session_state.editing_scene = current_scene
                st.session_state.edit_mode = True
                st.session_state.regenerate_scene = False
                st.rerun()

        with col3:
            if st.button("🔄 重新生成", use_container_width=True, key=f"regen_{scene_key}"):
                # 重新生成场景，清除编辑模式
                st.session_state.regenerate_scene = True
                st.session_state.regenerate_prompt = ""
                st.session_state.edit_mode = False
                st.session_state.editing_scene = None
                st.rerun()

        with col4:
            if st.button("⏭️ 跳过", use_container_width=True, key=f"skip_{scene_key}"):
                # 跳过当前场景，清除编辑模式
                st.session_state.edit_mode = False
                st.session_state.editing_scene = None
                st.session_state.regenerate_scene = False
                st.session_state.current_event_index = current_index + 1
                st.rerun()

        # 重新生成提示框
        if st.session_state.get('regenerate_scene'):
            st.markdown("---")
            st.markdown("### 🔄 重新生成场景")

            regenerate_prompt = st.text_area(
                "输入重新生成的提示词（可选）",
                placeholder="例如：更强调家庭聚会场景、增加礼品推荐...",
                key=f"regen_prompt_{scene_key}",
                help="留空则使用默认提示重新生成"
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("🚀 确认重新生成", type="primary", use_container_width=True, key=f"confirm_regen_{scene_key}"):
                    # 移除当前场景，准备重新生成
                    pending_scenes = [s for s in pending_scenes if s.get('scene_key') != scene_key]
                    st.session_state.pending_seasonal_scenes = pending_scenes
                    st.session_state.regenerate_scene = False
                    st.session_state.regenerate_prompt = regenerate_prompt
                    st.rerun()

            with col2:
                if st.button("❌ 取消", use_container_width=True, key=f"cancel_regen_{scene_key}"):
                    st.session_state.regenerate_scene = False
                    st.session_state.regenerate_prompt = ""
                    st.rerun()

    # 编辑模式
    if st.session_state.get('edit_mode') and st.session_state.get('editing_scene'):
        render_scene_edit_review(st.session_state.editing_scene)

    # 底部导航
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("⬅️ 上一个", use_container_width=True, disabled=current_index == 0):
            st.session_state.current_event_index = max(0, current_index - 1)
            st.session_state.regenerate_scene = False
            st.session_state.edit_mode = False
            st.rerun()

    with col2:
        st.metric("进度", f"{current_index + 1}/{total_events}")

    with col3:
        if st.button("返回时节场景", use_container_width=True):
            st.session_state.show_review_mode = False
            st.session_state.pending_seasonal_scenes = []
            st.session_state.current_event_index = 0
            st.rerun()


def render_scene_edit_review(scene: Dict):
    """渲染场景编辑审核页面"""
    st.markdown("---")
    st.markdown("### ✏️ 编辑场景")

    with st.form("edit_scene_review_form"):
        st.markdown("#### 📝 编辑场景信息")

        col1, col2 = st.columns(2)

        with col1:
            edited_scene_name = st.text_input("场景名称", scene.get('scene_name', ''))
            edited_scene_type = st.text_input("场景类型", scene.get('scene_type', ''))
            edited_trigger = st.text_input("触发事件", scene.get('trigger_event', ''))

        with col2:
            edited_temporal = st.text_input("时间范围", scene.get('temporal_scope', ''))
            edited_geo = st.text_input("地理范围", scene.get('geo_scope', ''))
            edited_target = st.text_input("目标人群", scene.get('target_population', ''))

        edited_intent = st.text_area("用户意图", scene.get('user_intent', ''), height=100)

        edited_keywords = st.text_input(
            "关键词（逗号分隔）",
            ','.join(scene.get('potential_keywords', [])),
            help="用逗号分隔多个关键词"
        )

        st.markdown("---")

        btn_col1, btn_col2, btn_col3 = st.columns(3)

        with btn_col1:
            save_edit = st.form_submit_button("💾 保存编辑", type="primary", use_container_width=True)

        with btn_col2:
            cancel_edit = st.form_submit_button("❌ 取消", use_container_width=True)

        with btn_col3:
            delete_edit = st.form_submit_button("🗑️ 删除场景", use_container_width=True)

        if save_edit:
            # 更新场景数据
            updated_scene = {
                **scene,
                'scene_name': edited_scene_name,
                'scene_type': edited_scene_type,
                'trigger_event': edited_trigger,
                'temporal_scope': edited_temporal,
                'geo_scope': edited_geo,
                'user_intent': edited_intent,
                'target_population': edited_target,
                'potential_keywords': [k.strip() for k in edited_keywords.split(',') if k.strip()]
            }

            # 重新匹配商品（按品类分组）
            keywords = updated_scene.get('potential_keywords', [])
            service = get_service()
            matched = service.product_matching.match_products(keywords, group_by_category=True)

            # 构建结构化的商品关联
            updated_scene['matched_products'] = matched
            updated_scene['product_summary'] = {
                'total_count': sum(group['product_count'] for group in matched),
                'category_count': len(matched),
                'categories': [group['category'] for group in matched]
            }

            # 更新待审核列表
            pending_scenes = st.session_state.get('pending_seasonal_scenes', [])
            scene_key = scene.get('scene_key')

            for idx, s in enumerate(pending_scenes):
                if s.get('scene_key') == scene_key:
                    pending_scenes[idx] = updated_scene
                    break

            st.session_state.pending_seasonal_scenes = pending_scenes
            st.session_state.editing_scene = updated_scene
            st.session_state.edit_mode = False
            st.success("✅ 编辑已保存！")
            st.rerun()

        elif cancel_edit:
            st.session_state.edit_mode = False
            st.session_state.editing_scene = None
            st.rerun()

        elif delete_edit:
            # 从待审核列表中删除
            pending_scenes = st.session_state.get('pending_seasonal_scenes', [])
            scene_key = scene.get('scene_key')
            pending_scenes = [s for s in pending_scenes if s.get('scene_key') != scene_key]
            st.session_state.pending_seasonal_scenes = pending_scenes
            st.session_state.edit_mode = False
            st.session_state.editing_scene = None
            st.info("🗑️ 场景已删除")
            st.rerun()


def render_hotspot_review_mode():
    """渲染热点场景审核模式（复用时节审核逻辑）"""
    service = get_service()

    st.markdown("### 🔍 热点场景审核")

    # 获取待审核的场景
    if 'pending_hotspot_scenes' not in st.session_state:
        st.warning("⚠️ 未找到待审核的场景")
        if st.button("返回热点追踪", use_container_width=True):
            st.session_state.show_hotspot_review_mode = False
            st.rerun()
        return

    scenes = st.session_state.pending_hotspot_scenes
    current_index = st.session_state.get('current_hotspot_index', 0)
    total_scenes = len(scenes)

    # 如果当前场景已处理完
    if current_index >= total_scenes:
        st.success("✅ 所有场景审核完成！")
        st.session_state.show_hotspot_review_mode = False
        st.session_state.pending_hotspot_scenes = []
        if st.button("返回热点追踪", use_container_width=True):
            st.rerun()
        return

    # 获取当前场景
    current_scene = scenes[current_index]
    scene_key = current_scene.get('scene_key', f'hotspot_{current_index}')

    # 显示进度
    st.markdown(f"**进度**: {current_index + 1}/{total_scenes}")
    st.progress((current_index + 1) / total_scenes)

    # 显示来源热点
    st.markdown("---")
    st.markdown(f"### 🔥 来源热点: {current_scene.get('source_topic', '未知')}")

    # 场景预览
    st.markdown("---")
    with st.expander("👁️ 场景预览", expanded=True):
        render_scene_content(current_scene)

    # 操作按钮
    st.markdown("---")
    st.markdown("### 🎯 场景操作")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("✅ 储存场景", type="primary", use_container_width=True, key=f"hot_save_{scene_key}"):
            # 保存场景
            try:
                # 清除编辑模式状态
                st.session_state.edit_mode = False
                st.session_state.editing_scene = None
                st.session_state.regenerate_scene = False

                if service.save_scene(current_scene):
                    st.success(f"✅ 场景「{current_scene['scene_name']}」已保存！")
                    # 移动到下一个
                    st.session_state.current_hotspot_index = current_index + 1
                    st.rerun()
                else:
                    st.error("❌ 保存失败")
            except Exception as e:
                st.error(f"❌ 保存异常: {e}")

    with col2:
        if st.button("✏️ 编辑场景", use_container_width=True, key=f"hot_edit_{scene_key}"):
            # 进入编辑模式
            st.session_state.editing_scene = current_scene
            st.session_state.edit_mode = True
            st.session_state.regenerate_scene = False
            st.rerun()

    with col3:
        if st.button("⏭️ 跳过", use_container_width=True, key=f"hot_skip_{scene_key}"):
            # 跳过当前场景，清除编辑模式
            st.session_state.edit_mode = False
            st.session_state.editing_scene = None
            st.session_state.regenerate_scene = False
            st.session_state.current_hotspot_index = current_index + 1
            st.rerun()

    with col4:
        if st.button("❌ 取消审核", use_container_width=True, key=f"hot_cancel_{scene_key}"):
            # 取消审核，返回热点追踪页面
            st.session_state.show_hotspot_review_mode = False
            st.session_state.edit_mode = False
            st.session_state.editing_scene = None
            st.rerun()

    # 编辑模式（复用时节编辑逻辑）
    if st.session_state.get('edit_mode') and st.session_state.get('editing_scene'):
        render_scene_edit_review(st.session_state.editing_scene)

    # 底部导航
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("⬅️ 上一个", use_container_width=True, disabled=current_index == 0, key=f"hot_prev_{scene_key}"):
            st.session_state.current_hotspot_index = max(0, current_index - 1)
            st.session_state.regenerate_scene = False
            st.session_state.edit_mode = False
            st.rerun()

    with col2:
        st.metric("进度", f"{current_index + 1}/{total_scenes}")

    with col3:
        if st.button("返回热点追踪", use_container_width=True):
            st.session_state.show_hotspot_review_mode = False
            st.session_state.pending_hotspot_scenes = []
            st.session_state.current_hotspot_index = 0
            st.rerun()


def render_seasonal_scenes():
    """渲染时节场景页面"""
    service = get_service()

    st.markdown("### 📅 时节场景")

    # 时节统计卡片
    seasonal_stats = service.get_seasonal_statistics()
    source_stats = service.get_source_statistics()['seasonal']

    # 统计概览 - 白色卡片
    st.markdown(f'''
    <div class="white-container">
        <div style="display: flex; justify-content: space-around; text-align: center;">
            <div>
                <div style="font-size: 0.8rem; color: #6b7280;">时节场景</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #1f2937;">{source_stats['count']}</div>
            </div>
            <div style="width: 1px; background: #e5e7eb;"></div>
            <div>
                <div style="font-size: 0.8rem; color: #6b7280;">临近事件</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #1f2937;">{seasonal_stats['upcoming_count']}</div>
            </div>
            <div style="width: 1px; background: #e5e7eb;"></div>
            <div>
                <div style="font-size: 0.8rem; color: #6b7280;">节日</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #1f2937;">{seasonal_stats['total_festivals']}</div>
            </div>
            <div style="width: 1px; background: #e5e7eb;"></div>
            <div>
                <div style="font-size: 0.8rem; color: #6b7280;">节气</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #1f2937;">{seasonal_stats['total_solar_terms']}</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # 第二行：节日和节气总数（可展开查看详情）
    # 获取节日和节气数据
    festivals = (
        service.seasonal_perception.festivals_data.get('traditional_festivals', []) +
        service.seasonal_perception.festivals_data.get('modern_festivals', [])
    )
    solar_terms = service.seasonal_perception.festivals_data.get('solar_terms', [])

    # 节日展开区域
    with st.expander(f"🎉 节日总数 ({len(festivals)}个)", expanded=False):
        st.markdown("#### 传统节日")
        traditional = service.seasonal_perception.festivals_data.get('traditional_festivals', [])
        for festival in traditional:
            st.markdown(f"- **{festival['name']}** ({festival['date']}) - {festival.get('description', '')}")

        st.markdown("#### 现代节日")
        modern = service.seasonal_perception.festivals_data.get('modern_festivals', [])
        for festival in modern:
            st.markdown(f"- **{festival['name']}** ({festival['date']}) - {festival.get('description', '')}")

    # 节气展开区域
    with st.expander(f"🌾 节气总数 ({len(solar_terms)}个)", expanded=False):
        cols_per_row = 4
        for idx in range(0, len(solar_terms), cols_per_row):
            cols = st.columns(cols_per_row)
            for col_idx in range(cols_per_row):
                term_idx = idx + col_idx
                if term_idx < len(solar_terms):
                    term = solar_terms[term_idx]
                    with cols[col_idx]:
                        st.markdown(f"**{term['name']}** ({term['date']})")
                        st.caption(f"{term.get('description', '')[:20]}...")

    # 生成时节场景区域
    st.markdown('''
    <h3 style="color: #1f2937; margin: 0 0 0.5rem 0; font-size: 1.3rem;">🔄 生成时节场景</h3>
    ''', unsafe_allow_html=True)
    st.caption("📅 选择日期范围，自动生成覆盖到的所有节日、节气相关场景（智能去重后直接保存）")
    st.caption("💡 每个节日/节气可生成多个场景，如：端午送礼、端午出游、自制粽子等")

    from datetime import datetime, timedelta

    # 日期范围选择
    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input(
            "开始日期",
            value=datetime.now().date(),
            max_value=datetime.now().date() + timedelta(days=365),
            key="seasonal_start_date"
        )

    with col2:
        end_date = st.date_input(
            "结束日期",
            value=datetime.now().date() + timedelta(days=90),
            max_value=datetime.now().date() + timedelta(days=365),
            key="seasonal_end_date"
        )

    # 显示将会生成的时节事件预览
    events = []
    if start_date and end_date:
        from src.seasonal_perception import SeasonalPerception
        seasonal = SeasonalPerception()

        # 获取日期范围内的时节事件
        start = datetime.combine(start_date, datetime.min.time())
        end = datetime.combine(end_date, datetime.min.time())

        all_events = (
            seasonal.festivals_data.get('traditional_festivals', []) +
            seasonal.festivals_data.get('modern_festivals', []) +
            seasonal.festivals_data.get('solar_terms', [])
        )

        for event in all_events:
            event_date = seasonal._parse_event_date(event['date'])
            if start <= event_date <= end:
                events.append({
                    'name': event['name'],
                    'date': event['date'],
                    'date_obj': event_date,
                    'days_until': (event_date - datetime.now()).days,
                    'description': event.get('description', '')
                })

        if events:
            st.caption(f"📋 将生成 {len(events)} 个时节场景：")
            # 按时间排序显示预览
            events.sort(key=lambda x: x['date_obj'])

            preview_cols = st.columns(3)
            for idx, event in enumerate(events[:9]):  # 最多显示9个预览
                with preview_cols[idx % 3]:
                    st.caption(f"**{event['name']}** ({event['date']})")

            if len(events) > 9:
                st.caption(f"... 还有 {len(events) - 9} 个事件")

    # 场景数量设置
    col1, col2 = st.columns(2)
    with col1:
        scenes_per_event = st.slider(
            "每个节日生成场景数",
            min_value=1,
            max_value=15,
            value=5,
            help="每个节日/节气会生成多个不同角度的购物场景"
        )
    with col2:
        st.metric("预计场景数", f"~{len(events) * scenes_per_event} 个")

    # 生成按钮
    if st.button("🚀 批量生成时节场景", type="primary", use_container_width=True, key="batch_generate_seasonal"):
        if events:
            # 将日期转换为 datetime 对象
            start_datetime = datetime.combine(start_date, datetime.min.time())
            end_datetime = datetime.combine(end_date, datetime.min.time())
            total_expected = len(events) * scenes_per_event

            # ── 终端风格日志面板（与热点追踪一致）──
            progress_area = st.empty()
            progress_logs = []
            current_step = ""

            def _render():
                with progress_area.container():
                    if current_step:
                        st.markdown(f'<div class="log-status">{current_step}</div>', unsafe_allow_html=True)
                    if progress_logs:
                        lines_html = ""
                        for log in progress_logs[-18:]:
                            cls = "log-line"
                            if log.startswith("📌"):   cls = "log-step"
                            elif log.startswith("✅"): cls = "log-success"
                            elif log.startswith("❌"): cls = "log-error"
                            log = log.replace("**", "")
                            lines_html += f'<div class="{cls}">{log}</div>'
                        st.markdown(f'<div class="log-panel">{lines_html}</div>', unsafe_allow_html=True)

            def _cb(event_type, *args):
                nonlocal current_step
                if event_type == 'processing':
                    idx, total, name = args
                    current_step = f"⏳ 处理中 ({idx}/{total})"
                    progress_logs.append(f"📌 [{idx}/{total}] 处理: {name}（生成 {scenes_per_event} 个场景）")
                    _render()

            current_step = f"⏳ 开始生成（{len(events)} 个事件，预计 {total_expected} 个场景）"
            progress_logs.append(f"📌 时节事件共 {len(events)} 个，每个生成 {scenes_per_event} 个场景")
            _render()

            result = service.generate_seasonal_scenes(
                auto_save=True,
                scenes_per_event=scenes_per_event,
                start_date=start_datetime,
                end_date=end_datetime,
                progress_callback=_cb,
            )

            saved = result.get('saved', 0)
            skipped = result.get('skipped', 0)
            skipped_scenes = result.get('skipped_scenes', [])

            progress_logs.append(f"✅ 生成完成 — 新增 {saved} 个场景，跳过 {skipped} 个重复")
            current_step = "✅ 完成"
            _render()

            st.success(f"✅ 生成完成! 新增 {saved} 个场景，跳过 {skipped} 个重复场景")

            # 显示去重详情
            if skipped_scenes:
                with st.expander(f"🔍 查看跳过的重复场景 ({len(skipped_scenes)}个)", expanded=False):
                    for skipped in skipped_scenes:
                        st.markdown(f"**{skipped['scene_name']}**")
                        st.caption(f"与「{skipped['duplicate_of']}」重复: {skipped['reason']}")

            # 显示新增场景列表
            if saved > 0:
                with st.expander(f"📋 查看新增的场景 ({saved}个)", expanded=True):
                    for scene in result.get('scenes', []):
                        # 检查场景是否被保存
                        is_saved = not any(s['scene_name'] == scene['scene_name'] for s in skipped_scenes)
                        if is_saved:
                            st.markdown(f"**📌 {scene.get('scene_name')}**")
                            col_a, col_b = st.columns(2)
                            with col_a:
                                st.caption(f"类型: {scene.get('scene_type', '未知')}")
                            with col_b:
                                st.caption(f"时间: {scene.get('temporal_scope', '未知')}")
                            st.write(f"**用户意图**: {scene.get('user_intent', '暂无')[:100]}...")
                            keywords = normalize_keywords(scene.get('potential_keywords', []))
                            if keywords:
                                st.write("**关键词**:", ", ".join(keywords[:5]))
                            st.markdown("---")
            else:
                st.info("📋 所有生成的场景都与已有场景重复，未新增场景")

            st.info("💡 场景已保存到场景库，可在「场景库管理」中进行编辑和删除")
        else:
            st.warning("⚠️  选择的时间范围内没有时节事件")

    # 显示临近时节事件
    if seasonal_stats.get('upcoming_events'):
        st.markdown('''
        <h3 style="color: #1f2937; margin: 1.5rem 0 0.5rem 0; font-size: 1.3rem;">📆 临近时节事件</h3>
        ''', unsafe_allow_html=True)

        events = seasonal_stats['upcoming_events'][:6]

        cols = st.columns(3)

        for idx, event in enumerate(events):
            with cols[idx % 3]:
                days_until = event.get('days_until', 0)
                if days_until == 0:
                    status = "今天"
                elif days_until < 0:
                    status = f"已过{abs(days_until)}天"
                else:
                    status = f"{days_until}天后"

                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 12px; color: white; margin: 0.5rem 0;">
                    <div style="font-size: 1.1rem; font-weight: bold;">{event['name']}</div>
                    <div style="font-size: 0.9rem; opacity: 0.9;">{status}</div>
                </div>
                """, unsafe_allow_html=True)

    # 场景列表
    scenes = service.get_scenes_by_source('seasonal')

    st.markdown('''
    <h3 style="color: #1f2937; margin: 1.5rem 0 0.5rem 0; font-size: 1.3rem;">📋 时节场景列表</h3>
    ''', unsafe_allow_html=True)

    if scenes:
        for scene in scenes:
            render_scene_card(scene)
    else:
        st.info("暂无时节场景，请先生成时节场景")


def render_hotspot_scenes():
    """渲染热点追踪页面"""
    service = get_service()

    st.markdown("### 🔥 热点追踪")

    # 热点统计
    source_stats = service.get_source_statistics()['hotspot']
    # 获取实时热搜（使用默认10条）
    hot_data = service.get_hot_topics_only(limit=10)
    hot_count = len(hot_data.get('baidu_hot', []))

    # 统计概览 - 白色卡片
    st.markdown(f'''
    <div class="white-container">
        <div style="display: flex; justify-content: space-around; text-align: center;">
            <div>
                <div style="font-size: 0.8rem; color: #6b7280;">热点场景</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #1f2937;">{source_stats['count']}</div>
            </div>
            <div style="width: 1px; background: #e5e7eb;"></div>
            <div>
                <div style="font-size: 0.8rem; color: #6b7280;">实时热搜</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #1f2937;">{hot_count}</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # 热点抓取区域
    st.markdown("---")
    st.markdown("### 🔍 抓取实时热点")
    st.info("抓取百度实时热搜，自动生成购物场景（智能去重后直接保存）")

    col1, col2 = st.columns(2)
    with col1:
        hot_limit = st.slider("热点数量", 5, 20, 10)
    with col2:
        scene_limit = st.slider("生成场景", 3, 10, 5)

    if st.button("🚀 开始抓取", type="primary", use_container_width=True):
        run_pipeline(hot_limit, scene_limit)

    # 展示实时热搜
    if hot_data.get('baidu_hot'):
        st.markdown("---")
        st.markdown("### 🔴 实时热搜 Top 10")

        baidu_topics = hot_data.get('baidu_hot', [])[:10]

        cols_per_row = 2
        for idx in range(0, len(baidu_topics), cols_per_row):
            cols = st.columns(cols_per_row)
            for col_idx in range(cols_per_row):
                topic_idx = idx + col_idx
                if topic_idx < len(baidu_topics):
                    topic = baidu_topics[topic_idx]
                    with cols[col_idx]:
                        st.markdown(f"**#{topic['rank']}** {topic['title']}")
                        st.caption(f"热度: {topic['heat']:,}")

    # 场景列表
    st.markdown("---")
    st.markdown("### 📋 热点场景列表")

    scenes = service.get_scenes_by_source('hotspot')

    if scenes:
        # 按创建时间倒序
        scenes.sort(key=lambda x: x.get('created_at', ''), reverse=True)

        for scene in scenes[:20]:  # 最多显示20个
            render_scene_card(scene)
    else:
        st.info("暂无热点场景，请先抓取热点")


def render_manual_scenes():
    """渲染人工提报页面"""
    service = get_service()

    st.markdown("### ✍️ 人工提报")

    # 人工提报统计
    source_stats = service.get_source_statistics()['manual']
    total_scenes = len(service.scene_mining.load_scenes())

    # 统计概览 - 白色卡片
    st.markdown(f'''
    <div class="white-container">
        <div style="display: flex; justify-content: space-around; text-align: center;">
            <div>
                <div style="font-size: 0.8rem; color: #6b7280;">人工场景</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #1f2937;">{source_stats['count']}</div>
            </div>
            <div style="width: 1px; background: #e5e7eb;"></div>
            <div>
                <div style="font-size: 0.8rem; color: #6b7280;">场景库总数</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #1f2937;">{total_scenes}</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # 提报表单
    st.markdown("---")
    render_scene_submission()

    # 已提报场景列表
    st.markdown("---")
    st.markdown("### 📋 已提报场景")

    scenes = service.get_scenes_by_source('manual')

    if scenes:
        # 按创建时间倒序
        scenes.sort(key=lambda x: x.get('created_at', ''), reverse=True)

        for scene in scenes:
            render_scene_card(scene)
    else:
        st.info("暂无人工提报场景")


def render_scene_library():
    """渲染场景库管理页面"""
    service = get_service()

    st.markdown("### 📚 场景库管理")

    st.info("💡 所有时节场景和热点追踪生成的场景已自动保存（智能去重）。您可以在此处统一编辑、删除或管理场景。")

    # 统计信息
    all_scenes = service.scene_mining.load_scenes()
    seasonal_count = len([s for s in all_scenes if s.get('source') == 'seasonal'])
    hotspot_count = len([s for s in all_scenes if s.get('source') == 'hotspot'])
    manual_count = len([s for s in all_scenes if s.get('source') == 'manual'])

    # 统计概览 - 白色卡片
    st.markdown(f'''
    <div class="white-container">
        <div style="display: flex; justify-content: space-around; text-align: center;">
            <div>
                <div style="font-size: 0.75rem; color: #6b7280;">场景总数</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #1f2937;">{len(all_scenes)}</div>
            </div>
            <div style="width: 1px; background: #e5e7eb;"></div>
            <div>
                <div style="font-size: 0.75rem; color: #6b7280;">时节</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #1f2937;">{seasonal_count}</div>
            </div>
            <div style="width: 1px; background: #e5e7eb;"></div>
            <div>
                <div style="font-size: 0.75rem; color: #6b7280;">热点</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #1f2937;">{hotspot_count}</div>
            </div>
            <div style="width: 1px; background: #e5e7eb;"></div>
            <div>
                <div style="font-size: 0.75rem; color: #6b7280;">人工</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #1f2937;">{manual_count}</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # 筛选选项
    st.markdown("---")
    st.markdown("### 🔍 场景筛选")

    col1, col2, col3 = st.columns(3)

    with col1:
        source_filter = st.selectbox(
            "来源筛选",
            ["全部", "时节场景", "热点场景", "人工场景"],
            help="按场景来源筛选"
        )

    with col2:
        search_keyword = st.text_input(
            "搜索关键词",
            placeholder="输入场景名称或关键词...",
            help="搜索场景名称或关键词"
        )

    with col3:
        sort_by = st.selectbox(
            "排序方式",
            ["创建时间（最新）", "创建时间（最早）", "场景名称（A-Z）"],
            help="场景排序方式"
        )

    # 应用筛选和排序
    filtered_scenes = all_scenes.copy()

    # 来源筛选
    if source_filter == "时节场景":
        filtered_scenes = [s for s in filtered_scenes if s.get('source') == 'seasonal']
    elif source_filter == "热点场景":
        filtered_scenes = [s for s in filtered_scenes if s.get('source') == 'hotspot']
    elif source_filter == "人工场景":
        filtered_scenes = [s for s in filtered_scenes if s.get('source') == 'manual']

    # 关键词搜索
    if search_keyword:
        search_lower = search_keyword.lower()
        filtered_scenes = [
            s for s in filtered_scenes
            if search_lower in s.get('scene_name', '').lower() or
            any(search_lower in kw.lower() for kw in s.get('potential_keywords', []))
        ]

    # 排序
    if sort_by == "创建时间（最新）":
        filtered_scenes.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    elif sort_by == "创建时间（最早）":
        filtered_scenes.sort(key=lambda x: x.get('created_at', ''), reverse=False)
    elif sort_by == "场景名称（A-Z）":
        filtered_scenes.sort(key=lambda x: x.get('scene_name', ''))

    # 显示筛选结果
    st.markdown(f"**显示 {len(filtered_scenes)} 个场景**")

    if not filtered_scenes:
        st.info("暂无符合条件的场景")
        return

    # 批量操作
    st.markdown("---")
    if st.button("🗑️ 批量删除（筛选结果）", use_container_width=True):
        st.session_state.batch_delete_mode = True
        st.session_state.batch_delete_scenes = filtered_scenes
        st.rerun()

    # 场景列表（带操作按钮）
    st.markdown("---")

    for idx, scene in enumerate(filtered_scenes):
        scene_id = scene.get('scene_id', f'unknown_{idx}')

        # 场景卡片
        with st.expander(f"📌 {scene.get('scene_name', '未命名')}", expanded=False):
            # 场景基本信息
            col1, col2 = st.columns(2)

            with col1:
                st.caption(f"ID: {scene_id[:20]}...")
                st.caption(f"类型: {scene.get('scene_type', '未知')}")
                source_icon = {'seasonal': '📅', 'hotspot': '🔥', 'manual': '✍️'}.get(scene.get('source', ''), '')
                st.caption(f"来源: {source_icon} {scene.get('source_type', '未知')}")

            with col2:
                created_time = scene.get('created_at', '未知')
                if created_time and len(created_time) > 10:
                    created_time = created_time[:10].replace('T', ' ')
                st.caption(f"创建时间: {created_time}")
                st.caption(f"时间范围: {scene.get('temporal_scope', '未知')}")

            # 用户意图和关键词
            st.markdown(f"**🎯 用户意图**: {scene.get('user_intent', '暂无')[:100]}...")

            keywords = scene.get('potential_keywords', [])
            if keywords:
                st.markdown("**🔑 关键词**:")
                keyword_tags = " ".join([f'<span class="keyword-tag">{keyword}</span>' for keyword in keywords])
                st.markdown(keyword_tags, unsafe_allow_html=True)

            # 匹配的商品（按品类分组显示）
            matched_products = scene.get('matched_products', [])
            if matched_products:
                product_summary = scene.get('product_summary', {})
                if product_summary:
                    st.markdown(f"**🛍️ 关联商品**: 共 {product_summary.get('total_count', 0)} 个商品，{product_summary.get('category_count', 0)} 个品类")

                # 检测数据格式：按品类分组 vs 简单列表
                if matched_products and isinstance(matched_products, list) and len(matched_products) > 0:
                    # 检查是否是分组格式（有 category 和 product_count 字段）
                    is_grouped = 'category' in matched_products[0] and 'product_count' in matched_products[0]

                    if is_grouped:
                        # 按品类显示商品（新格式）
                        for category_group in matched_products:
                            # 使用标题而非 expander，避免嵌套
                            st.markdown(f"**📦 {category_group['category']}** ({category_group['product_count']} 个)")
                            for product in category_group['products'][:5]:  # 每个品类最多显示5个
                                st.markdown(f"  - **{product['title']}** ¥{product['price']} (相关度: {product.get('relevance_score', 'N/A')})")
                            if category_group['product_count'] > 5:
                                st.caption(f"  ... 还有 {category_group['product_count'] - 5} 个商品")
                    else:
                        # 简单商品列表（旧格式），直接显示
                        st.markdown("**🛍️ 关联商品**:")
                        for product in matched_products[:10]:
                            st.markdown(f"- **{product['title']}** ¥{product['price']} (相关度: {product.get('relevance_score', 'N/A')})")
                        if len(matched_products) > 10:
                            st.caption(f"... 还有 {len(matched_products) - 10} 个商品")
            else:
                # 没有匹配到商品
                st.caption("🛍️ 暂无关联商品（商品库中无匹配商品）")

            # 操作按钮
            st.markdown("---")
            btn_col1, btn_col2, btn_col3 = st.columns(3)

            with btn_col1:
                if st.button("✏️ 编辑", use_container_width=True, key=f"lib_edit_{idx}"):
                    st.session_state.editing_scene = scene
                    st.session_state.scene_library_mode = True
                    st.session_state.scene_library_source = 'library'
                    st.rerun()

            with btn_col2:
                if st.button("📋 复制", use_container_width=True, key=f"lib_copy_{idx}"):
                    # 复制场景到人工提报
                    st.session_state.pending_scene = scene.copy()
                    st.session_state.pending_scene['scene_id'] = None  # 移除ID以便创建新场景
                    st.session_state.show_edit_mode = True
                    st.session_state.copy_mode = True
                    st.info(f"✅ 场景「{scene.get('scene_name')}」已复制到编辑器")
                    st.rerun()

            with btn_col3:
                if st.button("🗑️ 删除", use_container_width=True, key=f"lib_delete_{idx}"):
                    # 确认删除
                    st.session_state.deleting_scene_id = scene_id
                    st.session_state.deleting_scene = scene
                    st.rerun()


def _render_recommendations(recs):
    """在一行内渲染推荐商品卡片网格"""
    if not recs:
        return
    cols = st.columns(min(3, len(recs)))
    for col, r in zip(cols, recs):
        with col:
            render_product_card(r.get('product', {}), r.get('reason'))


# 「AI 推荐」页的场景胶囊（label / 场景标签 / 匹配关键词）
AI_RECOMMEND_SCENES = [
    {"label": "🏕️ 露营",     "scene_tag": "露营经济场景", "keywords": ["露营", "帐篷", "户外", "野营", "烧烤"]},
    {"label": "🏃 户外运动", "scene_tag": "户外运动场景", "keywords": ["运动", "跑步", "健身", "徒步", "骑行"]},
    {"label": "⚽ 看球聚会", "scene_tag": "赛事聚会场景", "keywords": ["啤酒", "世界杯", "看球", "聚会", "零食"]},
    {"label": "💄 护肤美容", "scene_tag": "颜值经济场景", "keywords": ["护肤", "面膜", "美妆", "精华", "防晒"]},
    {"label": "📱 数码生活", "scene_tag": "数码生活场景", "keywords": ["数码", "耳机", "手机", "智能", "音箱"]},
    {"label": "🍼 母婴亲子", "scene_tag": "母婴亲子场景", "keywords": ["婴儿", "母婴", "纸尿裤", "奶粉", "玩具"]},
    {"label": "🍜 居家美食", "scene_tag": "居家美食场景", "keywords": ["零食", "火锅", "方便面", "美食", "调料"]},
    {"label": "🧹 居家生活", "scene_tag": "居家生活场景", "keywords": ["收纳", "清洁", "家居", "扫地"]},
]


def render_ai_recommend():
    """渲染「AI 推荐」页面：顶部场景筛选胶囊 + 下方垂直商品卡片列表"""
    st.markdown("""
    <div style="text-align:center; padding:0.5rem 0 0.25rem 0;">
        <h1 style="font-size:1.8rem; font-weight:700; background:linear-gradient(135deg,#3b82f6,#8b5cf6);
           -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin:0;">🎯 AI 推荐 · 场景化选品</h1>
        <p style="color:#6b7280; margin-top:0.4rem;">选择一个场景，AI 结合商品属性与场景为你精选好物，并提炼产品亮点与推荐理由</p>
    </div>
    """, unsafe_allow_html=True)

    # 默认选中第一个场景
    if 'ai_rec_scene' not in st.session_state:
        st.session_state.ai_rec_scene = AI_RECOMMEND_SCENES[0]['label']

    # 顶部场景筛选胶囊（每行 4 个）
    st.markdown("#### 🏷️ 选择场景")
    for i in range(0, len(AI_RECOMMEND_SCENES), 4):
        row = AI_RECOMMEND_SCENES[i:i + 4]
        cols = st.columns(len(row))
        for col, sc in zip(cols, row):
            selected = st.session_state.ai_rec_scene == sc['label']
            if col.button(
                sc['label'],
                key=f"scene_capsule_{sc['label']}",
                use_container_width=True,
                type="primary" if selected else "secondary",
            ):
                st.session_state.ai_rec_scene = sc['label']
                st.rerun()

    current = next(s for s in AI_RECOMMEND_SCENES if s['label'] == st.session_state.ai_rec_scene)

    st.markdown('<div style="height:1px; background:linear-gradient(90deg,transparent,#e5e7eb,transparent); margin:1.25rem 0 0.5rem 0;"></div>', unsafe_allow_html=True)
    st.markdown(f"##### 🔍 {current['label']} · 场景标签 `#{current['scene_tag']}` 为你精选")

    # 先渲染 chrome（标题/胶囊/副标题），再初始化推荐引擎并拉取
    recommender = get_service().get_recommender()
    cache = st.session_state.setdefault('ai_rec_cache', {})

    if current['label'] not in cache:
        # ── 暗色终端日志面板（与热点/时节/提报一致）──
        log_area = st.empty()
        loading_spacer = st.empty()   # 撑满视口，覆盖旧页残留（拉取完成后清除）
        with log_area.container():
            st.markdown(f'<div class="log-status">⏳ 正在分析场景…</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="log-panel">'
                f'<div class="log-step">📌 场景：{current["label"]}（{current["scene_tag"]}）</div>'
                f'<div class="log-llm">🤖 LLM 正在结合商品属性与场景标签精选好物、提炼亮点与推荐理由…</div>'
                f'<div class="log-detail">关键词：{", ".join(current["keywords"][:5])}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        loading_spacer.markdown('<div style="min-height:55vh"></div>', unsafe_allow_html=True)
        try:
            cache[current['label']] = recommender.recommend_by_scene(
                current['label'], current['scene_tag'], current['keywords'], top_n=6
            )
        except Exception as e:
            cache[current['label']] = []
            loading_spacer.empty()
            log_area.error(f'生成失败：{e}')
            return

        recs = cache.get(current['label'], [])
        loading_spacer.empty()   # 清除占位，卡片接替填入
        with log_area.container():
            st.markdown(f'<div class="log-status">✅ 完成</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="log-panel">'
                f'<div class="log-step">📌 场景：{current["label"]}（{current["scene_tag"]}）</div>'
                f'<div class="log-success">✅ 已生成 {len(recs)} 张推荐卡片，含亮点提炼与推荐理由</div>'
                f'<div class="log-detail">示例：{recs[0]["product"]["title"] if recs else ""}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # 数据就绪：渲染商品卡片列表
    cards = cache.get(current['label'], [])
    if not cards:
        st.info("该场景暂无匹配商品，试试其他场景～")
    else:
        for c in cards:
            render_scene_product_card(
                c.get('product', {}),
                scene_tag=c.get('scene_tag'),
                attr_tags=c.get('attr_tags'),
                highlights=c.get('highlights'),
                reason=c.get('reason'),
            )
            st.markdown("")  # 卡片间留白


def render_chatbot():
    """渲染 AI 购物助手页面：登录(Marla/Steve) + 多轮对话 + 个性化商品卡片推荐"""
    service = get_service()
    recommender = service.get_recommender()
    users = recommender.list_users()

    # 初始化会话状态
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []

    # ==================== 登录态：选择用户 ====================
    if not st.session_state.get('current_user'):
        st.markdown("""
        <div style="text-align:center; padding:1rem 0 0.5rem 0;">
            <h1 style="font-size:1.8rem; font-weight:700; background:linear-gradient(135deg,#3b82f6,#8b5cf6); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin:0;">🤖 AI 购物助手</h1>
            <p style="color:#6b7280; margin-top:0.5rem;">登录后，与懂你的 AI 助手聊聊，获得应时应景的个性化推荐</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 👋 请选择一个用户登录")
        cols = st.columns(len(users)) if users else [st.container()]
        for col, u in zip(cols, users):
            with col:
                interests = "".join(f'<span class="keyword-tag">{it}</span>' for it in u.get('interests', [])[:4])
                st.markdown(f'''
                <div class="persona-card">
                    <div style="font-size:3rem; text-align:center;">{u.get('avatar_emoji','🙂')}</div>
                    <h3 style="text-align:center; margin:0.5rem 0; color:#1f2937;">{u.get('name')}</h3>
                    <p style="text-align:center; color:#6b7280; font-size:0.82rem; min-height:3rem;">{u.get('persona','')}</p>
                    <div style="text-align:center; margin-top:0.5rem;">{interests}</div>
                </div>
                ''', unsafe_allow_html=True)
                if st.button(f"以 {u.get('name')} 登录", key=f"login_{u.get('user_id')}", use_container_width=True):
                    st.session_state.current_user = u.get('user_id')
                    st.session_state.chat_messages = []
                    st.rerun()
        return

    # ==================== 已登录：对话界面 ====================
    user_id = st.session_state.current_user
    profile = recommender.get_profile(user_id)
    if not profile:
        st.error("用户画像加载失败，请重新登录。")
        if st.button("返回登录"):
            st.session_state.current_user = None
            st.rerun()
        return

    # 顶栏：当前用户 + 操作
    tcol1, tcol2, tcol3 = st.columns([6, 1, 1])
    with tcol1:
        st.markdown(f"### {profile.get('avatar_emoji')} 与 **{profile.get('name')}** 的购物对话")
    with tcol2:
        if st.button("🔄 切换用户", use_container_width=True, key="switch_user"):
            st.session_state.current_user = None
            st.session_state.chat_messages = []
            st.rerun()
    with tcol3:
        if st.button("🗑️ 清空对话", use_container_width=True, key="clear_chat"):
            st.session_state.chat_messages = []
            st.rerun()

    # 主体：左侧对话 + 右侧画像/场景
    chat_col, info_col = st.columns([3.2, 1])

    with info_col:
        st.markdown("##### 👤 用户画像")
        st.caption(profile.get('persona', ''))
        st.markdown(f"**基础**：{profile['basics'].get('age')}岁 · {profile['basics'].get('city')} · {profile['basics'].get('occupation')}")

        prefs = profile.get('preferences', {})
        st.markdown("**偏好品类**")
        st.markdown(" · ".join(prefs.get('favorite_categories', [])))
        pr = prefs.get('price_range', [])
        if len(pr) == 2:
            st.caption(f"预算区间 ¥{pr[0]} ~ ¥{pr[1]}")

        st.markdown("**兴趣标签**")
        interest_html = "".join(f'<span class="keyword-tag">{it}</span>' for it in profile.get('interests', []))
        st.markdown(interest_html, unsafe_allow_html=True)

        hist = profile.get('history', {})
        purchased_titles = []
        for sku in hist.get('purchased', []):
            prod = service.product_matching.get_product_by_sku(sku)
            if prod:
                purchased_titles.append(prod.get('title'))
        if purchased_titles:
            st.markdown("**近期购买（历史兴趣）**")
            for t in purchased_titles:
                st.markdown(f"· {t}")

        st.markdown("---")
        st.markdown("##### 🌐 当前参考场景")
        st.caption("推荐会结合以下时节/热点场景：")
        try:
            scenes = recommender._scene_summary(recommender._get_active_scenes())
        except Exception:
            scenes = []
        for s in scenes[:6]:
            st.markdown(
                f"<div style='margin:0.2rem 0;'><span class='keyword-tag'>{s.get('source_type','')}</span> "
                f"<span style='font-size:0.8rem;color:#374151;'>{s.get('scene_name','')}</span></div>",
                unsafe_allow_html=True
            )

    with chat_col:
        # 渲染历史对话
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg['role']):
                st.markdown(msg['content'])
                if msg['role'] == 'assistant' and msg.get('recommendations'):
                    _render_recommendations(msg['recommendations'])

        # 输入框
        if prompt := st.chat_input(f"和 {profile.get('name')} 的购物助手聊聊吧～（例如：周末想出游 / 最近有什么新品）"):
            # 追加用户消息
            st.session_state.chat_messages.append({'role': 'user', 'content': prompt})
            with st.chat_message('user'):
                st.markdown(prompt)

            # 调用推荐引擎
            with st.chat_message('assistant'):
                with st.spinner('正在结合你的兴趣与当下场景为你挑选…'):
                    slim_history = [{'role': m['role'], 'content': m['content']} for m in st.session_state.chat_messages]
                    try:
                        result = recommender.chat(user_id, slim_history)
                    except Exception as e:
                        result = {'reply': f'（出错了：{e}）', 'recommendations': []}
                st.markdown(result['reply'])
                if result.get('recommendations'):
                    _render_recommendations(result['recommendations'])

            # 持久化助手回复
            st.session_state.chat_messages.append({
                'role': 'assistant',
                'content': result['reply'],
                'recommendations': result.get('recommendations', []),
            })


def handle_library_modals():
    """场景库的删除确认 / 批量删除 / 库内编辑弹窗。

    多页架构下由「场景库」页调用：若渲染了某个弹窗则返回 True，页面跳过常规库列表渲染。
    """
    # 单个删除确认
    if st.session_state.get('deleting_scene'):
        scene = st.session_state.deleting_scene
        scene_id = st.session_state.deleting_scene_id

        st.markdown("### 🗑️ 确认删除场景")
        st.warning(f"确定要删除场景「{scene.get('scene_name', '未命名')}」吗？此操作不可恢复。")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("确认删除", type="primary", use_container_width=True):
                try:
                    service = get_service()
                    if service.delete_scene(scene_id):
                        st.success(f"✅ 场景「{scene.get('scene_name')}」已删除")
                        st.session_state.deleting_scene = None
                        st.session_state.deleting_scene_id = None
                        st.rerun()
                    else:
                        st.error("❌ 删除失败")
                except Exception as e:
                    st.error(f"❌ 删除异常: {e}")

        with col2:
            if st.button("取消", use_container_width=True):
                st.session_state.deleting_scene = None
                st.session_state.deleting_scene_id = None
                st.rerun()

        return True

    # 批量删除确认
    if st.session_state.get('batch_delete_mode'):
        batch_scenes = st.session_state.get('batch_delete_scenes', [])

        st.markdown("### 🗑️ 批量删除确认")
        st.warning(f"确定要删除 **{len(batch_scenes)}** 个场景吗？此操作不可恢复。")

        # 显示要删除的场景列表
        st.markdown("**将要删除的场景：**")
        for i, scene in enumerate(batch_scenes[:10], 1):
            st.markdown(f"{i}. {scene.get('scene_name', '未命名')} ({scene.get('source', 'unknown')})")
        if len(batch_scenes) > 10:
            st.caption(f"... 还有 {len(batch_scenes) - 10} 个场景")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("确认批量删除", type="primary", use_container_width=True):
                try:
                    service = get_service()
                    deleted_count = 0
                    failed_count = 0

                    for scene in batch_scenes:
                        scene_id = scene.get('scene_id', '')
                        if service.delete_scene(scene_id):
                            deleted_count += 1
                        else:
                            failed_count += 1

                    if deleted_count > 0:
                        st.success(f"✅ 成功删除 {deleted_count} 个场景")
                    if failed_count > 0:
                        st.warning(f"⚠️ {failed_count} 个场景删除失败")

                    # 清除批量删除状态
                    st.session_state.batch_delete_mode = False
                    st.session_state.batch_delete_scenes = []
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ 删除异常: {e}")

        with col2:
            if st.button("取消", use_container_width=True):
                st.session_state.batch_delete_mode = False
                st.session_state.batch_delete_scenes = []
                st.rerun()

        return True

    # 场景库内编辑
    if st.session_state.get('scene_library_mode') and st.session_state.get('editing_scene'):
        render_header()
        render_library_scene_editor(st.session_state.editing_scene)
        return True

    return False


def render_library_scene_editor(scene: Dict):
    """渲染场景库场景编辑页面"""
    st.subheader("✏️ 编辑场景")

    st.markdown("---")
    st.markdown(f"### 📌 {scene.get('scene_name', '未命名场景')}")

    # 显示匹配的商品预览
    matched_products = scene.get('matched_products', [])
    if matched_products:
        st.markdown(f"**已匹配 {len(matched_products)} 个相关商品**")
        cols = st.columns(min(4, len(matched_products)))
        for idx, product in enumerate(matched_products[:8]):
            with cols[idx % 4]:
                st.caption(f"{product.get('title', 'Unknown')[:15]}... ¥{product.get('price', 0)}")

    st.markdown("---")

    with st.form("library_edit_scene_form"):
        st.markdown("#### 📝 编辑场景信息")

        col1, col2 = st.columns(2)

        with col1:
            edited_scene_name = st.text_input("场景名称", scene.get('scene_name', ''))
            edited_scene_type = st.text_input("场景类型", scene.get('scene_type', ''))
            edited_trigger = st.text_input("触发事件", scene.get('trigger_event', ''))

        with col2:
            edited_temporal = st.text_input("时间范围", scene.get('temporal_scope', ''))
            edited_geo = st.text_input("地理范围", scene.get('geo_scope', ''))
            edited_target = st.text_input("目标人群", scene.get('target_population', ''))

        edited_intent = st.text_area("用户意图", scene.get('user_intent', ''), height=100)

        edited_keywords = st.text_input(
            "关键词（逗号分隔）",
            ','.join(scene.get('potential_keywords', [])),
            help="用逗号分隔多个关键词"
        )

        st.markdown("---")

        btn_col1, btn_col2, btn_col3 = st.columns(3)

        with btn_col1:
            save = st.form_submit_button("💾 保存修改", type="primary", use_container_width=True)

        with btn_col2:
            cancel = st.form_submit_button("❌ 取消", use_container_width=True)

        with btn_col3:
            delete = st.form_submit_button("🗑️ 删除场景", use_container_width=True)

        if save:
            # 更新场景数据
            updated_scene = {
                **scene,
                'scene_name': edited_scene_name,
                'scene_type': edited_scene_type,
                'trigger_event': edited_trigger,
                'temporal_scope': edited_temporal,
                'geo_scope': edited_geo,
                'user_intent': edited_intent,
                'target_population': edited_target,
                'potential_keywords': [k.strip() for k in edited_keywords.split(',') if k.strip()]
            }

            # 重新匹配商品（按品类分组）
            keywords = updated_scene.get('potential_keywords', [])
            service = get_service()
            matched = service.product_matching.match_products(keywords, group_by_category=True)

            # 构建结构化的商品关联
            updated_scene['matched_products'] = matched
            updated_scene['product_summary'] = {
                'total_count': sum(group['product_count'] for group in matched),
                'category_count': len(matched),
                'categories': [group['category'] for group in matched]
            }

            # 保存到文件
            try:
                import json
                from src.config import Config

                # 加载所有场景
                all_scenes = service.scene_mining.load_scenes()

                # 更新对应的场景
                scene_id = scene.get('scene_id')
                for idx, s in enumerate(all_scenes):
                    if s.get('scene_id') == scene_id:
                        all_scenes[idx] = updated_scene
                        break

                # 保存
                with open(Config.SCENARIOS_PATH, 'w', encoding='utf-8') as f:
                    json.dump(all_scenes, f, ensure_ascii=False, indent=2)

                st.success("✅ 场景已更新!")
                st.session_state.scene_library_mode = False
                st.session_state.editing_scene = None

                st.rerun()
            except Exception as e:
                st.error(f"❌ 保存异常: {e}")

        elif cancel:
            st.session_state.scene_library_mode = False
            st.session_state.editing_scene = None
            st.rerun()

        elif delete:
            st.session_state.deleting_scene_id = scene.get('scene_id')
            st.session_state.deleting_scene = scene
            st.session_state.scene_library_mode = False
            st.session_state.editing_scene = None
            st.rerun()

