import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="财务分析看板 · 数智赋能工业AI", layout="wide", page_icon="📊")

st.markdown("""
<style>
    .big-number {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1f3a5f;
        line-height: 1.2;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #6b7280;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    .ai-box {
        background: linear-gradient(135deg, #f0f4ff 0%, #e8edf5 100%);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        border-left: 5px solid #ff7f2a;
        margin: 0.8rem 0;
    }
    .suggestion-box {
        background: #fef9e7;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        border-left: 4px solid #f39c12;
        margin: 0.5rem 0;
    }
    .footer-card {
        background: #1f3a5f;
        border-radius: 16px;
        padding: 1.8rem 2rem;
        color: white;
        margin-top: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 1rem;
        font-weight: 600;
        padding: 0.6rem 1.8rem;
    }
</style>
""", unsafe_allow_html=True)

years = ["第一年\n(试点期)", "第二年\n(增长期)", "第三年\n(扩张期)"]
revenue = [85, 220, 480]
cost = [58, 122, 230]
profit = [27, 98, 250]
gross_margin = [31.7, 44.5, 52.1]
customers = [2, 9, 28]
recurring_ratio = [0, 21.8, 38.5]
team = [6, 10, 18]

structure_data = {
    "年份": ["第一年", "第二年", "第三年"],
    "一次性部署+硬件": [85, 172, 295],
    "SaaS年费": [0, 30, 107],
    "节能效益分成": [0, 18, 78]
}
df_structure = pd.DataFrame(structure_data)

cost_detail = {
    "年份": ["第一年", "第二年", "第三年"],
    "固定成本": [8, 22, 54],
    "变动成本": [22, 48, 95],
    "期间费用": [28, 52, 99]
}
df_cost = pd.DataFrame(cost_detail)

months = list(range(1, 13))
monthly_revenue_y1 = [2, 3, 4, 5, 6, 8, 10, 14, 11, 8, 7, 7]
monthly_cost_y1 = [4, 4, 5, 5, 5, 6, 7, 8, 6, 5, 4, 4]

st.title("财务分析 · 数智赋能工业AI项目")
st.caption("轻资产模式 · 三年滚动预测 · AI智能诊断")

tab1, tab2, tab3, tab4 = st.tabs(["第一年 · 试点期", "第二年 · 增长期", "第三年 · 扩张期", "三年总览"])

