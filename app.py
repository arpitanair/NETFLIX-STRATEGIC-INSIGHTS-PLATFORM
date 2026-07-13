import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data
from utils.theme import load_css
from utils.charts import create_timeline_chart
# -------------------------
# Page Configuration
# -------------------------
import streamlit as st

st.set_page_config(
    page_title="Netflix Analytics Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(load_css(), unsafe_allow_html=True)
st.markdown("""
<style>

/* ---------- Background ---------- */

.stApp{
    background-color:#0E1117;
}

/* ---------- Sidebar ---------- */

section[data-testid="stSidebar"]{
    background:#161B22;
    border-right:2px solid #E50914;
}

/* ---------- Main ---------- */

.block-container{
    padding-top:1rem;
    padding-bottom:1rem;
    padding-left:3rem;
    padding-right:3rem;
}

/* ---------- Headers ---------- */

h1,h2,h3,h4{
    color:white;
}

p{
    color:#B8B8B8;
}

/* ---------- Metric Cards ---------- */

[data-testid="metric-container"]{

    background:#161B22;

    border-radius:15px;

    padding:18px;

    border-left:5px solid #E50914;

    box-shadow:0px 4px 15px rgba(0,0,0,0.4);

}

/* ---------- Buttons ---------- */

.stButton>button{

    background:#E50914;

    color:white;

    border:none;

    border-radius:10px;

    padding:10px 18px;

}

.stButton>button:hover{

    background:#ff3030;

}

/* ---------- Selectbox ---------- */

div[data-baseweb="select"]{

    background:#161B22;

}

/* ---------- Plotly ---------- */

.js-plotly-plot{

    border-radius:18px;

}

/* ---------- Horizontal Line ---------- */

hr{

    border:1px solid #333;

}

</style>

""", unsafe_allow_html=True)
# -------------------------
# Load Dataset
# -------------------------
df = load_data()

# -------------------------
# KPI Calculations
# -------------------------
total_titles = len(df)
total_movies = (df["type"] == "Movie").sum()
total_tv = (df["type"] == "TV Show").sum()

countries = (
    df["country"]
    .dropna()
    .str.split(",")
    .explode()
    .str.strip()
)

total_countries = countries.nunique()

genres = (
    df["listed_in"]
    .dropna()
    .str.split(",")
    .explode()
    .str.strip()
)

total_genres = genres.nunique()

# -------------------------
# Dashboard Title
# ------------------------
st.title(" NETFLIX STRATEGIC INSIGHTS PLATFORM")

st.markdown(
"""
### Decoding the DNA of Netflix's Global Content Library

This dashboard analyzes Netflix's movies and TV shows library,
covering:

-  Content growth trends
-  Country-wise distribution
-  Genre popularity
-  Movie and TV show analysis
-  Ratings and duration insights

Built using:
**Python | Pandas | Plotly | Streamlit**
"""
)

st.markdown(
"""
<div style="
background-color:#E50914;
padding:18px;
border-radius:12px;
text-align:center;
color:white;
font-size:20px;
font-weight:bold;
">
 Analyze 8,800+ Netflix Movies & TV Shows Across Countries, Genres, Ratings and Trends
</div>
""",
unsafe_allow_html=True
)

st.write("")

st.markdown("---")
st.markdown(
"""
<style>

[data-testid="metric-container"] {

    background-color: #181818;

    border: 1px solid #333333;

    padding: 20px;

    border-radius: 12px;

}


[data-testid="metric-container"] label {

    color: white;

    font-size: 18px;

}


[data-testid="metric-container"] div {

    color: #E50914;

    font-size: 35px;

    font-weight: bold;

}


</style>

""",
unsafe_allow_html=True
)
# ==========================================
# NETFLIX INSIGHT STUDIO - KPI SECTION
# ==========================================


st.markdown("---")

st.subheader("📊 Netflix Content Overview")


# Create four KPI columns
col1, col2, col3, col4 = st.columns(4)


# KPI 1 - Total Titles
with col1:

    total_titles = len(df)

    st.metric(
        label="🎬 Total Titles",
        value=f"{total_titles:,}"
    )


# KPI 2 - Movies
with col2:

    total_movies = len(
        df[df["type"] == "Movie"]
    )

    st.metric(
        label="🎥 Movies",
        value=f"{total_movies:,}"
    )


# KPI 3 - TV Shows
with col3:

    total_tv = len(
        df[df["type"] == "TV Show"]
    )

    st.metric(
        label="📺 TV Shows",
        value=f"{total_tv:,}"
    )


# KPI 4 - Countries
with col4:

    total_countries = df["country"].nunique()

    st.metric(
        label="🌎 Countries",
        value=f"{total_countries:,}"
    )


st.markdown("---")


st.sidebar.markdown("""
# 🎬 Netflix BI

### Dashboard Filters

---
""")
st.sidebar.markdown("""
---

###  Developed By

**Arpita Nair**

B.Tech CSE (Data Science and ML)

Lovely Professional University

---

NETFLIX STRATEGIC INSIGHTS PLATFORM

Version **1.0**

""")
# =====================================================
# NETFLIX CONTENT ADDED OVER TIME
# =====================================================

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<h2 style="
font-size:40px;
font-weight:bold;
margin-top:60px;
margin-bottom:20px;
">
📈 Netflix Growth Timeline
</h2>
""", unsafe_allow_html=True)
timeline = create_timeline_chart(df)

st.markdown("---")

left, right = st.columns([1.3,1])

with left:

    st.subheader("📈 Netflix Growth Timeline")

    st.plotly_chart(
        timeline,
        use_container_width=True
    )






    st.sidebar.info(
    "Netflix Content Analytics Dashboard\n\n"
    "Built using Python, Pandas, Plotly & Streamlit."
)
    st.markdown("---")




 
 
# =====================================================
# MOVIES VS TV SHOWS DONUT CHART
# =====================================================

# Create the data
type_counts = (
    df["type"]
    .value_counts()
    .reset_index()
)

# Rename columns
type_counts.columns = ["Type", "Count"]

# Create donut chart
donut = px.pie(
    type_counts,
    names="Type",
    values="Count",
    hole=0.65,
    color="Type",
    color_discrete_map={
        "Movie": "#E50914",
        "TV Show": "#564DFF"
    }
)

# Professional styling
donut.update_traces(
    textposition="inside",
    textinfo="percent+label",
    hovertemplate="<b>%{label}</b><br>Titles: %{value}<br>Percentage: %{percent}<extra></extra>"
)

donut.update_layout(
    template="plotly_dark",

    paper_bgcolor="#0F1116",
    plot_bgcolor="#0F1116",

    font=dict(
        family="Arial",
        size=15,
        color="white"
    ),

    title=dict(
        text="Movies vs TV Shows",
        x=0.5,
        font=dict(size=22)
    ),

    legend=dict(
        orientation="h",
        y=-0.15,
        x=0.25
    ),

    margin=dict(l=20, r=20, t=60, b=20),

    height=500
)
with right:

    st.subheader("🍩 Content Type")

    st.plotly_chart(
        donut,
        use_container_width=True
    )

# Business Insight
movie_pct = round(total_movies / total_titles * 100, 1)
tv_pct = round(total_tv / total_titles * 100, 1)

st.info(
    f"""
### 📊 Business Insight

🎬 Movies account for **{movie_pct}%** of Netflix's catalog.

📺 TV Shows account for **{tv_pct}%**.

Netflix's catalog is primarily movie-focused while maintaining a substantial TV show library, reflecting a strategy that balances broad movie offerings with long-form episodic content.
"""
)
    



country_df = (
    df["country"]
    .dropna()
    .str.split(",")
    .explode()
    .str.strip()
    .value_counts()
    .head(10)
    .reset_index()
)

country_df.columns = ["Country", "Titles"]
country_fig = px.bar(

    country_df,

    x="Titles",

    y="Country",

    orientation="h",

    color="Titles",

    color_continuous_scale="Reds"

)
country_fig.update_layout(

    template="plotly_dark",

    paper_bgcolor="#0F1116",
    plot_bgcolor="#0F1116",

    font=dict(
        family="Arial",
        size=15,
        color="white"
    ),

    coloraxis_showscale=False,

    yaxis=dict(categoryorder="total ascending"),

    height=500,

    margin=dict(l=20, r=20, t=60, b=20)
)


genre_df = (

    df["listed_in"]

    .dropna()

    .str.split(",")

    .explode()

    .str.strip()

    .value_counts()

    .head(10)

    .reset_index()

)

genre_df.columns = ["Genre", "Titles"]
genre_fig = px.bar(

    genre_df,

    x="Titles",

    y="Genre",

    orientation="h",

    color="Titles",

    color_continuous_scale="Sunset"

)

genre_fig.update_layout(

    template="plotly_dark",

    paper_bgcolor="#0F1116",
    plot_bgcolor="#0F1116",

    font=dict(
        family="Arial",
        size=15,
        color="white"
    ),

    coloraxis_showscale=False,

    yaxis=dict(categoryorder="total ascending"),

    height=500,

    margin=dict(l=20, r=20, t=60, b=20)

)





st.markdown("""
## 🎭 Top Genres

Explore the most popular content categories on Netflix.

""")

st.plotly_chart(
        genre_fig,
        use_container_width=True
    )

top_country = country_df.iloc[0]["Country"]
top_titles = country_df.iloc[0]["Titles"]

st.success(
    f"🌍 **Insight:** {top_country} contributes the highest number of Netflix titles with **{top_titles}** titles."
)
top_genre = genre_df.iloc[0]["Genre"]
top_genre_titles = genre_df.iloc[0]["Titles"]

st.success(
    f"🎭 **Insight:** {top_genre} is the most common Netflix genre with **{top_genre_titles}** titles."
)

country_df = (
    df["country"]
    .dropna()
    .str.split(",")
    .explode()
    .str.strip()
    .value_counts()
    .head(10)
    .reset_index()
)

country_df.columns = ["Country", "Titles"]

country_fig = px.bar(
    country_df,
    x="Titles",
    y="Country",
    orientation="h",
    color="Titles",
    color_continuous_scale="Reds"
)
country_fig.update_layout(

    template="plotly_dark",

    paper_bgcolor="#0F1116",
    plot_bgcolor="#0F1116",

    title="Top 10 Content Producing Countries",

    font=dict(
        color="white",
        size=15
    ),

    coloraxis_showscale=False,

    height=550,

    yaxis=dict(
        categoryorder="total ascending"
    )
)
country_df.columns = ["Country", "Titles"]

top_country = country_df.iloc[0]["Country"]
top_titles = country_df.iloc[0]["Titles"]


left3, right3 = st.columns([1.6, 0.7])

    

with left3:

    st.markdown("""
    ## 🌍 Top Content Producing Countries

    Discover which countries contribute the most Netflix titles.
    """)
    # Highlight KPI
    

    st.markdown("<br>", unsafe_allow_html=True)
    

    st.plotly_chart(
       country_fig,
       use_container_width=True,
       config={"displayModeBar": False}
    )
    st.info(f"""
### 🏆 Leading Country

# {top_country}

### 🎬 {top_titles:,} Titles
""")
    
with right3:

    st.markdown("## 📌 Business Insight")

    st.info(f"""
### 🇺🇸 {top_country}

Netflix's biggest production hub.

### 🎬 Titles Produced

**{top_titles:,}**

Netflix invests heavily in American productions, producing almost four times more titles than the next highest country.
""")
st.markdown("---")

st.markdown("""
# ⭐ Netflix Ratings Distribution

Understand the audience maturity level of Netflix content.
""")
rating_df = (
    df["rating"]
    .dropna()
    .value_counts()
    .head(10)
    .reset_index()
)

rating_df.columns = ["Rating", "Titles"]
rating_fig = px.bar(
    rating_df,
    x="Titles",
    y="Rating",
    orientation="h",
    color="Titles",
    color_continuous_scale="Purples"
)
rating_fig.update_layout(

    template="plotly_dark",

    paper_bgcolor="#0F1116",
    plot_bgcolor="#0F1116",

    coloraxis_showscale=False,

    height=500,

    font=dict(
        color="white",
        size=15
    ),

    title="Top Netflix Ratings",

    yaxis=dict(
        categoryorder="total ascending"
    )
)
left4, right4 = st.columns([1.6, 0.7])
with left4:

    st.markdown("""
## ⭐ Ratings Distribution

Explore how Netflix content is classified by audience maturity.
""")

    st.plotly_chart(
        rating_fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )
top_rating = rating_df.iloc[0]["Rating"]
top_rating_titles = rating_df.iloc[0]["Titles"]
with right4:

    st.markdown("## 📌 Business Insight")

    st.info(f"""
### ⭐ {top_rating}

Most common audience rating.

### 🎬 Titles

**{top_rating_titles:,}**

Netflix's catalog is dominated by **{top_rating}** content, suggesting a strong focus on serving this audience segment.
""")
color_continuous_scale=[
    "#FFE5EC",
    "#FFB3C6",
    "#FF5C8A",
    "#E50914"
]
st.markdown("---")

st.markdown("""
# 🎬 Top Directors

Discover the filmmakers with the highest number of titles on Netflix.
""")
director_df = (
    df["director"]
    .dropna()
    .str.split(",")
    .explode()
    .str.strip()
    .value_counts()
    .head(10)
    .reset_index()
)

director_df.columns = ["Director", "Titles"]
director_fig = px.bar(
    director_df,
    x="Titles",
    y="Director",
    orientation="h",
    color="Titles",
    color_continuous_scale=[
        "#FFE5EC",
        "#FFB3C6",
        "#FF5C8A",
        "#E50914"
    ]
)
director_fig.update_layout(

    template="plotly_dark",

    paper_bgcolor="#0F1116",
    plot_bgcolor="#0F1116",

    coloraxis_showscale=False,

    height=500,

    font=dict(
        color="white",
        size=15
    ),

    title="Top 10 Directors",

    yaxis=dict(
        categoryorder="total ascending"
    )
)
left5, right5 = st.columns([1.6,0.7])
with left5:

    st.markdown("""
## 🎬 Top Directors

Directors with the highest number of Netflix titles.
""")

    st.plotly_chart(
        director_fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )
top_director = director_df.iloc[0]["Director"]
top_director_titles = director_df.iloc[0]["Titles"]
with right5:

    st.markdown("## 📌 Business Insight")

    st.info(f"""
### 🎬 {top_director}

Most featured director.

### 🎥 Titles

**{top_director_titles:,}**

This director has contributed the highest number of titles to Netflix, highlighting a strong and consistent collaboration with the platform.
""")
st.markdown("---")

st.markdown("""
# ⏱ Movie Duration Analysis

Analyze how long Netflix movies typically are.
""")
movie_duration = df[df["type"] == "Movie"].copy()
movie_duration["Minutes"] = (
    movie_duration["duration"]
    .str.extract(r"(\d+)")
    .astype(float)
)

movie_duration = movie_duration.dropna(subset=["Minutes"])

movie_duration["Minutes"] = movie_duration["Minutes"].astype(int)
duration_fig = px.histogram(
    movie_duration,
    x="Minutes",
    nbins=25,
    color_discrete_sequence=["#E50914"]
)
duration_fig.update_layout(

    template="plotly_dark",

    paper_bgcolor="#0F1116",
    plot_bgcolor="#0F1116",

    title="Distribution of Movie Durations",

    font=dict(
        color="white",
        size=15
    ),

    height=500
)
left6, right6 = st.columns([1.6,0.7])
with left6:

    st.markdown("""
## ⏱ Movie Runtime Distribution

Understand how long Netflix movies usually are.
""")

    st.plotly_chart(
        duration_fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )
avg_duration = int(movie_duration["Minutes"].mean())
with right6:

    st.markdown("## 📌 Business Insight")

    st.info(f"""
### 🎬 Average Runtime

**{avg_duration} Minutes**

Most Netflix movies fall between **80–120 minutes**, indicating a preference for feature-length films that balance storytelling with viewer engagement.
""")
st.markdown("---")

st.markdown("""
# 🎭 Top Actors on Netflix

Discover which actors appear most frequently across Netflix titles.
""")
cast_df = (

    df["cast"]

    .dropna()

    .str.split(",")

    .explode()

    .str.strip()

    .value_counts()

    .head(10)

    .reset_index()

)

cast_df.columns = ["Actor", "Titles"]
cast_fig = px.bar(

    cast_df,

    x="Titles",

    y="Actor",

    orientation="h",

    color="Titles",

    color_continuous_scale=[

        "#FFE5EC",

        "#FFB3C6",

        "#FF5C8A",

        "#E50914"

    ]

)
cast_fig.update_layout(

    template="plotly_dark",

    paper_bgcolor="#0F1116",

    plot_bgcolor="#0F1116",

    coloraxis_showscale=False,

    height=500,

    font=dict(

        color="white",

        size=15

    ),

    title="Top 10 Actors",

    yaxis=dict(

        categoryorder="total ascending"

    )

)
left7, right7 = st.columns([1.6,0.7])
with left7:

    st.markdown("""

## 🎭 Most Featured Actors

Explore which actors appear in the highest number of Netflix titles.

""")

    st.plotly_chart(

        cast_fig,

        use_container_width=True,

        config={"displayModeBar": False}

    )
top_actor = cast_df.iloc[0]["Actor"]

top_actor_titles = cast_df.iloc[0]["Titles"]
with right7:

    st.markdown("## 📌 Business Insight")

    st.info(f"""

### 🎭 {top_actor}

Most featured actor.

### 🎬 Titles

**{top_actor_titles:,}**

This actor appears in more Netflix titles than any other performer in the dataset, indicating a strong and recurring presence across the platform's catalog.

""")
st.markdown("---")

st.markdown("""
# 📅 Release Year Analysis

Explore how Netflix's content library spans different release years.
""")
release_df = (
    df["release_year"]
    .value_counts()
    .sort_index()
    .reset_index()
)

release_df.columns = ["Year", "Titles"]
release_fig = px.area(
    release_df,
    x="Year",
    y="Titles",
    color_discrete_sequence=["#E50914"]
)
release_fig.update_layout(

    template="plotly_dark",

    paper_bgcolor="#0F1116",

    plot_bgcolor="#0F1116",

    height=500,

    font=dict(
        color="white",
        size=15
    ),

    title="Content Release Trend",

    xaxis_title="Release Year",

    yaxis_title="Number of Titles"
)
left8, right8 = st.columns([1.6,0.7])
with left8:

    st.markdown("""
## 📈 Release Trend

Visualize how Netflix's catalog is distributed across release years.
""")

    st.plotly_chart(
        release_fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )
peak_year = release_df.loc[
    release_df["Titles"].idxmax(),
    "Year"
]

peak_titles = release_df["Titles"].max()
with right8:

    st.markdown("## 📌 Business Insight")

    st.info(f"""
### 🚀 Peak Release Year

**{peak_year}**

### 🎬 Titles Released

**{peak_titles:,}**

Netflix's catalog is dominated by titles released around **{peak_year}**, reflecting a strong focus on contemporary content while maintaining a diverse library of older releases.
""")
oldest = df["release_year"].min()
newest = df["release_year"].max()
median = int(df["release_year"].median())

c1, c2, c3 = st.columns(3)

c1.metric("🎬 Oldest", oldest)
c2.metric("📺 Median", median)
c3.metric("🚀 Latest", newest)
st.sidebar.title("Filters")
type_filter = st.sidebar.multiselect(
    "Select Type",
    df["type"].unique(),
    default=df["type"].unique(),
    key="content_type_filter"
)

filtered_df = df[
    df["type"].isin(type_filter)
]


st.sidebar.title("Filters")

type_filter = st.sidebar.multiselect(
    "Select Type",
    df["type"].unique(),
    default=df["type"].unique()
)

filtered_df = df[
    df["type"].isin(type_filter)
]
st.info(
"""
📌 Key Findings:

• Netflix library is dominated by Movies.
• USA contributes the highest amount of content.
• Content additions increased rapidly after 2015.
• TV Shows show strong growth indicating Netflix's shift towards series-based content.
"""
)
csv = filtered_df.to_csv(index=False)

st.download_button(
    "Download Filtered Data",
    csv,
    "netflix_filtered_data.csv",
    "text/csv"
)
# ==========================================
# EXECUTIVE INSIGHTS PANEL
# ==========================================

st.markdown("---")

st.subheader("💡 Executive Insights")


st.info(
"""
🎬 Content Strategy

Netflix's library contains a larger proportion of movies
compared to TV shows, highlighting Netflix's strong investment
in movie content.


🌎 Global Expansion

Netflix has built a worldwide content ecosystem with titles
from multiple countries, showing its international reach.


📈 Growth Pattern

The Netflix content catalog expanded significantly over the years,
with rapid growth observed after 2015.


🎭 Genre Trends

Drama, International Movies, and Comedies are among the most
frequently appearing categories in Netflix's content library.


🎯 Audience Strategy

The dominance of mature ratings suggests Netflix focuses heavily
on adult-oriented entertainment while maintaining diverse content.
"""
)
# ==========================================
# NETFLIX CONTENT EXPLORER
# ==========================================

st.markdown("---")

st.subheader("🔍 Explore Netflix Library")


search_title = st.text_input(
    "Search for a Netflix title",
    placeholder="Example: Stranger Things"
)


if search_title:

    result = df[
        df["title"]
        .str.contains(
            search_title,
            case=False,
            na=False
        )
    ]


    if len(result) > 0:

        st.success(
            f"{len(result)} result(s) found"
        )


        for index, row in result.iterrows():

            st.markdown(
            f"""
            ## 🎬 {row['title']}

            **Type:** {row['type']}

            **Release Year:** {row['release_year']}

            **Rating:** {row['rating']}

            **Duration:** {row['duration']}

            **Genre:** {row['listed_in']}

            **Country:** {row['country']}

            ---
            """
            )


    else:

        st.warning(
            "No title found. Try another search."
        )
st.markdown(
"""
---
Built by Arpita Nair

CSE | Data Science & Machine Learning

Skills:
Python • Pandas • Data Visualization • Streamlit
"""
)

