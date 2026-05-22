import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page Config
st.set_page_config(
    page_title="Swiggy Restaurant Dashboard",
    layout="wide"
)

# Title
st.title("🍔 Swiggy Restaurant Analytics Dashboard")

# Load Dataset
df = pd.read_csv("swiggy_restaurants.csv")

# Show Columns for Debugging
st.subheader("Dataset Columns")
st.write(df.columns)

# Convert column names to lowercase
df.columns = df.columns.str.lower()

# Display first rows
st.subheader("Dataset Preview")
st.dataframe(df.head())

# -----------------------------
# DATA CLEANING
# -----------------------------

# Rating column handling
if 'avg_rating' in df.columns:
    rating_col = 'avg_rating'
elif 'avgrating' in df.columns:
    rating_col = 'avgrating'
else:
    st.error("Rating column not found in dataset")
    st.stop()

df[rating_col] = pd.to_numeric(df[rating_col], errors='coerce')

# Cost column handling
if 'cost_for_two' in df.columns:
    cost_col = 'cost_for_two'
elif 'costfortwo' in df.columns:
    cost_col = 'costfortwo'
else:
    st.error("Cost column not found in dataset")
    st.stop()

df[cost_col] = (
    df[cost_col]
    .astype(str)
    .str.extract(r'(\d+)')[0]
    .astype(float)
)

# Drop null ratings
df.dropna(subset=[rating_col], inplace=True)

# -----------------------------
# SIDEBAR FILTER
# -----------------------------

st.sidebar.header("Filters")

# Area Filter
if 'area' in df.columns:
    selected_area = st.sidebar.selectbox(
        "Select Area",
        ["All"] + list(df['area'].dropna().unique())
    )

    if selected_area != "All":
        df = df[df['area'] == selected_area]

# -----------------------------
# METRICS
# -----------------------------

st.subheader("Dashboard Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Restaurants", len(df))

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

st.subheader("📊 Distribution of Ratings")

fig1, ax1 = plt.subplots(figsize=(8, 4))

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

if 'area' in df.columns:

    st.subheader("📍 Top Areas by Restaurant Count")

    fig2, ax2 = plt.subplots(figsize=(10, 4))

    area_counts = df['area'].value_counts().head(10)

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

fig3, ax3 = plt.subplots(figsize=(8, 4))

sns.scatterplot(
    x=df[cost_col],
    y=df[rating_col],
    ax=ax3
)

ax3.set_xlabel("Cost for Two")
ax3.set_ylabel("Average Rating")

st.pyplot(fig3)

# -----------------------------
# PIE CHART
# -----------------------------

if 'cuisines' in df.columns:

    st.subheader("🍕 Top Cuisines")

    cuisine_counts = df['cuisines'].value_counts().head(5)

    fig4, ax4 = plt.subplots(figsize=(6, 6))

    ax4.pie(
        cuisine_counts.values,
        labels=cuisine_counts.index,
        autopct="%1.1f%%"
    )

    st.pyplot(fig4)

# -----------------------------
# SUCCESS MESSAGE
# -----------------------------

st.success("✅ Swiggy Dashboard Loaded Successfully!")
