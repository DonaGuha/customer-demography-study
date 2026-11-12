import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Page Configuration
st.set_page_config(
    page_title="Customer Demography Study",
    page_icon="📊",
    layout="wide"
)

# Dashboard Title
st.title("📊 Customer Demography Study")
st.markdown("### Interactive Customer Demographic Analysis Dashboard")

st.write(
    "This project analyzes customer demographics, income, "
    "spending behaviour and purchasing preferences."
)

# Load Dataset
@st.cache_data
def load_data():
    file_path = Path(__file__).parent / "customer_demographics.csv"
    return pd.read_csv(file_path)

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# Sidebar Filters
st.sidebar.header("🔍 Customer Filters")

cities = st.sidebar.multiselect(
    "Select City",
    options=sorted(df["city"].dropna().unique()),
    default=sorted(df["city"].dropna().unique())
)

genders = st.sidebar.multiselect(
    "Select Gender",
    options=sorted(df["gender"].dropna().unique()),
    default=sorted(df["gender"].dropna().unique())
)

categories = st.sidebar.multiselect(
    "Select Product Category",
    options=sorted(df["preferred_category"].dropna().unique()),
    default=sorted(df["preferred_category"].dropna().unique())
)

age_range = st.sidebar.slider(
    "Select Age Range",
    int(df["age"].min()),
    int(df["age"].max()),
    (int(df["age"].min()), int(df["age"].max()))
)

# Apply Filters
filtered_df = df[
    (df["city"].isin(cities)) &
    (df["gender"].isin(genders)) &
    (df["preferred_category"].isin(categories)) &
    (df["age"].between(age_range[0], age_range[1]))
]

if filtered_df.empty:
    st.warning("No customers found. Please change the filters.")
    st.stop()

# Customer Overview
st.subheader("📌 Customer Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", f"{len(filtered_df):,}")
col2.metric("Average Age", f"{filtered_df['age'].mean():.1f} Years")
col3.metric("Average Annual Income", f"₹{filtered_df['annual_income'].mean():,.0f}")
col4.metric("Average Spending Score", f"{filtered_df['spending_score'].mean():.1f}/100")

st.divider()

# Age and Gender Analysis
col1, col2 = st.columns(2)

with col1:
    st.subheader("👥 Age Distribution")

    fig_age = px.histogram(
        filtered_df,
        x="age",
        color="gender",
        nbins=20,
        title="Customer Age Distribution",
        labels={"age": "Customer Age"}
    )

    st.plotly_chart(fig_age, use_container_width=True)

with col2:
    st.subheader("⚧ Gender Distribution")

    gender_data = filtered_df["gender"].value_counts().reset_index()
    gender_data.columns = ["Gender", "Customers"]

    fig_gender = px.pie(
        gender_data,
        names="Gender",
        values="Customers",
        hole=0.45,
        title="Customer Gender Composition"
    )

    st.plotly_chart(fig_gender, use_container_width=True)

st.divider()

# Income Analysis
col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 Income by Profession")

    fig_income = px.box(
        filtered_df,
        x="profession",
        y="annual_income",
        color="profession",
        title="Annual Income Distribution",
        labels={
            "profession": "Profession",
            "annual_income": "Annual Income (₹)"
        }
    )

    fig_income.update_layout(
        showlegend=False,
        xaxis_tickangle=-30
    )

    st.plotly_chart(fig_income, use_container_width=True)

with col2:
    st.subheader("🛍️ Preferred Product Categories")

    category_data = filtered_df["preferred_category"].value_counts().reset_index()
    category_data.columns = ["Category", "Customers"]

    fig_category = px.bar(
        category_data,
        x="Category",
        y="Customers",
        color="Category",
        title="Customer Product Preferences"
    )

    fig_category.update_layout(
        showlegend=False,
        xaxis_tickangle=-25
    )

    st.plotly_chart(fig_category, use_container_width=True)

st.divider()

# Income vs Spending Score
st.subheader("📈 Income vs Spending Score")

fig_scatter = px.scatter(
    filtered_df,
    x="annual_income",
    y="spending_score",
    color="gender",
    size="purchase_frequency",
    hover_data=["customer_id", "age", "city"],
    title="Customer Income and Spending Behaviour",
    labels={
        "annual_income": "Annual Income (₹)",
        "spending_score": "Spending Score"
    }
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()

# Customer Dataset
st.subheader("📋 Customer Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

# Download Filtered Dataset
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Customer Data",
    data=csv_data,
    file_name="filtered_customer_demographics.csv",
    mime="text/csv"
)

# Footer
st.divider()

st.markdown("""
**Customer Demography Study**

Data Analytics Internship Project

Technologies: Python | Pandas | Streamlit | Plotly

Dataset: Synthetic data created for educational purposes.
""")