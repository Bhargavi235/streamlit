import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Music Insights Dashboard",
    layout="wide"
)

# With caching, the dataset is loaded only once, making the application much faster.
@st.cache_data
def load_data():
    df = pd.read_csv("dataset.csv")
    return df


df = load_data()

st.sidebar.title("Navigation")
page = st.sidebar.radio(

    "Go To",
    [
        "Home",
        "Data Explorer",
        "Visualizations",
       
    ]
)
if page == "Home":

    st.title("Music Insights Dashboard")
    st.write(

        """
        Welcome to the Music Insights Dashboard.

        This application analyzes Spotify songs
        and provides interactive visualizations,
        filtering options,
        and popularity prediction.

        """
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Songs",
            len(df)
        )

    with col2:
        st.metric(
            "Average Popularity",
            round(df["popularity"].mean(), 2)
        )

    with col3:

        st.metric(
            "Average Danceability",
            round(df["danceability"].mean(), 2)
        )


    with col4:
        st.metric(
            "Average Energy",
            round(df["energy"].mean(), 2)
        )

    st.subheader("Dataset Preview")
    st.dataframe(
        df.sample(10),
        use_container_width=True
    )

elif page == "Data Explorer":

    st.title(" Data Explorer")
    st.write(
        """
        Filter Spotify songs based on different
        music characteristics.
        """
    )

    genres = sorted(df["track_genre"].unique())
    genres.insert(0, "All Genres")
    selected_genre = st.selectbox(
        "Select Genre",
        genres
    )

    artist_name = st.text_input(
        "Artist Name (optional)"
    )
    
    popularity = st.slider(
        "Minimum Popularity",
        min_value=0,
        max_value=100,
        value=50
    )

    explicit_only = st.checkbox(
        "Show Only Explicit Songs"
    )

    filtered_df = df.copy()
    if selected_genre != "All Genres":
        filtered_df = filtered_df[
            filtered_df["track_genre"] == selected_genre
        ]
    if artist_name:
        filtered_df = filtered_df[
            filtered_df["artists"]
            .str.contains(
                artist_name,
                case=False,
                na=False
            )
        ]

    filtered_df = filtered_df[
        filtered_df["popularity"] >= popularity
    ]


    if explicit_only:
        filtered_df = filtered_df[
            filtered_df["explicit"] == True
        ]

    st.subheader("Filtered Songs")
    st.success(
        f"{len(filtered_df)} songs found."
    )

    st.dataframe(
        filtered_df,
        use_container_width=True
    )
    
elif page == "Visualizations":

    st.title("Music Visualizations")
    st.write(
        """
        Interactive visualizations of the Spotify dataset.
        """
    )
    st.subheader("Genre Distribution")
    genre_count = (
        df["track_genre"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    genre_count.columns = ["Genre", "Count"]

    fig = px.pie(

        genre_count,

        names="Genre",

        values="Count",

        title="Top 10 Genres"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.subheader("Average Popularity by Genre")
    popularity_genre = (
        df.groupby("track_genre")["popularity"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        popularity_genre,
        x="track_genre",
        y="popularity",
        color="popularity",
        title="Top Genres by Average Popularity"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Danceability vs Popularity")
    sample = df.sample(1500)
    fig = px.scatter(
        sample,
        x="danceability",
        y="popularity",
        color="track_genre",
        hover_data=["track_name"]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Energy vs Popularity")
    fig = px.scatter(
        sample,
        x="energy",
        y="popularity",
        color="track_genre",
        hover_data=["track_name"]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Popularity Distribution")
    fig = px.histogram(
        df,
        x="popularity",
        nbins=30,
        title="Popularity Score Distribution"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )