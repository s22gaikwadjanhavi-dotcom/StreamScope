import streamlit as st
import pandas as pd
import plotly.express as px







# ---------------- CONFIG ----------------
st.set_page_config(page_title="Netflix Dashboard", layout="wide")

st.title("🎬 Netflix Interactive Dashboard")
st.markdown("### Analysis & Dynamic Insights")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("netflix_milestone2_final_dataset.csv")

# ---------------- SIDEBAR ----------------
st.sidebar.title("🎯 Filters")

year = st.sidebar.multiselect("Year", sorted(df['year_added'].dropna().unique()))
country = st.sidebar.multiselect("Country", sorted(df['country'].dropna().unique()))
content_type = st.sidebar.multiselect("Type", df['type'].unique())

df['listed_in'] = df['listed_in'].fillna("")
genres = sorted(set(g.strip() for sublist in df['listed_in'].str.split(',') for g in sublist))
genre = st.sidebar.multiselect("Genre", genres)

# ---------------- FILTER ----------------
filtered_df = df.copy()

if year:
    filtered_df = filtered_df[filtered_df['year_added'].isin(year)]
if country:
    filtered_df = filtered_df[filtered_df['country'].isin(country)]
if content_type:
    filtered_df = filtered_df[filtered_df['type'].isin(content_type)]
if genre:
    filtered_df = filtered_df[
        filtered_df['listed_in'].str.contains('|'.join(genre))
    ]

# ---------------- KPI ----------------
st.subheader("📊 Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Titles", len(filtered_df))
col2.metric("Movies", (filtered_df['type'] == 'Movie').sum())
col3.metric("TV Shows", (filtered_df['type'] == 'TV Show').sum())
col4.metric("Countries", filtered_df['country'].nunique())

# ---------------- ROW 1 ----------------
col1, col2 = st.columns(2)

# 🎯 Pie Chart (Hover enabled)
with col1:
    type_counts = filtered_df['type'].value_counts().reset_index()
    type_counts.columns = ['Type', 'Count']

    fig = px.pie(
        type_counts,
        names='Type',
        values='Count',
        title="Content Type Distribution",
        hole=0.4
    )
    st.plotly_chart(fig, width='stretch')

# 🎯 Rating Chart (Hover enabled)
with col2:
    rating_counts = filtered_df['rating'].value_counts().head(10).reset_index()
    rating_counts.columns = ['Rating', 'Count']

    fig = px.bar(
        rating_counts,
        x='Rating',
        y='Count',
        title="Top Ratings",
        text='Count'
    )
    st.plotly_chart(fig, width='stretch')

# ---------------- YEAR TREND ----------------
st.subheader("📈 Content Growth Over Time")

year_data = filtered_df['year_added'].value_counts().sort_index().reset_index()
year_data.columns = ['Year', 'Count']

fig = px.line(
    year_data,
    x='Year',
    y='Count',
    markers=True,
    title="Year-wise Content Growth"
)
st.plotly_chart(fig, width='stretch')

# ---------------- ROW 3 ----------------
col1, col2 = st.columns(2)

# 🎭 Genres
with col1:
    genre_df = filtered_df.copy()
    genre_df['listed_in'] = genre_df['listed_in'].str.split(',')
    genre_df = genre_df.explode('listed_in')
    genre_df['listed_in'] = genre_df['listed_in'].str.strip()

    top_genres = genre_df['listed_in'].value_counts().head(10).reset_index()
    top_genres.columns = ['Genre', 'Count']

    fig = px.bar(
        top_genres,
        x='Count',
        y='Genre',
        orientation='h',
        title="Top Genres"
    )
    st.plotly_chart(fig, width='stretch')

# 🌍 Countries
with col2:
    top_countries = filtered_df['country'].value_counts().head(10).reset_index()
    top_countries.columns = ['Country', 'Count']

    fig = px.bar(
        top_countries,
        x='Count',
        y='Country',
        orientation='h',
        title="Top Countries"
    )
    st.plotly_chart(fig, width='stretch')

# ---------------- DATA ----------------
with st.expander("📂 View Data"):
    st.dataframe(filtered_df)