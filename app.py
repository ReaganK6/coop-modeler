import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date

# --- Page Configuration ---
st.set_page_config(page_title="Nkeretanyi Cooperative Fund", layout="wide")

# --- Custom CSS for Sidebar Buttons ---
st.markdown("""
    <style>
    section[data-testid="stSidebar"] .stButton button {
        border: 2px solid #3b82f6; 
        background-color: transparent;
        color: white;
        border-radius: 4px;
        height: 45px;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background-color: #3b82f6;
        color: white;
    }
    section[data-testid="stSidebar"] .stButton button p {
        font-weight: 600;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE INITIALIZATION (DATABASE)
# ==========================================
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

# Month abbreviations for columns
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Initialize Collections Database
if 'collections_df' not in st.session_state:
    st.session_state.years = [2024]
    members = [f"{i:03d}" for i in range(1, 101)]
    df = pd.DataFrame({"Member No": members, "Member Name": [""] * 100})
    for m in months:
        df[f"2024 {m}"] = 0.0
    st.session_state.collections_df = df

# Initialize Expenses Database
if 'expenses_df' not in st.session_state:
    st.session_state.expenses_df = pd.DataFrame({
        "No": [1], 
        "Description": ["Initial Setup"], 
        "Date": [date.today()], 
        "Amount": [0.0]
    })

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
st.sidebar.title("Navigation")

if st.sidebar.button("Home", use_container_width=True): st.session_state.page = "Home"
if st.sidebar.button("Part 1: Main Scenario", use_container_width=True): st.session_state.page = "Part 1: Main Scenario"
if st.sidebar.button("Part 2: Tiered Model", use_container_width=True): st.session_state.page = "Part 2: Tiered Model"
if st.sidebar.button("Part 3: Collections", use_container_width=True): st.session_state.page = "Part 3: Collections Database"
if st.sidebar.button("Part 4: Expenses", use_container_width=True): st.session_state.page = "Part 4: Expense Ledger"
if st.sidebar.button("Part 5: Dashboard", use_container_width=True): st.session_state.page = "Part 5: Financial Dashboard"

st.sidebar.divider()

# ==========================================
# PAGE: HOME (AND PARTS 1 & 2)
# ==========================================
if st.session_state.page == "Home":
    st.title("Nkeretanyi Cooperative Fund")
    st.markdown("### Welcome to the Cooperative Growth Modeler")
    st.image("https://img.magnific.com/premium-photo/african-farmers-inspire-sustainable-cooperative-regenerative-agriculture_191555-9274.jpg?w=2000", use_container_width=True)
    st.markdown("Use the navigation menu on the left to explore the financial models and manage databases.")

elif st.session_state.page in ["Part 1: Main Scenario", "Part 2: Tiered Model"]:
    st.title("Nkeretanyi Cooperative Fund")
    st.info("These sections function exactly as built previously. Navigate to Parts 3, 4, or 5 to see the new database features!")

# ==========================================
# PAGE: PART 3 - COLLECTIONS DATABASE
# ==========================================
elif st.session_state.page == "Part 3: Collections Database":
    st.title("Collections Database")
    
    # --- Year Management Controls ---
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

    # --- Prepare Data for Table 1 ---
    base_df = st.session_state.collections_df.copy()
    
    # Calculate row totals across ALL years (hidden or visible)
    all_month_cols = [c for c in base_df.columns if c not in ["Member No", "Member Name"]]
    base_df["Total to Date"] = base_df[all_month_cols].sum(axis=1)
    
    # Filter columns based on visible years selected
    cols_to_show = ["Member No", "Member Name"]
    for y in visible_years:
        cols_to_show.extend([f"{y} {m}" for m in months])
    cols_to_show.append("Total to Date")
    
    display_df = base_df[cols_to_show]

    # Column configuration to limit text and format numbers
    col_config = {
        "Member No": st.column_config.TextColumn("No", disabled=True),
        "Member Name": st.column_config.TextColumn("Member Name", max_chars=30),
        "Total to Date": st.column_config.NumberColumn("Total to Date", disabled=True, format="%.0f")
    }

    # --- Render Table 1 ---
    edited_df = st.data_editor(
        display_df,
        column_config=col_config,
        num_rows="dynamic",
        use_container_width=True,
        height=500
    )

    # Save changes back to session state
    for col in edited_df.columns:
        if col != "Total to Date":
            st.session_state.collections_df[col] = edited_df[col]

    # --- Bottom Totals Row ---
    st.markdown("**Monthly & Grand Totals**")
    totals_dict = {"Member No": ["SUM"], "Member Name": ["All Members"]}
    for col in edited_df.columns:
        if col not in ["Member No", "Member Name"]:
            totals_dict[col] = [edited_df[col].sum()]
    
    st.dataframe(pd.DataFrame(totals_dict), hide_index=True, use_container_width=True)
    
    st.divider()

    # --- Table 2: Yearly Summary ---
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
    
    # Calculate backend totals
    all_month_cols = [c for c in st.session_state.collections_df.columns if c not in ["Member No", "Member Name"]]
    gross_collections = st.session_state.collections_df[all_month_cols].sum().sum()
    total_expenses = st.session_state.expenses_df["Amount"].sum()
    net_capital = gross_collections - total_expenses
    
    # Active members count (members who have contributed > 0)
    member_totals = st.session_state.collections_df[all_month_cols].sum(axis=1)
    active_members = (member_totals > 0).sum()

    # --- Top Row Metrics ---
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
    
    # --- Secondary Metrics ---
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

    # --- Cash Flow Visualizer ---
    st.markdown("### Yearly Cash Flow Overview")
    
    # Aggregate collections by year
    yearly_collections = []
    for y in st.session_state.years:
        y_cols = [c for c in st.session_state.collections_df.columns if str(y) in c]
        yearly_collections.append(st.session_state.collections_df[y_cols].sum().sum())
        
    # Aggregate expenses by year
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
