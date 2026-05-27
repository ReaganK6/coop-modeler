import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date
import random

# --- Page Configuration ---
st.set_page_config(page_title="Nkeretanyi Cooperative Fund", layout="wide")

# --- Custom CSS for Sidebar Buttons ---
st.markdown("""
    <style>
    section[data-testid="stSidebar"] .stButton button p {
        font-weight: 600;
        font-size: 16px;
    }
    section[data-testid="stSidebar"] .stButton button[kind="secondary"] {
        border: 2px solid #3b82f6; 
        background-color: transparent;
        color: white;
        border-radius: 4px;
        height: 45px;
    }
    section[data-testid="stSidebar"] .stButton button[kind="secondary"]:hover {
        background-color: rgba(59, 130, 246, 0.2);
        color: white;
    }
    section[data-testid="stSidebar"] .stButton button[kind="primary"] {
        border: 2px solid #3b82f6; 
        background-color: #3b82f6;
        color: white;
        border-radius: 4px;
        height: 45px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE INITIALIZATION (DATABASE)
# ==========================================
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Initialize Collections Database with Fake Data
if 'collections_df' not in st.session_state:
    # Set years up to 2026
    st.session_state.years = [2024, 2025, 2026]
    
    # Generate 100 members, but give the first 10 fake names
    members = [f"{i:03d}" for i in range(1, 101)]
    fake_names = ["Kagabo Jean", "Mukamana Alice", "Bizimana Eric", "Uwera Sarah", "Habimana Paul",
                  "Gatete Patrick", "Umutoni Grace", "Nshuti David", "Kamikazi Diane", "Rukundo Yves"]
    names = fake_names + [""] * 90 
    
    df = pd.DataFrame({"Member No": members, "Member Name": names})
    
    # Fake contribution options
    amounts = [0, 50000, 100000, 100000, 150000, 200000, 300000] 
    
    for y in st.session_state.years:
        for m in months:
            col_name = f"{y} {m}"
            # Stop generating data after May 2026
            if y == 2026 and months.index(m) > 4: 
                df[col_name] = 0.0
            else:
                col_data = []
                for i in range(100):
                    if i < 10: # Only assign money to our 10 fake members
                        col_data.append(float(random.choice(amounts)))
                    else:
                        col_data.append(0.0)
                df[col_name] = col_data
                
    st.session_state.collections_df = df

# Initialize Expenses Database with Fake Data
if 'expenses_df' not in st.session_state:
    st.session_state.expenses_df = pd.DataFrame({
        "No": [1, 2, 3, 4], 
        "Description": ["Initial Legal Setup", "Bank Account Fees 2024", "Annual General Meeting", "Agri-Equipment Lease Deposit"], 
        "Date": [date(2024, 1, 15), date(2024, 12, 30), date(2025, 6, 10), date(2026, 3, 5)], 
        "Amount": [150000.0, 25000.0, 300000.0, 1200000.0]
    })

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
st.sidebar.title("Navigation")

def get_btn_type(page_name):
    return "primary" if st.session_state.page == page_name else "secondary"

if st.sidebar.button("Home", use_container_width=True, type=get_btn_type("Home")): 
    st.session_state.page = "Home"
    st.rerun()
if st.sidebar.button("Part 1: Main Scenario", use_container_width=True, type=get_btn_type("Part 1: Main Scenario")): 
    st.session_state.page = "Part 1: Main Scenario"
    st.rerun()
if st.sidebar.button("Part 2: Tiered Model", use_container_width=True, type=get_btn_type("Part 2: Tiered Model")): 
    st.session_state.page = "Part 2: Tiered Model"
    st.rerun()
if st.sidebar.button("Part 3: Collections", use_container_width=True, type=get_btn_type("Part 3: Collections Database")): 
    st.session_state.page = "Part 3: Collections Database"
    st.rerun()
if st.sidebar.button("Part 4: Expenses", use_container_width=True, type=get_btn_type("Part 4: Expense Ledger")): 
    st.session_state.page = "Part 4: Expense Ledger"
    st.rerun()
if st.sidebar.button("Part 5: Dashboard", use_container_width=True, type=get_btn_type("Part 5: Financial Dashboard")): 
    st.session_state.page = "Part 5: Financial Dashboard"
    st.rerun()

st.sidebar.divider()

# ==========================================
# PAGE: HOME
# ==========================================
if st.session_state.page == "Home":
    st.title("Nkeretanyi Cooperative Fund")
    st.markdown("### Welcome to the Cooperative Growth Modeler")
    st.image("https://img.magnific.com/premium-photo/african-farmers-inspire-sustainable-cooperative-regenerative-agriculture_191555-9274.jpg?w=2000", use_container_width=True)
    st.markdown("""
    Use the navigation menu on the left to explore the financial models and manage databases:
    * **Parts 1 & 2:** Predictive modeling and scenario planning.
    * **Parts 3 & 4:** Active data entry for collections and expenses.
    * **Part 5:** Live executive dashboard tracking actual funds.
    """)

# ==========================================
# PAGE: PART 1 (MAIN SCENARIO)
# ==========================================
elif st.session_state.page == "Part 1: Main Scenario":
    st.title("Nkeretanyi Cooperative Fund")
    st.header("Part 1: Main Scenario Analysis")
    
    st.sidebar.subheader("1. Core Parameters")
    group_size = st.sidebar.number_input("Group Size", min_value=1, value=20, step=1)
    monthly_contrib = st.sidebar.number_input("Monthly Contribution", min_value=0, value=100000, step=5000)
    months_slider = st.sidebar.slider("Timeframe (Months)", min_value=12, max_value=120, value=60, step=12)

    st.sidebar.subheader("2. Reality Mechanics")
    success_rate = st.sidebar.slider("Payment Success Rate (%)", min_value=50.0, max_value=100.0, value=90.0, step=1.0)
    inflation_rate = st.sidebar.slider("Annual Inflation Rate (%)", min_value=0.0, max_value=20.0, value=3.0, step=0.5)

    st.sidebar.subheader("3. Investment Options")
    show_investment = st.sidebar.checkbox("Toggle Invested Value", value=True)
    if show_investment:
        annual_interest = st.sidebar.slider("Expected Annual Return (%)", min_value=0.0, max_value=20.0, value=5.0, step=0.5)
    else:
        annual_interest = 0.0

    effective_monthly_pool = group_size * monthly_contrib * (success_rate / 100)
    monthly_interest_rate = (annual_interest / 100) / 12

    data = []
    current_invested_value = 0

    for month in range(1, months_slider + 1):
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

    total_years = int(months_slider / 12)
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

    t1_total = t1_people * t1_amount * tier_months * (tier_success_rate / 100)
    t2_total = t2_people * t2_amount * tier_months * (tier_success_rate / 100)
    t3_total = t3_people * t3_amount * tier_months * (tier_success_rate / 100)
    tier_grand_total = t1_total + t2_total + t3_total
    tier_years = int(tier_months / 12)

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
# PAGE: PART 3 - COLLECTIONS DATABASE
# ==========================================
elif st.session_state.page == "Part 3: Collections Database":
    st.title("Collections Database")
    
    st.markdown("### Table 1: Master Collections Log")
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("➕ Add Next Year", use_container_width=True):
            next_year = max(st.session_state.years) + 1
            st.session_state.years.append(next_year)
            for m in months:
                st.session_state.collections_df[f"{next_year} {m}"] = 0.0
            st.rerun()
    with col2:
        year_to_remove = st.selectbox("Remove Year", ["Select"] + st.session_state.years, label_visibility="collapsed")
        if year_to_remove != "Select" and st.button("🗑️ Delete Selected", use_container_width=True):
            st.session_state.years.remove(year_to_remove)
            cols_to_drop = [c for c in st.session_state.collections_df.columns if str(year_to_remove) in c]
            st.session_state.collections_df.drop(columns=cols_to_drop, inplace=True)
            st.rerun()
    with col3:
        visible_years = st.multiselect("Visible Years (Hide/Unhide Months):", st.session_state.years, default=st.session_state.years)

    base_df = st.session_state.collections_df.copy()
    all_month_cols = [c for c in base_df.columns if c not in ["Member No", "Member Name"]]
    base_df["Total to Date"] = base_df[all_month_cols].sum(axis=1)
    
    cols_to_show = ["Member No", "Member Name"]
    for y in visible_years:
        cols_to_show.extend([f"{y} {m}" for m in months])
    cols_to_show.append("Total to Date")
    
    display_df = base_df[cols_to_show]

    col_config = {
        "Member No": st.column_config.TextColumn("No", disabled=True),
        "Member Name": st.column_config.TextColumn("Member Name", max_chars=30),
        "Total to Date": st.column_config.NumberColumn("Total to Date", disabled=True, format="%.0f")
    }

    edited_df = st.data_editor(
        display_df,
        column_config=col_config,
        num_rows="dynamic",
        use_container_width=True,
        height=500
    )

    for col in edited_df.columns:
        if col != "Total to Date":
            st.session_state.collections_df[col] = edited_df[col]

    st.markdown("**Monthly & Grand Totals**")
    totals_dict = {"Member No": ["SUM"], "Member Name": ["All Members"]}
    for col in edited_df.columns:
        if col not in ["Member No", "Member Name"]:
            totals_dict[col] = [edited_df[col].sum()]
    
    st.dataframe(pd.DataFrame(totals_dict), hide_index=True, use_container_width=True)
    
    st.divider()

    st.markdown("### Table 2: Yearly Summary & Share")
    summary_df = pd.DataFrame()
    summary_df["Member No"] = st.session_state.collections_df["Member No"]
    summary_df["Member Name"] = st.session_state.collections_df["Member Name"]
    
    for y in st.session_state.years:
        y_cols = [c for c in st.session_state.collections_df.columns if str(y) in c]
        summary_df[f"{y} Total"] = st.session_state.collections_df[y_cols].sum(axis=1)
        
    summary_df["Grand Total"] = summary_df[[f"{y} Total" for y in st.session_state.years]].sum(axis=1)
    
    total_fund_pool = summary_df["Grand Total"].sum()
    if total_fund_pool > 0:
        summary_df["% Share"] = (summary_df["Grand Total"] / total_fund_pool * 100).round(2)
    else:
        summary_df["% Share"] = 0.0

    st.dataframe(
        summary_df, 
        use_container_width=True,
        column_config={"% Share": st.column_config.NumberColumn("% Share", format="%.2f %%")}
    )

# ==========================================
# PAGE: PART 4 - EXPENSE LEDGER
# ==========================================
elif st.session_state.page == "Part 4: Expense Ledger":
    st.title("Expense Ledger")
    st.markdown("Track all operational expenditures and disbursements.")
    
    edited_expenses = st.data_editor(
        st.session_state.expenses_df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "No": st.column_config.NumberColumn("Ref No.", step=1),
            "Date": st.column_config.DateColumn("Date"),
            "Amount": st.column_config.NumberColumn("Amount", format="%.0f")
        }
    )
    
    st.session_state.expenses_df = edited_expenses
    
    total_expenses = edited_expenses["Amount"].sum()
    st.markdown(f"### Total Disbursed: **{total_expenses:,.0f}**")

# ==========================================
# PAGE: PART 5 - FINANCIAL DASHBOARD
# ==========================================
elif st.session_state.page == "Part 5: Financial Dashboard":
    st.title("Executive Dashboard")
    st.markdown("Live operational status of the Nkeretanyi Cooperative Fund.")
    
    all_month_cols = [c for c in st.session_state.collections_df.columns if c not in ["Member No", "Member Name"]]
    gross_collections = st.session_state.collections_df[all_month_cols].sum().sum()
    total_expenses = st.session_state.expenses_df["Amount"].sum()
    net_capital = gross_collections - total_expenses
    
    member_totals = st.session_state.collections_df[all_month_cols].sum(axis=1)
    active_members = (member_totals > 0).sum()

    col1, col2, col3 = st.columns(3)
    
    col1.markdown(f"""
    <div style="background-color: #1e1e2e; padding: 20px; border-radius: 8px; border-top: 4px solid #3b82f6;">
        <p style="color: #a1a1aa; margin: 0;">Gross Capital Pool (Collected)</p>
        <h2 style="color: white; margin: 0;">{gross_collections:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col2.markdown(f"""
    <div style="background-color: #1e1e2e; padding: 20px; border-radius: 8px; border-top: 4px solid #ef4444;">
        <p style="color: #a1a1aa; margin: 0;">Operational Expenditures</p>
        <h2 style="color: white; margin: 0;">{total_expenses:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col3.markdown(f"""
    <div style="background-color: #1e1e2e; padding: 20px; border-radius: 8px; border-top: 4px solid #22c55e;">
        <p style="color: #a1a1aa; margin: 0;">Net Available Capital (In Pot)</p>
        <h2 style="color: white; margin: 0;">{net_capital:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")
    
    col4, col5 = st.columns(2)
    with col4:
        st.metric("Active Contributing Members", f"{active_members} / 100")
    with col5:
        if gross_collections > 0:
            expense_ratio = (total_expenses / gross_collections) * 100
        else:
            expense_ratio = 0.0
        st.metric("Capital Utilization (Burn Rate)", f"{expense_ratio:.1f}%")

    st.divider()

    st.markdown("### Yearly Cash Flow Overview")
    
    yearly_collections = []
    for y in st.session_state.years:
        y_cols = [c for c in st.session_state.collections_df.columns if str(y) in c]
        yearly_collections.append(st.session_state.collections_df[y_cols].sum().sum())
        
    expenses_df = st.session_state.expenses_df.copy()
    expenses_df["Date"] = pd.to_datetime(expenses_df["Date"])
    yearly_expenses = []
    for y in st.session_state.years:
        year_exp = expenses_df[expenses_df["Date"].dt.year == y]["Amount"].sum()
        yearly_expenses.append(year_exp)
        
    fig = go.Figure()
    fig.add_trace(go.Bar(x=st.session_state.years, y=yearly_collections, name='Collected', marker_color='#3b82f6'))
    fig.add_trace(go.Bar(x=st.session_state.years, y=yearly_expenses, name='Disbursed', marker_color='#ef4444'))

    fig.update_layout(
        barmode='group',
        xaxis_title="Year",
        yaxis_title="Amount",
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis=dict(tickmode='array', tickvals=st.session_state.years)
    )
    
    st.plotly_chart(fig, use_container_width=True)
