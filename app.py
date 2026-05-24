import streamlit as st

st.set_page_config(page_title="Swiggy Data Analysis Dashboard", layout="wide")

st.title("📊 Swiggy Data Analysis Dashboard")

st.markdown("Interactive Power BI Dashboard")

powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiMzZiNzhkODUtNWZjZi00N2NjLWIwYjEtOWI4Yzk5NzlhYjVlIiwidCI6ImZmYzMxNjU1LTI0NTMtNGMzNy1iNmM3LWI4MzQ2ODM4MTc3NiJ9"

st.components.v1.iframe(powerbi_url, height=700, scrolling=True)
