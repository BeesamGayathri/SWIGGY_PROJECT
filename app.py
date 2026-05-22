import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------

st.set_page_config(
    page_title="Swiggy Dashboard",
    layout="wide"
)

st.title("🍔 Swiggy Restaurant Dashboard")

# ---------------------------------------
# LOAD CSV
# ---------------------------------------

df = pd.read_csv("swiggy_restaurants.csv")

# ---------------------------------------
# SHOW DATA
# ---------------------------------------

st.subheader("Dataset")

st.write(df.head())

# ---------------------------------------
# CLEAN COLUMN NAMES
# ---------------------------------------

df.columns = df.columns.str.lower().str.strip()

# ---------------------------------------
# PRINT COLUMNS
# ---------------------------------------

st.write("Columns:")
st.write(df.columns)

# ---------------------------------------
# USE EXACT COLUMN NAMES
# ---------------------------------------

# CHANGE THESE IF NEEDED
rating_col = df.columns[3]
cost_col = df.columns[5]
area_col = df.columns[7]

# ---------------------------------------
# CLEAN DATA
# ---------------------------------------

df[rating_col] = pd.to_numeric(
    df[rating_col],
    errors="coerce"
)

df[cost_col] = (
    df[cost_col]
    .astype(str)
    .str.extract(r'(\d+)')[0]
)

df[cost_col] = pd.to_numeric(
    df[cost_col],
    errors="coerce"
)

df = df.dropna()

# ---------------------------------------
# METRICS
# ---------------------------------------

col1, col2 = st.columns(2)

col1.metric(
    "Restaurants",
    len(df)
)

col2.metric(
    "Average Rating",
    round(df[rating_col].mean(), 2)
)

# ---------------------------------------
# GRAPH 1
# ---------------------------------------

st.subheader("Ratings Distribution")

fig1, ax1 = plt.subplots()

ax1.hist(df[rating_col], bins=20)

st.pyplot(fig1)

# ---------------------------------------
# GRAPH 2
# ---------------------------------------

st.subheader("Top Areas")

top_areas = df[area_col].value_counts().head(10)

fig2, ax2 = plt.subplots()

ax2.bar(
    top_areas.index,
    top_areas.values
)

plt.xticks(rotation=45)

st.pyplot(fig2)

# ---------------------------------------
# GRAPH 3
# ---------------------------------------

st.subheader("Cost vs Rating")

fig3, ax3 = plt.subplots()

ax3.scatter(
    df[cost_col],
    df[rating_col]
)

ax3.set_xlabel("Cost")
ax3.set_ylabel("Rating")

st.pyplot(fig3)

# ---------------------------------------
# SUCCESS
# ---------------------------------------

st.success("Dashboard Loaded Successfully!")