with tab1:
    st.subheader("第一年 · 试点落地期")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("营业收入", "85 万元", delta="基准线")
    with col2:
        st.metric("综合成本", "58 万元", delta="预算内", delta_color="normal")
    with col3:
        st.metric("毛利润", "27 万元", delta="正向")
    with col4:
        st.metric("毛利率", "31.7%", delta="vs 行业均值 35%", delta_color="off")
    
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=months, y=monthly_revenue_y1, mode='lines+markers', 
                              name='营收', line=dict(color='#1f3a5f', width=3),
                              marker=dict(size=8, color='#1f3a5f')))
    fig1.add_trace(go.Scatter(x=months, y=monthly_cost_y1, mode='lines+markers',
                              name='成本', line=dict(color='#e74c3c', width=3, dash='dot'),
                              marker=dict(size=8, color='#e74c3c')))
    fig1.add_annotation(x=9, y=14, text="⚡ 首个标杆项目交付", showarrow=True, arrowhead=2,
                        ax=-80, ay=-30, font=dict(size=12, color="#1f3a5f"))
    fig1.update_layout(title="月度营收/成本趋势", height=350, template="plotly_white",
                       xaxis_title="月份", yaxis_title="万元", legend=dict(orientation="h", y=1.02))
    st.plotly_chart(fig1, use_container_width=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        fig_pie = go.Figure(data=[go.Pie(labels=['固定成本 8万 (13.8%)', '变动成本 22万 (37.9%)', '期间费用 28万 (48.3%)'],
                                         values=[8, 22, 28], marker=dict(colors=['#2ecc71', '#3498db', '#f39c12']),
                                         textinfo='label', textposition='inside')])
        fig_pie.update_layout(title="成本结构拆解", height=300)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="ai-box">
            <b>AI 自动解读</b><br>
            • 期间费用占比 <b>48.3%</b>，高于健康线（<40%），其中营销费用 8 万对应仅 2 个订单，<b>单客获客成本 4 万元</b>，偏高。<br>
            • Q3 出现营收拐点，验证了 "以案例代广告" 策略的有效性。<br>
            • 依托校内资源，固定成本仅 8 万，比行业平均低 40%。
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("#### 年度经营诊断")
        diag_data = {
            "维度": ["营收规模", "盈利质量", "成本控制", "客户集中度"],
            "状态": ["待提升", "健康", "优秀", "高风险"],
            "评价": ["85万低于同类均值120万", "首年即实现27万正利润", "固定成本比行业低40%", "单一客户占比70.6%"]
        }
        st.dataframe(pd.DataFrame(diag_data), use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("#### 改进建议（面向第二年）")
        st.markdown("""
        <div class="suggestion-box">
            <b>1. 客户数量翻倍</b> — 目标从 2 家增至 8-10 家，单客占比压至 30% 以下<br>
            <b>2. 收入结构多元化</b> — 新增 SaaS 年费（15万）+ 节能分成（8万）<br>
            <b>3. 压缩交付周期</b> — 从 4 个月压至 2.5 个月（标准化工具包上线）<br>
            <b>4. 推出 "轻量版"</b> — 定价 5-8 万，降低决策门槛
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div class="ai-box" style="border-left-color:#1f3a5f;">
        <b>AI 总结</b>：第一年选择 "慢启动、深打磨"，85万营收验证了商业模式和付费意愿，27万正利润证明轻资产模型跑得通。但单一客户占比70%、Q1-Q2零订单是两个预警信号。第二年核心策略：<b>从 "做深一个" 转向 "做宽一批"</b>。
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.subheader("第二年 · 快速增长期")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("营业收入", "220 万元", delta="+158.8%", delta_color="normal")
    with col2:
        st.metric("综合成本", "122 万元", delta="+110.3%", delta_color="off")
    with col3:
        st.metric("毛利润", "98 万元", delta="+263%", delta_color="normal")
    with col4:
        st.metric("毛利率", "44.5%", delta="+12.8pp", delta_color="normal")
    
    fig2 = make_subplots(rows=1, cols=2, subplot_titles=("季度营收/成本趋势", "收入结构 (万元)"))
    quarters = ["Q1", "Q2", "Q3", "Q4"]
    q_rev = [45, 50, 58, 67]
    q_cost = [26, 28, 32, 36]
    fig2.add_trace(go.Bar(x=quarters, y=q_rev, name="营收", marker_color="#1f3a5f"), row=1, col=1)
    fig2.add_trace(go.Bar(x=quarters, y=q_cost, name="成本", marker_color="#e74c3c"), row=1, col=1)
    fig2.add_trace(go.Bar(x=["第二年"], y=[172], name="部署+硬件", marker_color="#3498db"), row=1, col=2)
    fig2.add_trace(go.Bar(x=["第二年"], y=[30], name="SaaS年费", marker_color="#2ecc71"), row=1, col=2)
    fig2.add_trace(go.Bar(x=["第二年"], y=[18], name="节能分成", marker_color="#f39c12"), row=1, col=2)
    fig2.update_layout(height=350, template="plotly_white", showlegend=True)
    fig2.update_xaxes(title_text="季度", row=1, col=1)
    fig2.update_yaxes(title_text="万元", row=1, col=1)
    st.plotly_chart(fig2, use_container_width=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("#### 年度经营诊断")
        diag_data2 = {
            "维度": ["营收规模", "盈利质量", "毛利率", "收入结构", "现金流"],
            "状态": ["优秀", "优秀", "健康", "待优化", "健康"],
            "评价": ["220万超目标，增速158.8%", "98万利润，3.6倍于首年", "44.5%接近行业均值", "持续性收入仅21.8%", "经营性现金流约+70万"]
        }
        st.dataframe(pd.DataFrame(diag_data2), use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("#### 改进建议（面向第三年）")
        st.markdown("""
        <div class="suggestion-box">
            <b>1. 主推 "节能分成"</b> — 目标持续性收入占比 ≥ 35%<br>
            <b>2. 区域复制</b> — 从东北一省扩展到三省+内蒙古东部<br>
            <b>3. 产品标准化达70%</b> — 定制化适配从40%压至25%<br>
            <b>4. 打造 "客户成功" 团队</b> — 专人负责续约与增购
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div class="ai-box" style="border-left-color:#1f3a5f;">
        <b>AI 总结</b>：第二年是从 "1到N" 的关键跨越。220万营收、98万利润、44.5%毛利率全部超预期。收入结构从 "100%一次性" 优化为 "78%部署+22%持续"，客户数从2家扩展到9家，<b>商业模式已经从 "项目制生存" 进化到 "产品化增长"</b>。第三年核心：把 "节能分成" 模式铺开。
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.subheader("第三年 · 规模化扩张期")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("营业收入", "480 万元", delta="+118.2%", delta_color="normal")
    with col2:
        st.metric("综合成本", "230 万元", delta="+88.5%", delta_color="off")
    with col3:
        st.metric("毛利润", "250 万元", delta="+155.1%", delta_color="normal")
    with col4:
        st.metric("毛利率", "52.1%", delta="+7.6pp", delta_color="normal")
    
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=["第一年", "第二年", "第三年"], y=[85, 172, 295],
                         name="部署+硬件", marker_color="#3498db"))
    fig3.add_trace(go.Bar(x=["第一年", "第二年", "第三年"], y=[0, 30, 107],
                         name="SaaS年费", marker_color="#2ecc71"))
    fig3.add_trace(go.Bar(x=["第一年", "第二年", "第三年"], y=[0, 18, 78],
                         name="节能分成", marker_color="#f39c12"))
    fig3.update_layout(title="收入结构演化 (三年堆积对比)", height=350, template="plotly_white",
                       barmode="stack", xaxis_title="年份", yaxis_title="万元",
                       legend=dict(orientation="h", y=1.02))
    fig3.add_annotation(x=2, y=400, text="持续性收入 38.5%", showarrow=True,
                        arrowhead=2, ax=40, ay=-30, font=dict(size=13, color="#1f3a5f"))
    st.plotly_chart(fig3, use_container_width=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("#### 年度经营诊断")
        diag_data3 = {
            "维度": ["营收规模", "盈利质量", "毛利率", "收入结构", "市场地位"],
            "状态": ["优秀", "卓越", "高毛利", "健康", "领先"],
            "评价": ["480万达规模化门槛", "累计毛利润375万", "52.1%超行业均值", "持续性38.5%达标", "东北细分赛道渗透率第一"]
        }
        st.dataframe(pd.DataFrame(diag_data3), use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("#### 改进建议（面向第四年）")
        st.markdown("""
        <div class="suggestion-box">
            <b>1. 出省战略</b> — 进军京津冀，瞄准同类型铸造产业集群<br>
            <b>2. 产品矩阵扩展</b> — 从热处理优化延伸到全流程，客单价 15万→40万+<br>
            <b>3. 申报专精特新 "小巨人"</b> — 争取政策补贴 50-100万<br>
            <b>4. 启动 Pre-A 轮融资</b> — 融资 500-800万，用于区域扩张
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div class="ai-box" style="border-left-color:#1f3a5f;">
        <b>AI 总结</b>：第三年完成从 "项目型公司" 到 "产品型平台" 的质变。480万营收、52.1%毛利率、38.5%持续性收入占比 — 三项指标均达细分赛道领先水平。<b>185万年费+分成收入意味着即便不发展新客户，现有客户池也能支撑持续运营。</b> 三年累计毛利润375万，投资回收期1.8年，轻资产模式完全跑通。
    </div>
    """, unsafe_allow_html=True)

with tab4:
    st.subheader("三年对比总览 · 财务全景")
    
    fig4 = make_subplots(specs=[[{"secondary_y": True}]])
    fig4.add_trace(go.Scatter(x=years, y=revenue, mode='lines+markers', name='营收',
                             line=dict(color='#1f3a5f', width=4), marker=dict(size=12)), secondary_y=False)
    fig4.add_trace(go.Scatter(x=years, y=gross_margin, mode='lines+markers', name='毛利率 (%)',
                             line=dict(color='#ff7f2a', width=4, dash='dot'), marker=dict(size=12)), secondary_y=True)
    fig4.update_layout(title="营收 & 毛利率 三年趋势", height=350, template="plotly_white",
                       legend=dict(orientation="h", y=1.08))
    fig4.update_yaxes(title_text="营收 (万元)", secondary_y=False)
    fig4.update_yaxes(title_text="毛利率 (%)", secondary_y=True, range=[20, 60])
    st.plotly_chart(fig4, use_container_width=True)
    
    st.markdown("#### 三年核心数据全表")
    df_summary = pd.DataFrame({
        "指标": ["营业收入", "综合成本", "毛利润", "毛利率", "客户数", "持续性收入占比", "团队规模", "人效(万/人)", "经营性现金流"],
        "第一年": ["85万", "58万", "27万", "31.7%", "2家", "0%", "6人", "14.2", "+5万"],
        "第二年": ["220万", "122万", "98万", "44.5%", "9家", "21.8%", "10人", "22.0", "+70万"],
        "第三年": ["480万", "230万", "250万", "52.1%", "28家", "38.5%", "18人", "26.7", "+185万"]
    })
    st.dataframe(df_summary, use_container_width=True, hide_index=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("#### 三年综合AI诊断")
        diag_all = {
            "维度": ["营收增长", "盈利质量", "成本效率", "收入结构", "客户生态", "可持续性"],
            "评级": ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐☆", "⭐⭐⭐⭐☆", "⭐⭐⭐⭐☆", "⭐⭐⭐⭐⭐"],
            "结论": ["三年CAGR 137.7%", "累计毛利润375万", "期间费用率↓12.9pp", "持续性收入38.5%", "2→9→28家", "经营性现金流+260万"]
        }
        st.dataframe(pd.DataFrame(diag_all), use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("#### 三年综合建议")
        st.markdown("""
        <div class="suggestion-box">
            <b>已达成</b>：商业模式验证、产品标准化、持续性收入突破、现金流转正<br><br>
            <b>下一阶段</b>：跨省复制（京津冀）、产品矩阵扩展（全流程数字孪生）、Pre-A轮融资<br><br>
            <b>核心目标</b>：第四年营收突破 <b>1000万</b>，毛利率维持 52%+，启动上市规划
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="footer-card">
        <h3 style="color:#ff7f2a; margin-top:0;">三年核心财务指标精华卡</h3>
        <div style="display:grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 1rem; margin-top: 1rem;">
            <div><b style="color:#ff7f2a;">累计营收</b><br><span style="font-size:1.8rem; font-weight:700;">785万</span></div>
            <div><b style="color:#ff7f2a;">累计毛利润</b><br><span style="font-size:1.8rem; font-weight:700;">375万</span></div>
            <div><b style="color:#ff7f2a;">平均毛利率</b><br><span style="font-size:1.8rem; font-weight:700;">42.8%</span></div>
            <div><b style="color:#ff7f2a;">投资回收期</b><br><span style="font-size:1.8rem; font-weight:700;">1.8年</span></div>
            <div><b style="color:#ff7f2a;">三年CAGR</b><br><span style="font-size:1.8rem; font-weight:700;">137.7%</span></div>
            <div><b style="color:#ff7f2a;">期末现金流</b><br><span style="font-size:1.8rem; font-weight:700;">+260万</span></div>
            <div><b style="color:#ff7f2a;">客户总数</b><br><span style="font-size:1.8rem; font-weight:700;">28家</span></div>
            <div><b style="color:#ff7f2a;">持续性收入</b><br><span style="font-size:1.8rem; font-weight:700;">38.5%</span></div>
        </div>
        <p style="margin-top:1.5rem; border-top:1px solid rgba(255,255,255,0.2); padding-top:1rem;">
            财务可行性结论：<b style="color:#ff7f2a;">极强</b> — 商业模式健康、盈利路径清晰、现金流充沛、无需外部融资即可滚动发展、具备产业化推广价值
        </p>
    </div>
    """, unsafe_allow_html=True)
