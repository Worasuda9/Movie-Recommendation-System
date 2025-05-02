# 🎬 Movie Recommendation System (TMDB 5000 Dataset)

A user-friendly Streamlit web application that recommends movies based on metadata such as genre, release year, and overview keywords. Built for data science group projects to demonstrate data wrangling, visualization, and simple content-based recommendation.

🚀 Features
1. 🎥 Filter movies by:
- Genre
- Year range
- Keywords in movie overviews
2. 📊 Visualize:
- Top 10 most common genres
- Number of movies released per year
3. 📦 Metadata includes:
- Title, genres, director, main actor, plot overview, vote average, runtime
4. 🖼️ Automatically fetches movie posters via TMDB API

🗂️ Dataset
1. Uses the TMDB 5000 Movies Dataset:
- tmdb_5000_movies.csv
- tmdb_5000_credits.csv
2. Merged and preprocessed to extract:
- Genres
- Director
- Main actor
- Release year (from release_date)
- Vote average and overview for ranking

🛠️ Technologies Used
- Python
- Streamlit for the web interface
- Pandas for data processing
- Matplotlib and Seaborn for visualizations
- Requests for fetching movie posters from TMDB API

📦 Installation
1. Clone the repository:
- git clone https://github.com/Worasuda9/movie-recommendation-system.git
- cd movie-recommendation-system
2. Run the app:
- streamlit run app.py

⚠️ Note: You must include a valid TMDB API key in the script (TMDB_API_KEY).

🧠 Recommendation Logic

The system filters and ranks movies based on:
- Genre match
- Overview keyword match (case-insensitive)
- Year range
- Sorted by IMDb vote average
  
📁 File Structure

.

├── app.py                 # Main Streamlit app

├── tmdb_5000_movies.csv   # Movie metadata

└── tmdb_5000_credits.csv  # Cast and crew information

👨‍💻 Authors
ITCS227 Introduction to Data Science: Group Project - Faculty of ICT, Mahidol University
