import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="Swiggy Dashboard",
    layout="wide"
)

st.title("🍔 Swiggy Restaurant Analytics Dashboard")

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

try:
    df = pd.read_csv("swiggy_restaurants.csv")
except:
    st.error("❌ CSV file not found")
    st.stop()

# -------------------------------------------------
# CLEAN COLUMN NAMES
# -------------------------------------------------

df.columns = df.columns.str.strip().str.lower()

# -------------------------------------------------
# SHOW DATA
# -------------------------------------------------

st.subheader("📄 Dataset Preview")
st.dataframe(df.head())

st.subheader("📌 Dataset Columns")
st.write(df.columns.tolist())

# -------------------------------------------------
# AUTO DETECT IMPORTANT COLUMNS
# -------------------------------------------------

rating_col = None
cost_col = None
area_col = None

for col in df.columns:

    if "rating" in col:
        rating_col = col

    if "cost" in col:
        cost_col = col

    if "area" in col:
        area_col = col

# -------------------------------------------------
# CHECK REQUIRED COLUMNS
# -------------------------------------------------

if rating_col is None:
    st.error("❌ Rating column not found")
    st.stop()

if cost_col is None:
    st.error("❌ Cost column not found")
    st.stop()

# -------------------------------------------------
# DATA CLEANING
# -------------------------------------------------

# Convert ratings to numeric
df[rating_col] = pd.to_numeric(
    df[rating_col],
    errors="coerce"
)

# Convert cost to numeric
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
df = df.dropna(
    subset=[rating_col, cost_col]
)

# -------------------------------------------------
# METRICS
# -------------------------------------------------

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

# -------------------------------------------------
# GRAPH 1 - RATING DISTRIBUTION
# -------------------------------------------------

st.subheader("⭐ Ratings Distribution")

fig1, ax1 = plt.subplots(figsize=(8,4))

ax1.hist(df[rating_col], bins=20)

ax1.set_xlabel("Ratings")
ax1.set_ylabel("Count")

st.pyplot(fig1)

# -------------------------------------------------
# GRAPH 2 - TOP AREAS
# -------------------------------------------------

if area_col is not None:

    st.subheader("📍 Top Areas")

    top_areas = df[area_col].value_counts().head(10)

    fig2, ax2 = plt.subplots(figsize=(10,4))

    ax2.bar(
        top_areas.index,
        top_areas.values
    )

    plt.xticks(rotation=45)

    st.pyplot(fig2)

# -------------------------------------------------
# GRAPH 3 - COST VS RATING
# -------------------------------------------------

st.subheader("💰 Cost vs Rating")

fig3, ax3 = plt.subplots(figsize=(8,4))

ax3.scatter(
    df[cost_col],
    df[rating_col]
)

ax3.set_xlabel("Cost")
ax3.set_ylabel("Rating")

st.pyplot(fig3)

# -------------------------------------------------
# SUCCESS MESSAGE
# -------------------------------------------------

st.success("✅ Dashboard Loaded Successfully!")
