# Import Required Libraries
import streamlit as st  # Web app framework
import pandas as pd  # Data handling
import ast  # Safe evaluation of stringified Python literals
import requests  # For API calls to fetch movie posters
import matplotlib.pyplot as plt  # Plotting
import seaborn as sns  # Enhancing plots

# API Key for TMDB Poster Fetching
TMDB_API_KEY = "API_KEY" #Get API key from the report (In 7.Code appendix, the line after github link)

# Streamlit Page Configuration
st.set_page_config(page_title="Movie Recommender (TMDB 5000)", layout="wide")
st.title("🎬 Movie Recommender Based on Metadata (TMDB 5000)")
st.caption("Filter movies by genre, release year, and keyword in overview.")

# Load and Process Dataset
@st.cache_data
def load_data():
    # Load movie and credit metadata
    movies = pd.read_csv("tmdb_5000_movies.csv")
    credits = pd.read_csv("tmdb_5000_credits.csv")

    # Merge on movie title
    df = movies.merge(credits, on="title")

    # Clean and extract year from release date
    df = df[df['release_date'].notnull()]
    df['release_year'] = pd.to_datetime(df['release_date'], errors='coerce').dt.year

    # Parse genres from string to list
    def parse_genres(genre_str):
        try:
            genres = ast.literal_eval(genre_str)
            return [g['name'].lower() for g in genres]
        except:
            return []

    df['genres_list'] = df['genres'].apply(parse_genres)

    # Extract director name from crew
    def extract_director(crew_str):
        try:
            crew = ast.literal_eval(crew_str)
            for member in crew:
                if member['job'] == 'Director':
                    return member['name']
        except:
            return None

    # Extract main actor from cast
    def extract_main_actor(cast_str):
        try:
            cast = ast.literal_eval(cast_str)
            return cast[0]['name'] if cast else None
        except:
            return None

    # Add new columns for director and main actor
    df['director'] = df['crew'].apply(extract_director)
    df['main_actor'] = df['cast'].apply(extract_main_actor)

    return df

# Load the cleaned DataFrame
df = load_data()

# Visual Summary: Genre and Year Distribution
st.markdown("<h2 style='font-size:20px;'>📈 Movie Data Overview</h2>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    # Count top 10 genres
    genre_counts = pd.Series([genre for sublist in df['genres_list'] for genre in sublist]).value_counts().head(10)
    fig1, ax1 = plt.subplots(figsize=(3, 2))
    genre_counts.plot(kind='bar', ax=ax1, color='skyblue')
    ax1.set_title("Top 10 Genres", fontsize=6)
    ax1.set_xlabel("Genre", fontsize=6)
    ax1.set_ylabel("Number of Movies", fontsize=6)
    ax1.tick_params(axis='x', labelsize=6)
    ax1.tick_params(axis='y', labelsize=6)
    st.pyplot(fig1, bbox_inches='tight', use_container_width=False)

with col2:
    # Plot number of movies released per year
    movies_per_year = df['release_year'].value_counts().sort_index()
    fig2, ax2 = plt.subplots(figsize=(3, 2))
    movies_per_year.plot(kind='line', ax=ax2, color='orange')
    ax2.set_title("Movies Released Per Year", fontsize=6)
    ax2.set_ylabel("Number of Movies", fontsize=6)
    ax2.set_xlabel("Year", fontsize=6)
    ax2.tick_params(axis='x', labelsize=6)
    ax2.tick_params(axis='y', labelsize=6)
    st.pyplot(fig2, bbox_inches='tight', use_container_width=False)

# Get Poster URL from TMDB API
@st.cache_data
def get_poster_url(title):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": title}
    response = requests.get(url, params=params).json()
    try:
        poster_path = response["results"][0]["poster_path"]
        return f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
    except:
        return None

# Sidebar Filters
st.sidebar.header("🔍 Filter Options")

# Dropdown for genre selection
all_genres = sorted(set(g for sublist in df['genres_list'] for g in sublist))
selected_genre = st.sidebar.selectbox("Select Genre", options=["Any"] + all_genres)

# Slider for release year range
min_year = int(df['release_year'].min())
max_year = int(df['release_year'].max())
year_range = st.sidebar.slider("Select Year Range", min_year, max_year, (2000, 2015))

# Text input for keyword filtering
keyword = st.sidebar.text_input("Enter Keyword (from Overview)")

# Slider for number of recommended results
top_n = st.sidebar.slider("Number of Results", 5, 50, 10)

# Recommendation Logic
def recommend_movies(genre=None, year=None, keyword=None, top_n=10):
    results = df.copy()

    # Filter by genre
    if genre and genre != "Any":
        genre = genre.lower()
        results = results[results['genres_list'].apply(lambda x: genre in x)]

    # Filter by year range
    if year and isinstance(year, (tuple, list)) and len(year) == 2:
        results = results[(results['release_year'] >= year[0]) & (results['release_year'] <= year[1])]

    # Filter by keyword in overview
    if keyword:
        keyword = keyword.lower()
        results = results[results['overview'].fillna('').str.lower().str.contains(keyword)]

    # Sort by vote average
    results = results.sort_values(by='vote_average', ascending=False)
    return results.head(top_n)

# Display Recommended Movies
st.header("🎥 Recommended Movies")

# Apply filters and get results
filtered_results = recommend_movies(
    genre=selected_genre if selected_genre != "Any" else None,
    year=year_range,
    keyword=keyword,
    top_n=top_n
)

# Display movie results
if filtered_results.empty:
    st.warning("No movies found matching your criteria. Try adjusting the filters.")
else:
    for idx, row in filtered_results.iterrows():
        cols = st.columns([1, 4])

        with cols[0]:
            # Show poster if available
            poster_url = get_poster_url(row['title'])
            if poster_url:
                st.image(poster_url, width=150)
            else:
                st.write("📷 No image")

        with cols[1]:
            # Expandable section for movie details
            with st.expander(f"**{row['title']}**"):
                st.markdown(f"""
**🎬 {row['title']}**
{', '.join([g.title() for g in row['genres_list']])} • {int(row['release_year']) if pd.notna(row['release_year']) else "N/A"}

⭐ IMDb Rating: {row['vote_average']} | Runtime: {row['runtime']} minutes  
🎬 Director: {row['director']} | 🎭 Main Actor: {row['main_actor']}

**📝 Plot Summary:**  
{row['overview']}
""")
