# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Swiggy Dashboard", layout="wide")

# Title
st.title("🍔 Swiggy Restaurant Analytics Dashboard")

# Load Data
df = pd.read_csv("swiggy_restaurants.csv")

# Data Cleaning
df['avg_rating'] = pd.to_numeric(df['avg_rating'], errors='coerce')

df['cost_for_two'] = (
    df['cost_for_two']
    .astype(str)
    .str.extract(r'(\d+)')[0]
    .astype(float)
)

df.dropna(subset=['avg_rating'], inplace=True)

# Sidebar Filters
st.sidebar.header("Filters")

selected_area = st.sidebar.selectbox(
    "Select Area",
    ["All"] + list(df['area'].dropna().unique())
)

if selected_area != "All":
    df = df[df['area'] == selected_area]

# Show Data
st.subheader("Dataset Preview")
st.dataframe(df.head())

# Metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total Restaurants", len(df))
col2.metric("Average Rating", round(df['avg_rating'].mean(), 2))
col3.metric("Average Cost", round(df['cost_for_two'].mean(), 2))

# Histogram
st.subheader("Distribution of Ratings")

fig, ax = plt.subplots(figsize=(8,4))
sns.histplot(df['avg_rating'], bins=20, kde=True, ax=ax)

st.pyplot(fig)

# Top Areas
st.subheader("Top Areas by Restaurant Count")

fig2, ax2 = plt.subplots(figsize=(10,4))

area_counts = df['area'].value_counts().head(10)

sns.barplot(
    x=area_counts.index,
    y=area_counts.values,
    ax=ax2
)

plt.xticks(rotation=45)

st.pyplot(fig2)

# Cost vs Rating
st.subheader("Cost vs Rating")

fig3, ax3 = plt.subplots(figsize=(8,4))

sns.scatterplot(
    x='cost_for_two',
    y='avg_rating',
    data=df,
    ax=ax3
)

st.pyplot(fig3)