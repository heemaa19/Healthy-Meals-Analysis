
import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ----------------------
# Page config
# ----------------------
st.set_page_config(
    page_title="Healthy Meals Dashboard",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🥗 Healthy Meals – Interactive Dashboard")
st.caption("Portfolio-ready dashboard: filters • KPIs • charts • export")

DATA_PATH = "healthy_eating_dataset_clean.csv"
if not os.path.exists(DATA_PATH):
    st.error("File 'healthy_eating_dataset_clean.csv' was not found. Please run the EDA notebook first or place the cleaned CSV alongside this app.")
    st.stop()

# ----------------------
# Load data
# ----------------------
@st.cache_data(show_spinner=False)
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Coerce numeric columns if needed
    num_cols = [
        'calories','protein_g','carbs_g','fat_g','fiber_g','sugar_g','sodium_mg',
        'cholesterol_mg','serving_size_g','prep_time_min','cook_time_min','rating','health_score','is_healthy'
    ]
    for c in df.columns:
        if c in num_cols:
            df[c] = pd.to_numeric(df[c], errors='coerce')
    return df

raw = load_data(DATA_PATH)

df = raw.copy()

# ----------------------
# Sidebar filters
# ----------------------
st.sidebar.header("Filters")

cuisines = sorted(df['cuisine'].dropna().unique().tolist()) if 'cuisine' in df.columns else []
diet_types = sorted(df['diet_type'].dropna().unique().tolist()) if 'diet_type' in df.columns else []
cooking_methods = sorted(df['cooking_method'].dropna().unique().tolist()) if 'cooking_method' in df.columns else []

sel_cuisines = st.sidebar.multiselect("Cuisine", cuisines, default=cuisines)
sel_diets = st.sidebar.multiselect("Diet Type", diet_types, default=diet_types)
sel_methods = st.sidebar.multiselect("Cooking Method", cooking_methods, default=cooking_methods)

c_min, c_max = float(df['calories'].min()), float(df['calories'].max())
min_cal, max_cal = st.sidebar.slider("Calories range", min_value=int(c_min), max_value=int(c_max), value=(int(c_min), int(c_max)), step=1)

hs_min, hs_max = (0, 100) if 'health_score' in df.columns else (0, 100)
min_hs, max_hs = st.sidebar.slider("Health Score range", min_value=int(hs_min), max_value=int(hs_max), value=(int(hs_min), int(hs_max)), step=1)

# Apply filters
mask = (
    (df['calories'].between(min_cal, max_cal)) &
    (df['health_score'].between(min_hs, max_hs) if 'health_score' in df.columns else True)
)
if cuisines:
    mask &= df['cuisine'].isin(sel_cuisines)
if diet_types:
    mask &= df['diet_type'].isin(sel_diets)
if cooking_methods:
    mask &= df['cooking_method'].isin(sel_methods)

fdf = df.loc[mask].copy()

# ----------------------
# KPIs
# ----------------------
left, mid, right, four = st.columns(4)

with left:
    st.metric("Rows (filtered)", f"{len(fdf):,}")
with mid:
    st.metric("Avg Calories", f"{fdf['calories'].mean():.1f}" if not fdf['calories'].isna().all() else "–")
with right:
    if 'is_healthy' in fdf.columns:
        st.metric("Healthy Share", f"{(fdf['is_healthy'].mean()*100):.1f}%")
    else:
        st.metric("Healthy Share", "–")
with four:
    if 'health_score' in fdf.columns:
        st.metric("Avg Health Score", f"{fdf['health_score'].mean():.1f}")
    else:
        st.metric("Avg Health Score", "–")

st.divider()

# ----------------------
# Charts
# ----------------------
chart_tab1, chart_tab2, chart_tab3, chart_tab4 = st.tabs([
    "Calories Distribution",
    "Health Score by Cuisine",
    "Healthy Ratio by Diet",
    "Calories vs Health Score"
])

with chart_tab1:
    bins = st.slider("Bins", min_value=10, max_value=100, value=40)
    fig = px.histogram(fdf, x='calories', nbins=bins, color_discrete_sequence=['#5DADE2'])
    fig.update_layout(title='Calories Distribution', xaxis_title='Calories (kcal)', yaxis_title='Count')
    st.plotly_chart(fig, use_container_width=True)

with chart_tab2:
    if 'health_score' in fdf.columns and 'cuisine' in fdf.columns:
        topN = st.slider("Top cuisines", 5, 20, 10)
        agg = (fdf.groupby('cuisine')['health_score']
                  .mean().sort_values(ascending=False).head(topN).reset_index())
        fig = px.bar(agg, x='cuisine', y='health_score', color='health_score', color_continuous_scale='Viridis')
        fig.update_layout(title=f'Average Health Score by Cuisine (Top {topN})', xaxis_title='Cuisine', yaxis_title='Avg Health Score')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Columns 'cuisine' and/or 'health_score' not available.")

with chart_tab3:
    if 'diet_type' in fdf.columns and 'is_healthy' in fdf.columns:
        agg = fdf.groupby('diet_type')['is_healthy'].mean().sort_values(ascending=False).reset_index()
        fig = px.bar(agg, x='diet_type', y='is_healthy', color='is_healthy', color_continuous_scale='Blues')
        fig.update_layout(title='Healthy Meal Ratio by Diet Type', xaxis_title='Diet Type', yaxis_title='Healthy Ratio')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Columns 'diet_type' and/or 'is_healthy' not available.")

with chart_tab4:
    if 'health_score' in fdf.columns:
        fig = px.scatter(fdf, x='calories', y='health_score', color='diet_type' if 'diet_type' in fdf.columns else None,
                         hover_data=['meal_name','cuisine','meal_type'] if 'meal_name' in fdf.columns else None,
                         trendline='ols')
        fig.update_layout(title='Calories vs Health Score', xaxis_title='Calories (kcal)', yaxis_title='Health Score')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Column 'health_score' not available.")

st.divider()

# ----------------------
# Data preview & export
# ----------------------
st.subheader("Filtered Meals")
st.dataframe(fdf.head(500), use_container_width=True)

@st.cache_data

def to_csv_bytes(df: pd.DataFrame):
    return df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download filtered data (CSV)",
    data=to_csv_bytes(fdf),
    file_name="filtered_meals.csv",
    mime="text/csv",
)

# Optional: load best model if present and show info
model_files = [f for f in os.listdir('.') if f.startswith('best_is_healthy_model_') and f.endswith('.joblib')]
if model_files:
    st.info(f"Found trained model: {model_files[0]}. You can extend this app to score new meals using the model.")
else:
    st.caption("No trained model artifact found in folder (optional).")

st.caption("© 2025 – Healthy Meals Dashboard (Yosef Reda)")
