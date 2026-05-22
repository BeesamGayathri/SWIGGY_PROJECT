import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Swiggy Dashboard",
    layout="wide"
)

st.title("🍔 Swiggy Restaurant Analytics Dashboard")

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("swiggy_restaurants.csv")

# Clean column names
df.columns = df.columns.str.strip().str.lower()

# Show dataset info
st.subheader("📄 Dataset Preview")
st.dataframe(df.head())

st.subheader("📌 Available Columns")
st.write(df.columns.tolist())

# -----------------------------
# AUTO DETECT COLUMNS
# -----------------------------

rating_col = None
cost_col = None
area_col = None
cuisine_col = None

for col in df.columns:

    if "rating" in col:
        rating_col = col

    if "cost" in col:
        cost_col = col

    if "area" in col:
        area_col = col

    if "cuisine" in col:
        cuisine_col = col

# -----------------------------
# CHECK REQUIRED COLUMNS
# -----------------------------
if rating_col is None:
    st.error("❌ No rating column found")
    st.stop()

if cost_col is None:
    st.error("❌ No cost column found")
    st.stop()

# -----------------------------
# DATA CLEANING
# -----------------------------

df[rating_col] = pd.to_numeric(
    df[rating_col],
    errors='coerce'
)

df[cost_col] = (
    df[cost_col]
    .astype(str)
    .str.extract(r'(\d+)')[0]
    .astype(float)
)

df.dropna(subset=[rating_col], inplace=True)

# -----------------------------
# SIDEBAR FILTER
# -----------------------------

st.sidebar.header("Filters")

if area_col is not None:

    selected_area = st.sidebar.selectbox(
        "Select Area",
        ["All"] + list(df[area_col].dropna().unique())
    )

    if selected_area != "All":
        df = df[df[area_col] == selected_area]

# -----------------------------
# METRICS
# -----------------------------

st.subheader("📊 Dashboard Metrics")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Restaurants",
    len(df)
)

col2.metric(
    "Average Rating",
    round(df[rating_col].mean(), 2)
)

col3.metric(
    "Average Cost",
    round(df[cost_col].mean(), 2)
)

# -----------------------------
# RATING DISTRIBUTION
# -----------------------------

st.subheader("⭐ Distribution of Ratings")

fig1, ax1 = plt.subplots(figsize=(8,4))

sns.histplot(
    df[rating_col],
    bins=20,
    kde=True,
    ax=ax1
)

st.pyplot(fig1)

# -----------------------------
# TOP AREAS
# -----------------------------

if area_col is not None:

    st.subheader("📍 Top Areas")

    fig2, ax2 = plt.subplots(figsize=(10,4))

    area_counts = df[area_col].value_counts().head(10)

    sns.barplot(
        x=area_counts.index,
        y=area_counts.values,
        ax=ax2
    )

    plt.xticks(rotation=45)

    st.pyplot(fig2)

# -----------------------------
# COST VS RATING
# -----------------------------

st.subheader("💰 Cost vs Rating")

fig3, ax3 = plt.subplots(figsize=(8,4))

sns.scatterplot(
    x=df[cost_col],
    y=df[rating_col],
    ax=ax3
)

ax3.set_xlabel("Cost")
ax3.set_ylabel("Rating")

st.pyplot(fig3)

# -----------------------------
# TOP CUISINES
# -----------------------------

if cuisine_col is not None:

    st.subheader("🍕 Top Cuisines")

    cuisine_counts = df[cuisine_col].value_counts().head(5)

    fig4, ax4 = plt.subplots(figsize=(6,6))

    ax4.pie(
        cuisine_counts.values,
        labels=cuisine_counts.index,
        autopct="%1.1f%%"
    )

    st.pyplot(fig4)

# -----------------------------
# SUCCESS
# -----------------------------

st.success("✅ Dashboard Loaded Successfully!")
