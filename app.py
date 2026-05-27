import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config(page_title="Nkeretanyi Cooperative Fund", layout="wide")

# --- Custom CSS for Blue Outline Sidebar Buttons ---
st.markdown("""
    <style>
    /* Target only buttons inside the sidebar */
    section[data-testid="stSidebar"] .stButton button {
        border: 2px solid #3b82f6; /* Blue border matching your sketch */
        background-color: transparent;
        color: white;
        border-radius: 4px;
        height: 45px;
    }
    /* Change background to solid blue when hovering */
    section[data-testid="stSidebar"] .stButton button:hover {
        background-color: #3b82f6;
        color: white;
    }
    /* Target the text inside the button to ensure it aligns well */
    section[data-testid="stSidebar"] .stButton button p {
        font-weight: 600;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
# This acts as the app's "memory" so it knows which page to stay on
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

# ==========================================
# SIDEBAR NAVIGATION (BUTTON LAYOUT)
# ==========================================
st.sidebar.title("Navigation")

# Create the buttons. If clicked, update the session_state.page variable
if st.sidebar.button("Home", use_container_width=True):
    st.session_state.page = "Home"
if st.sidebar.button("Part 1: Main Scenario", use_container_width=True):
    st.session_state.page = "Part 1: Main Scenario"
if st.sidebar.button("Part 2: Tiered Model", use_container_width=True):
    st.session_state.page = "Part 2: Tiered Model"
if st.sidebar.button("Part 3: Diversification", use_container_width=True):
    st.session_state.page = "Part 3: Diversification (Upcoming)"
if st.sidebar.button("Part 4: Digital Integration", use_container_width=True):
    st.session_state.page = "Part 4: Digital Integration (Upcoming)"

st.sidebar.divider()

# ==========================================
# PAGE: HOME
# ==========================================
if st.session_state.page == "Home":
    st.title("Nkeretanyi Cooperative Fund")
    st.markdown("### Welcome to the Cooperative Growth Modeler")
    
    # Updated Image URL
    st.image("https://img.magnific.com/premium-photo/african-farmers-inspire-sustainable-cooperative-regenerative-agriculture_191555-9274.jpg?w=2000", use_container_width=True)
    
    st.markdown("""
    Use the navigation menu on the left to explore the financial models:
    * **Part 1: Main Scenario:** Model the long-term capital accumulation of the core group.
    * **Part 2: Tiered Model:** Compare capital generation across different contribution subgroups.
    """)

# ==========================================
# PAGE: PART 1 (MAIN SCENARIO)
# ==========================================
elif st.session_state.page == "Part 1: Main Scenario":
    st.title("Nkeretanyi Cooperative Fund")
    st.header("Part 1: Main Scenario Analysis")
    
    # --- Part 1 Specific Sidebar Controls ---
    st.sidebar.subheader("1. Core Parameters")
    group_size = st.sidebar.number_input("Group Size", min_value=1, value=20, step=1)
    monthly_contrib = st.sidebar.number_input("Monthly Contribution", min_value=0, value=100000, step=5000)
    months = st.sidebar.slider("Timeframe (Months)", min_value=12, max_value=120, value=60, step=12)

    st.sidebar.subheader("2. Reality Mechanics")
    success_rate = st.sidebar.slider("Payment Success Rate (%)", min_value=50.0, max_value=100.0, value=90.0, step=1.0)
    inflation_rate = st.sidebar.slider("Annual Inflation Rate (%)", min_value=0.0, max_value=20.0, value=3.0, step=0.5)

    st.sidebar.subheader("3. Investment Options")
    show_investment = st.sidebar.checkbox("Toggle Invested Value", value=True)
    if show_investment:
        annual_interest = st.sidebar.slider("Expected Annual Return (%)", min_value=0.0, max_value=20.0, value=5.0, step=0.5)
    else:
        annual_interest = 0.0

    # --- Part 1 Calculations ---
    effective_monthly_pool = group_size * monthly_contrib * (success_rate / 100)
    monthly_interest_rate = (annual_interest / 100) / 12

    data = []
    current_invested_value = 0

    for month in range(1, months + 1):
        raw_cumulative = effective_monthly_pool * month
        current_invested_value = (current_invested_value + effective_monthly_pool) * (1 + monthly_interest_rate)
        
        years_passed = month / 12
        discount_factor = (1 + inflation_rate / 100) ** years_passed
        
        target_value = current_invested_value if show_investment else raw_cumulative
        purchasing_power = target_value / discount_factor
        
        data.append({
            "Year": years_passed, 
            "Raw Contribution": raw_cumulative,
            "Invested Value": current_invested_value,
            "Purchasing Power": purchasing_power
        })

    df = pd.DataFrame(data)

    # --- Part 1 Summary Metrics ---
    total_years = int(months / 12)
    st.subheader(f"Total Time (years {total_years})")

    col1, col2, col3 = st.columns(3)
    color_raw = "#3b82f6"      
    color_invested = "#22c55e" 
    color_power = "#ef4444"    

    raw_val = f"{df['Raw Contribution'].iloc[-1]:,.0f}"
    inv_val = f"{df['Invested Value'].iloc[-1]:,.0f}"
    pp_val = f"{df['Purchasing Power'].iloc[-1]:,.0f}"

    col1.markdown(f"<p style='margin-bottom: 0px;'>Total Collected (Raw)</p><h1 style='color: {color_raw}; margin-top: 0px;'>{raw_val}</h1>", unsafe_allow_html=True)

    if show_investment:
        interest_gained = df['Invested Value'].iloc[-1] - df['Raw Contribution'].iloc[-1]
        col2.markdown(f"<p style='margin-bottom: 0px;'>Total with Investment</p><h1 style='color: {color_invested}; margin-top: 0px;'>{inv_val}</h1><p style='color: {color_invested};'>↑ +{interest_gained:,.0f} Interest</p>", unsafe_allow_html=True)
    else:
        col2.markdown("<p style='margin-bottom: 0px;'>Total with Investment</p><h1 style='color: gray; margin-top: 0px;'>Toggled Off</h1>", unsafe_allow_html=True)
        
    col3.markdown(f"<p style='margin-bottom: 0px;'>Real Purchasing Power</p><h1 style='color: {color_power}; margin-top: 0px;'>{pp_val}</h1>", unsafe_allow_html=True)

    st.divider()

    # --- Part 1 Line Chart ---
    st.markdown("*Tip: Click on the legend items on the right side of the chart to toggle specific lines on and off.*")
    fig_line = go.Figure()

    fig_line.add_trace(go.Scatter(x=df["Year"], y=df["Raw Contribution"], mode='lines', name='Raw Contribution', line=dict(color=color_raw, width=3)))
    if show_investment:
        fig_line.add_trace(go.Scatter(x=df["Year"], y=df["Invested Value"], mode='lines', name='Invested Value', line=dict(color=color_invested, width=3, dash='solid')))
    fig_line.add_trace(go.Scatter(x=df["Year"], y=df["Purchasing Power"], mode='lines', name='Purchasing Power', line=dict(color=color_power, width=2, dash='dot')))

    fig_line.update_layout(xaxis_title="Time (Years)", yaxis_title="Total Capital", hovermode="x unified", margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig_line, use_container_width=True)

# ==========================================
# PAGE: PART 2 (TIERED MODEL)
# ==========================================
elif st.session_state.page == "Part 2: Tiered Model":
    st.title("Nkeretanyi Cooperative Fund")
    st.header("Part 2: Tiered Model Analysis")

    # --- Part 2 Specific Sidebar Controls ---
    st.sidebar.subheader("1. Tier Parameters")
    tier_months = st.sidebar.slider("Timeframe (Months)", min_value=12, max_value=120, value=60, step=12)
    tier_success_rate = st.sidebar.slider("Payment Success Rate (%)", min_value=50.0, max_value=100.0, value=100.0, step=1.0)

    st.sidebar.subheader("2. Subgroup Definitions")
    t1_col1, t1_col2 = st.sidebar.columns(2)
    t1_people = t1_col1.number_input("Tier 1 People", min_value=0, value=5, step=1)
    t1_amount = t1_col2.number_input("Tier 1 Amount", min_value=0, value=300000, step=10000)

    t2_col1, t2_col2 = st.sidebar.columns(2)
    t2_people = t2_col1.number_input("Tier 2 People", min_value=0, value=10, step=1)
    t2_amount = t2_col2.number_input("Tier 2 Amount", min_value=0, value=200000, step=10000)

    t3_col1, t3_col2 = st.sidebar.columns(2)
    t3_people = t3_col1.number_input("Tier 3 People", min_value=0, value=5, step=1)
    t3_amount = t3_col2.number_input("Tier 3 Amount", min_value=0, value=100000, step=10000)

    # --- Part 2 Calculations ---
    t1_total = t1_people * t1_amount * tier_months * (tier_success_rate / 100)
    t2_total = t2_people * t2_amount * tier_months * (tier_success_rate / 100)
    t3_total = t3_people * t3_amount * tier_months * (tier_success_rate / 100)
    tier_grand_total = t1_total + t2_total + t3_total
    tier_years = int(tier_months / 12)

    # --- Part 2 Header & Grand Total Box ---
    col_title, col_total = st.columns([3, 1])
    with col_title:
        st.markdown(f"Comparing total projected capital for different subgroups at the end of **{tier_years} years**, factoring in the **{tier_success_rate}%** payment success rate.")
    with col_total:
        st.markdown(f"""
        <div style="background-color: #1e1e2e; padding: 15px; border-radius: 10px; border: 1px solid #8b5cf6; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <p style="margin-bottom: 0px; font-size: 14px; color: #a1a1aa;">Tier Model Grand Total</p>
            <h2 style="margin-top: 0px; color: #ffffff;">{tier_grand_total:,.0f}</h2>
        </div>
        """, unsafe_allow_html=True)

    # --- Part 2 Bar Chart ---
    t1_label = f"Tier 1<br>({t1_people} ppl @ {t1_amount:,})"
    t2_label = f"Tier 2<br>({t2_people} ppl @ {t2_amount:,})"
    t3_label = f"Tier 3<br>({t3_people} ppl @ {t3_amount:,})"

    fig_bar = go.Figure(go.Bar(
        x=[t1_total, t2_total, t3_total], y=[t1_label, t2_label, t3_label], orientation='h',
        text=[f"{t1_total:,.0f}", f"{t2_total:,.0f}", f"{t3_total:,.0f}"], textposition='auto',
        marker=dict(color=['#8b5cf6', '#ec4899', '#f59e0b']) 
    ))

    fig_bar.update_layout(xaxis_title="Total Capital Collected", yaxis_title="", margin=dict(l=0, r=0, t=30, b=0), yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig_bar, use_container_width=True)

# ==========================================
# PAGE: UPCOMING MODULES
# ==========================================
else:
    st.title("Nkeretanyi Cooperative Fund")
    st.header(st.session_state.page)
    st.info("This module is currently under development. Check back later as we expand the application!")
