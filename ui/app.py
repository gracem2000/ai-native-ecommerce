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

# 设置页面配置 - 在所有其他内容之前
st.set_page_config(
    page_title="AI场景供给系统",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 加载外部CSS样式
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "style.css")
    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except:
        # 如果CSS文件不存在，使用内联样式
        pass

load_css()

# 强制应用红色边框样式
st.markdown('''
<style>
.stTextInput input, .stDateInput input, .stSelectbox select,
.stTextInput > div > div > input, .stDateInput > div > div > input, .stSelectbox > div > div > select,
div[data-testid="stTextInput"] input, div[data-testid="stDateInput"] input, div[data-testid="stSelectbox"] select {
    border: 1px solid #ef4444 !important;
    border-radius: 6px !important;
}
.stTextInput input:focus, .stDateInput input:focus, .stSelectbox select:focus,
.stTextInput > div > div > input:focus, .stDateInput > div > div > input:focus, .stSelectbox > div > div > select:focus,
div[data-testid="stTextInput"] input:focus, div[data-testid="stDateInput"] input:focus, div[data-testid="stSelectbox"] select:focus {
    border-color: #dc2626 !important;
    box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.15) !important;
}
</style>
''', unsafe_allow_html=True)


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
        <h1 style="font-size: 1.5rem; margin-bottom: 0.5rem; color: #1f2937; font-weight: 600;">电商场景智能供给系统</h1>
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

    st.markdown('<h2 style="text-align: center; margin: 1rem 0 1.5rem 0; font-size: 1.5rem;">两大核心功能</h2>', unsafe_allow_html=True)

    # 两大功能入口卡片：左 = 场景供给中心（功能一），右 = AI 购物助手（功能二）
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('''
        <div class="hero-card" style="text-align:left;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🧭</div>
            <h3 style="color: #1f2937; margin: 0 0 0.5rem 0; font-size: 1.3rem;">功能一 · 场景供给中心</h3>
            <p style="color: #6b7280; margin: 0 0 1rem 0; font-size: 0.9rem;">
                面向运营的后端演示：从<b>热点感知</b>、<b>季节感知</b>到<b>场景挖掘</b>与<b>商品匹配</b>的全链路闭环。
            </p>
            <div style="font-size:0.78rem; color:#6b7280; margin-bottom:0.75rem;">
                📅 时节 · 🔥 热点 · ✍️ 提报 · 📚 场景库
            </div>
        </div>
        ''', unsafe_allow_html=True)

        sub1, sub2 = st.columns(2)
        with sub1:
            if st.button("📅 时节场景", key="home_seasonal", use_container_width=True):
                st.session_state.current_page = 'seasonal'
                st.rerun()
            if st.button("✍️ 人工提报", key="home_manual", use_container_width=True):
                st.session_state.current_page = 'manual'
                st.rerun()
        with sub2:
            if st.button("🔥 热点追踪", key="home_hotspot", use_container_width=True):
                st.session_state.current_page = 'hotspot'
                st.rerun()
            if st.button("📚 场景库", key="home_library", use_container_width=True):
                st.session_state.current_page = 'library'
                st.rerun()

    with col_right:
        st.markdown('''
        <div class="hero-card" style="text-align:left; background: linear-gradient(135deg,#3b82f6,#8b5cf6); color:white;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🤖</div>
            <h3 style="color:white; margin: 0 0 0.5rem 0; font-size: 1.3rem;">功能二 · AI 购物助手</h3>
            <p style="color:rgba(255,255,255,0.92); margin: 0 0 1rem 0; font-size: 0.9rem;">
                面向用户的前端对话：登录为 <b>Marla</b> 或 <b>Steve</b>，与 AI 助手聊天，结合<b>历史兴趣</b>、<b>时节</b>与<b>热点场景</b>，获得带推荐理由的个性化商品推荐。
            </p>
            <div style="font-size:0.78rem; color:rgba(255,255,255,0.85);">
                🗣️ 多轮对话 · 🎯 个性化推荐 · 🃏 商品卡片
            </div>
        </div>
        ''', unsafe_allow_html=True)

        if st.button("🤖 登录并开始对话", key="home_chatbot", use_container_width=True):
            st.session_state.current_page = 'chatbot'
            st.rerun()

    st.markdown('<div style="height: 1px; background: linear-gradient(90deg, transparent, #e5e7eb, transparent); margin: 2rem 0;"></div>', unsafe_allow_html=True)

    # 系统特性 - 现代化卡片设计
    st.markdown('<h2 style="text-align: center; margin: 2rem 0; font-size: 1.5rem;">核心能力</h2>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('''
        <div class="feature-card">
            <div class="feature-icon">🧠</div>
            <h4 style="color: #1f2937; margin: 0.5rem 0; font-size: 1.3rem;">智能场景生成</h4>
            <p style="color: #6b7280; font-size: 0.875rem; margin: 0;">基于 LLM 的场景理解和生成</p>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        st.markdown('''
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <h4 style="color: #1f2937; margin: 0.5rem 0; font-size: 1.3rem;">精准商品匹配</h4>
            <p style="color: #6b7280; font-size: 0.875rem; margin: 0;">关键词驱动的智能商品推荐</p>
        </div>
        ''', unsafe_allow_html=True)

    with col3:
        st.markdown('''
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <h4 style="color: #1f2937; margin: 0.5rem 0; font-size: 1.3rem;">实时数据更新</h4>
            <p style="color: #6b7280; font-size: 0.875rem; margin: 0;">热点数据实时抓取和更新</p>
        </div>
        ''', unsafe_allow_html=True)

    # 底部技术信息
    st.markdown('<div style="height: 1px; background: linear-gradient(90deg, transparent, #e5e7eb, transparent); margin: 2rem 0;"></div>', unsafe_allow_html=True)

    st.markdown('''
    <div style="text-align: center; padding: 1rem 0;">
        <p style="color: #9ca3af; font-size: 0.875rem;">
            Powered by <span style="font-weight: 600; color: #3b82f6;">智谱 GLM-5.1</span> · AI-Native 场景供给平台
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
            margin: -1rem -1rem 1.5rem -1rem;
            color: white;
        ">
            <div style="font-size: 1.5rem; font-weight: 700; display: flex; align-items: center; gap: 0.5rem;">
                <span>🎯</span>
                <span>场景供给</span>
            </div>
            <div style="font-size: 0.8rem; opacity: 0.8; margin-top: 0.5rem;">
                AI-Native 演示系统
            </div>
        </div>
        ''', unsafe_allow_html=True)

        # 返回首页按钮
        if st.button("🏠 首页", use_container_width=True, key="nav_home"):
            if 'current_page' in st.session_state:
                del st.session_state.current_page
            st.rerun()

        st.markdown("---")

        # 导航菜单
        st.markdown('<div style="color: #6b7280; font-size: 0.75rem; font-weight: 600; margin-bottom: 0.5rem; text-transform: uppercase;">功能一 · 场景供给中心</div>', unsafe_allow_html=True)

        nav_items = [
            ("📅 时节场景", "seasonal"),
            ("🔥 热点追踪", "hotspot"),
            ("✍️ 人工提报", "manual"),
            ("📚 场景库", "library"),
        ]

        current_page = st.session_state.get('current_page', '')

        for icon, page in nav_items:
            is_active = current_page == page
            button_style = """
                background: """ + ("linear-gradient(135deg, #3b82f6, #8b5cf6)" if is_active else "#f9fafb") + """;
                color: """ + ("white" if is_active else "#1f2937") + """;
                border: 1px solid """ + ("transparent" if is_active else "#e5e7eb") + """;
                padding: 0.75rem 1rem;
                border-radius: 8px;
                margin: 0.25rem 0;
                font-weight: 500;
            """
            if st.button(icon, use_container_width=True, key=f"nav_{page}"):
                st.session_state.current_page = page
                st.rerun()

        # 功能二：AI 购物助手
        st.markdown('<div style="color: #6b7280; font-size: 0.75rem; font-weight: 600; margin: 1rem 0 0.5rem 0; text-transform: uppercase;">功能二 · AI 购物助手</div>', unsafe_allow_html=True)

        if st.button("🤖 AI购物助手", use_container_width=True, key="nav_chatbot"):
            st.session_state.current_page = 'chatbot'
            st.rerun()

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
            """渲染进度信息"""
            with progress_area.container():
                if current_step:
                    st.info(f"**{current_step}**")

                if progress_logs:
                    st.markdown("#### 📋 详细处理日志")
                    for log in progress_logs[-10:]:  # 只显示最后10条
                        st.markdown(log)

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

        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("🚀 生成场景", type="primary", use_container_width=True)
        with col2:
            example = st.form_submit_button("📝 示例", use_container_width=True)

        if example:
            st.info("示例主题：端午节、春节、世界杯观赛、高考季、双十一购物")

        if submitted and scene_name:
            with st.spinner(f"🤖 正在生成场景信息..."):
                try:
                    service = get_service()
                    result = service.submit_scene(scene_name, generate_multiple=generate_multiple, scene_count=scene_count)

                    if result['success']:
                        if generate_multiple and 'scenes' in result:
                            # 多场景模式：批量保存
                            scenes = result['scenes']
                            save_result = service.save_scenes_batch(scenes)

                            st.success(f"✅ 成功生成 {len(scenes)} 个场景！")
                            st.info(f"💾 保存结果: 新增 {save_result['saved']} 个场景，跳过 {save_result['skipped']} 个重复场景")

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
            # 直接生成并自动保存，不进入审核模式
            total_expected = len(events) * scenes_per_event
            # 将日期转换为 datetime 对象
            start_datetime = datetime.combine(start_date, datetime.min.time())
            end_datetime = datetime.combine(end_date, datetime.min.time())
            with st.spinner(f"🔄 正在为 {len(events)} 个时节事件生成场景（预计 {total_expected} 个）..."):
                result = service.generate_seasonal_scenes(
                    auto_save=True,
                    scenes_per_event=scenes_per_event,
                    start_date=start_datetime,
                    end_date=end_datetime
                )

            saved = result.get('saved', 0)
            skipped = result.get('skipped', 0)
            skipped_scenes = result.get('skipped_scenes', [])

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


def main():
    """主函数 - 首页导航 + 详细页面"""
    # 渲染侧边栏
    render_sidebar()

    # 检查是否有待删除的场景
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

        return

    # 检查是否在批量删除模式
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

        return

    # 检查是否有待编辑的场景（人工提报或复制）
    if st.session_state.get('show_edit_mode') and st.session_state.get('pending_scene'):
        render_header()
        render_scene_editor(st.session_state.pending_scene)
        return

    # 检查是否在场景库编辑模式
    if st.session_state.get('scene_library_mode') and st.session_state.get('editing_scene'):
        render_header()
        render_library_scene_editor(st.session_state.editing_scene)
        return

    # 根据 current_page 决定显示内容
    current_page = st.session_state.get('current_page')

    if current_page == 'seasonal':
        # 时节场景详细页面
        render_header()
        render_seasonal_scenes()

    elif current_page == 'hotspot':
        # 热点追踪详细页面
        render_header()
        render_hotspot_scenes()

    elif current_page == 'manual':
        # 人工提报详细页面
        render_header()
        render_manual_scenes()

    elif current_page == 'library':
        # 场景库管理页面
        render_header()
        render_scene_library()

    elif current_page == 'chatbot':
        # AI 购物助手对话页面（自带标题，不使用通用 header）
        render_chatbot()

    else:
        # 首页展示
        render_homepage()


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


if __name__ == "__main__":
    main()
