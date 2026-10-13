# Open API Service - Discover Books with the Open Library API
# The library provides the data. Our app searches for books and displays the results.

import requests
import streamlit as st

SEARCH_URL = "https://openlibrary.org/search.json"
COVER_URL = "https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"


@st.cache_data(ttl=3600)
def search_books(query, limit):
    """Search Open Library and return matching book records."""
    response = requests.get(
        SEARCH_URL,
        params={
            "q": query,
            "limit": limit,
            "fields": "key,title,author_name,first_publish_year,cover_i",
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json().get("docs", [])


st.set_page_config(page_title="Discover Books", layout="wide")
st.title("Discover Books with Open Library")
st.caption("Arts and Advanced Big Data | Open API Service")

query = st.text_input("Search for books", "The Little Prince")
count = st.slider("How many books to show", min_value=3, max_value=12, value=6)

if query.strip():
    try:
        books = search_books(query.strip(), count)

        if not books:
            st.info("No books found. Try another title, author, or keyword.")
        else:
            cols = st.columns(3)
            for i, book in enumerate(books):
                with cols[i % 3]:
                    cover_id = book.get("cover_i")
                    if cover_id:
                        st.image(COVER_URL.format(cover_id=cover_id), width=180)
                    else:
                        st.info("No cover image available")

                    st.markdown(f"**{book.get('title') or 'Untitled'}**")
                    authors = book.get("author_name") or ["Unknown"]
                    st.write("Author:", ", ".join(authors[:3]))
                    st.write("First published:", book.get("first_publish_year") or "Unknown")

                    key = book.get("key")
                    if key:
                        st.markdown(f"[View book details](https://openlibrary.org{key})")

    except requests.RequestException:
        st.error("Could not reach Open Library right now. Please try again in a moment.")

st.caption("Data: Open Library Search API.")
