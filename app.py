import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

# -----------------------------------
# SHOW RAW DATA
# -----------------------------------

st.subheader("Raw Dataset")
st.write(df.head())

# -----------------------------------
# CLEAN DATA
# -----------------------------------

# Convert ratings
df['avg_rating'] = pd.to_numeric(
    df['avg_rating'],
    errors='coerce'
)

# Convert cost column
df['cost_for_two'] = (
    df['cost_for_two']
    .astype(str)
    .str.extract(r'(\d+)')[0]
)

df['cost_for_two'] = pd.to_numeric(
    df['cost_for_two'],
    errors='coerce'
)

# Drop nulls
df = df.dropna(
    subset=['avg_rating', 'cost_for_two']
)

# -----------------------------------
# SHOW CLEANED DATA
# -----------------------------------

st.subheader("Cleaned Dataset")
st.write(df.head())

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
    round(df['avg_rating'].mean(), 2)
)

col3.metric(
    "Average Cost",
    round(df['cost_for_two'].mean(), 2)
)

# -----------------------------------
# GRAPH 1
# -----------------------------------

st.subheader("⭐ Ratings Distribution")

fig1, ax1 = plt.subplots(figsize=(8,4))

ax1.hist(df['avg_rating'], bins=20)

ax1.set_xlabel("Ratings")
ax1.set_ylabel("Count")

st.pyplot(fig1)

# -----------------------------------
# GRAPH 2
# -----------------------------------

st.subheader("📍 Top Areas")

top_areas = df['area'].value_counts().head(10)

fig2, ax2 = plt.subplots(figsize=(10,4))

ax2.bar(
    top_areas.index,
    top_areas.values
)

plt.xticks(rotation=45)

st.pyplot(fig2)

# -----------------------------------
# GRAPH 3
# -----------------------------------

st.subheader("💰 Cost vs Rating")

fig3, ax3 = plt.subplots(figsize=(8,4))

ax3.scatter(
    df['cost_for_two'],
    df['avg_rating']
)

ax3.set_xlabel("Cost for Two")
ax3.set_ylabel("Average Rating")

st.pyplot(fig3)

# -----------------------------------
# SUCCESS
# -----------------------------------

st.success("✅ Dashboard Loaded Successfully!")
