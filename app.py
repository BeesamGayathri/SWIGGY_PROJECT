import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Swiggy Dashboard",
    layout="wide"
)

st.title("🍔 Swiggy Restaurant Analytics Dashboard")

# -----------------------------------
# LOAD DATA
# -----------------------------------

df = pd.read_csv("swiggy_restaurants.csv")

# Clean column names
df.columns = df.columns.str.strip().str.lower()

# Show dataset
st.subheader("Dataset Preview")
st.dataframe(df.head())

# -----------------------------------
# COLUMN DETECTION
# -----------------------------------

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

# -----------------------------------
# DATA CLEANING
# -----------------------------------

# Convert ratings to numeric
df[rating_col] = pd.to_numeric(
    df[rating_col],
    errors="coerce"
)

# Extract numbers from cost column
df[cost_col] = (
    df[cost_col]
    .astype(str)
    .str.extract(r'(\d+)')[0]
)

df[cost_col] = pd.to_numeric(
    df[cost_col],
    errors="coerce"
)

# Remove null values
df.dropna(subset=[rating_col, cost_col], inplace=True)

# -----------------------------------
# SIDEBAR FILTER
# -----------------------------------

st.sidebar.header("Filters")

if area_col:

    selected_area = st.sidebar.selectbox(
        "Select Area",
        ["All"] + list(df[area_col].dropna().unique())
    )

    if selected_area != "All":
        df = df[df[area_col] == selected_area]

# -----------------------------------
# METRICS
# -----------------------------------

st.subheader("Dashboard Metrics")

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

# -----------------------------------
# GRAPH 1 - RATINGS
# -----------------------------------

st.subheader("⭐ Rating Distribution")

fig1, ax1 = plt.subplots(figsize=(8,4))

ax1.hist(df[rating_col], bins=20)

ax1.set_xlabel("Ratings")
ax1.set_ylabel("Count")

st.pyplot(fig1)

# -----------------------------------
# GRAPH 2 - TOP AREAS
# -----------------------------------

if area_col:

    st.subheader("📍 Top Areas")

    area_counts = df[area_col].value_counts().head(10)

    fig2, ax2 = plt.subplots(figsize=(10,4))

    ax2.bar(
        area_counts.index,
        area_counts.values
    )

    plt.xticks(rotation=45)

    st.pyplot(fig2)

# -----------------------------------
# GRAPH 3 - COST VS RATING
# -----------------------------------

st.subheader("💰 Cost vs Rating")

fig3, ax3 = plt.subplots(figsize=(8,4))

ax3.scatter(
    df[cost_col],
    df[rating_col]
)

ax3.set_xlabel("Cost for Two")
ax3.set_ylabel("Rating")

st.pyplot(fig3)

# -----------------------------------
# GRAPH 4 - TOP CUISINES
# -----------------------------------

if cuisine_col:

    st.subheader("🍕 Top Cuisines")

    cuisine_counts = df[cuisine_col].value_counts().head(5)

    fig4, ax4 = plt.subplots(figsize=(6,6))

    ax4.pie(
        cuisine_counts.values,
        labels=cuisine_counts.index,
        autopct="%1.1f%%"
    )

    st.pyplot(fig4)

# -----------------------------------
# SUCCESS MESSAGE
# -----------------------------------

st.success("✅ Dashboard Loaded Successfully!")
