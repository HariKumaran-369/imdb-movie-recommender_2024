import streamlit as st
from recommender import (
    build_recommendation_model,
    recommend_by_storyline,
    recommend_by_title,
)


DATA_PATH = "movies_final.csv"
PAGE_TITLE = "CineMatch | Movie Recommender"
PAGE_ICON = "🎬"

MATCH_HIGH_THRESHOLD = 50
MATCH_MEDIUM_THRESHOLD = 25

EXAMPLE_TITLES = ["The Manifestation", "Take Cover", "The Marriage Pass"]

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?'
    'family=Playfair+Display:wght@600;700&'
    'family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .app-header {
        padding: 2rem 0 1.5rem 0;
        border-bottom: 1px solid #E5E7EB;
        margin-bottom: 1.5rem;
    }
    .app-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.6rem;
        font-weight: 700;
        color: #1B263B;
        letter-spacing: -0.5px;
        margin-bottom: 0.2rem;
    }
    .app-title span { color: #C9A227; }
    .app-subtitle {
        font-size: 0.95rem;
        color: #6B7280;
        font-weight: 500;
        letter-spacing: 0.3px;
        text-transform: uppercase;
    }

    .stat-pill {
        background: #F8F9FA;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 0.9rem 1.2rem;
        text-align: center;
    }
    .stat-number { font-size: 1.6rem; font-weight: 700; color: #1B263B; }
    .stat-label {
        font-size: 0.75rem; color: #6B7280;
        text-transform: uppercase; letter-spacing: 0.5px;
    }

    .section-label {
        font-size: 0.78rem; font-weight: 700; color: #C9A227;
        text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.4rem;
    }
    .section-title {
        font-size: 1.4rem; font-weight: 700; color: #1B263B;
        margin-bottom: 1rem;
    }

    .example-chip {
        display: inline-block;
        font-size: 0.78rem;
        color: #1B263B;
        background: #F1F2F4;
        border-radius: 14px;
        padding: 0.2rem 0.7rem;
        margin: 0 0.3rem 0.3rem 0;
    }

    .movie-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 0.9rem;
        transition: box-shadow 0.2s ease, border-color 0.2s ease;
    }
    .movie-card:hover {
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
        border-color: #D9D9D9;
    }
    .movie-card-top {
        display: flex; justify-content: space-between;
        align-items: center; margin-bottom: 0.5rem;
    }
    .movie-rank {
        display: inline-flex; align-items: center; justify-content: center;
        width: 26px; height: 26px; border-radius: 50%;
        background: #1B263B; color: #fff;
        font-size: 0.8rem; font-weight: 700; margin-right: 0.6rem;
    }
    .movie-name { font-size: 1.05rem; font-weight: 700; color: #1C1C1C; }
    .match-badge {
        font-size: 0.78rem; font-weight: 700;
        padding: 0.25rem 0.7rem; border-radius: 20px; white-space: nowrap;
    }
    .match-high   { background: #E7F6EC; color: #1B7A3D; }
    .match-medium { background: #FCF3DC; color: #946200; }
    .match-low    { background: #FBEAEA; color: #A12C2C; }

    .progress-track {
        width: 100%; height: 6px; background: #EFEFEF;
        border-radius: 4px; margin: 0.5rem 0 0.7rem 0; overflow: hidden;
    }
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #C9A227, #E8B86D);
        border-radius: 4px;
    }
    .movie-story { font-size: 0.88rem; color: #5A5A5A; line-height: 1.55; }

    .app-footer {
        margin-top: 2rem; padding-top: 1rem;
        border-top: 1px solid #E5E7EB;
        font-size: 0.78rem; color: #9CA3AF; text-align: center;
    }

    .stButton button {
        background-color: #1B263B; color: #FFFFFF;
        border-radius: 8px; font-weight: 600;
        padding: 0.6rem 1.2rem; border: none;
    }
    .stButton button:hover { background-color: #C9A227; color: #1B263B; }

    section[data-testid="stSidebar"] {
        background-color: #F8F9FA;
        border-right: 1px solid #E5E7EB;
    }
</style>
"""


# --------------------------------------------------------------------------
# Setup helpers
# --------------------------------------------------------------------------

def configure_page() -> None:
    """Set Streamlit page-level configuration."""
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout="wide",
        initial_sidebar_state="expanded",
    )


def apply_custom_css() -> None:
    """Inject the app's custom stylesheet into the page."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


@st.cache_resource(show_spinner=False)
def load_model():
    """Load and cache the recommendation model built from the dataset."""
    return build_recommendation_model(DATA_PATH)


def get_match_class(score: float) -> str:
    """Return the CSS class name that matches a similarity score."""
    if score >= MATCH_HIGH_THRESHOLD:
        return "match-high"
    if score >= MATCH_MEDIUM_THRESHOLD:
        return "match-medium"
    return "match-low"


# --------------------------------------------------------------------------
# UI components
# --------------------------------------------------------------------------

def render_header() -> None:
    """Render the app title and subtitle."""
    st.markdown(
        """
        <div class="app-header">
            <div class="app-title">Cine<span>Match</span></div>
            <div class="app-subtitle">
                AI-Powered Movie Recommendation Engine &middot; 2024 Releases
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stats(movie_count: int) -> None:
    """Render the summary stat pills below the header."""
    stats = [
        (f"{movie_count:,}", "Movies Indexed"),
        ("TF-IDF", "NLP Engine"),
        ("Cosine", "Similarity Model"),
    ]
    for column, (value, label) in zip(st.columns(3), stats):
        with column:
            st.markdown(
                f"""
                <div class="stat-pill">
                    <div class="stat-number">{value}</div>
                    <div class="stat-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_sidebar() -> tuple[str, int]:
    """Render sidebar controls and return the selected search settings."""
    with st.sidebar:
        st.markdown(
            '<div class="section-label">Search Options</div>',
            unsafe_allow_html=True,
        )
        search_type = st.radio(
            "Search by",
            ["Movie Title", "Custom Storyline"],
            label_visibility="collapsed",
        )
        top_n = st.slider("Number of recommendations", 3, 10, 5)
        st.divider()
        st.caption(
            "Built with Selenium, TF-IDF, Cosine Similarity, and Streamlit."
        )
    return search_type, top_n


def render_title_search(df, cosine_sim, top_n: int) -> None:
    """Render the movie-title search form and handle its submission."""
    movie_input = st.text_input(
        "Movie title",
        placeholder="e.g. Kung Fu Panda , Moana 2, Civil War",
    )
    chips = "".join(
        f'<span class="example-chip">{title}</span>'
        for title in EXAMPLE_TITLES
    )
    st.markdown(chips, unsafe_allow_html=True)

    if st.button("Find Similar Movies", use_container_width=True):
        if not movie_input:
            st.warning("Please enter a movie title.")
            return
        with st.spinner("Searching catalog..."):
            results, error = recommend_by_title(
                movie_input, df, cosine_sim, top_n
            )
        if error:
            st.error(error)
        else:
            st.session_state["results"] = results
            st.session_state["search_label"] = movie_input


def render_storyline_search(df, vectorizer, tfidf_matrix, top_n: int) -> None:
    """Render the custom-storyline search form and handle its submission."""
    story_input = st.text_area(
        "Describe a storyline",
        placeholder=(
            "e.g. After Po is tapped to become the Spiritual Leader"
            "of the Valley of Peace he needs to find and train a"
        ),
        height=160,
    )

    if st.button("Find Similar Movies", use_container_width=True):
        word_count = len(story_input.split()) if story_input else 0
        if word_count < 10:
            st.warning("Please enter at least 10 words.")
            return
        with st.spinner("Analyzing storyline..."):
            results, error = recommend_by_storyline(
                story_input, df, vectorizer, tfidf_matrix, top_n
            )
        if error:
            st.error(error)
        else:
            st.session_state["results"] = results
            st.session_state["search_label"] = "your storyline"


def render_movie_card(movie: dict) -> None:
    """Render a single recommended movie as a styled card."""
    badge_class = get_match_class(movie["similarity_score"])
    st.markdown(
        f"""
        <div class="movie-card">
            <div class="movie-card-top">
                <div>
                    <span class="movie-rank">{movie['rank']}</span>
                    <span class="movie-name">{movie['movie_name']}</span>
                </div>
                <span class="match-badge {badge_class}">
                    {movie['similarity_score']}% Match
                </span>
            </div>
            <div class="progress-track">
                <div class="progress-fill"
                     style="width:{movie['similarity_score']}%;"></div>
            </div>
            <div class="movie-story">{movie['storyline']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_results() -> None:
    """Render the recommendation results panel."""
    results = st.session_state.get("results")
    if not results:
        st.info("Run a search on the left to see recommendations here.")
        return

    search_label = st.session_state.get("search_label", "")
    st.caption(f'Showing top {len(results)} matches for "{search_label}"')
    for movie in results:
        render_movie_card(movie)


def render_footer() -> None:
    """Render the closing footer."""
    st.markdown(
        '<div class="app-footer">'
        "CineMatch · Powered by Selenium, scikit-learn, and Streamlit"
        "</div>",
        unsafe_allow_html=True,
    )


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------

def main() -> None:
    """Run the CineMatch Streamlit application."""
    configure_page()
    apply_custom_css()
    render_header()

    with st.spinner("Loading recommendation engine..."):
        df, vectorizer, tfidf_matrix, cosine_sim = load_model()

    render_stats(len(df))
    st.write("")

    search_type, top_n = render_sidebar()
    search_col, results_col = st.columns([1, 1.3], gap="large")

    with search_col:
        st.markdown(
            '<div class="section-label">Step 1</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="section-title">Search</div>',
            unsafe_allow_html=True,
        )
        if search_type == "Movie Title":
            render_title_search(df, cosine_sim, top_n)
        else:
            render_storyline_search(df, vectorizer, tfidf_matrix, top_n)

    with results_col:
        st.markdown(
            '<div class="section-label">Step 2</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="section-title">Recommendations</div>',
            unsafe_allow_html=True,
        )
        render_results()

    render_footer()


if __name__ == "__main__":
    main()
