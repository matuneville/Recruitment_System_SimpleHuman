import streamlit as st
import requests
import os

# Configuración de página y layout
st.set_page_config(page_title="Recruitment System", layout="wide")

# Puerto default de FastAPI (si no debería traerlo de un .env)
API_URL = "http://localhost:8000"

# Helpers (para API requests)
@st.cache_data
def get_candidates(name=None, college=None, degree=None, min_score=None, max_score=None):
    params = {
        "name": name,
        "college": college,
        "degree": degree,
        "min_score": min_score,
        "max_score": max_score
    }
    try:
        response = requests.get(f"{API_URL}/candidates/", params=params)
        # print("Debug:", response.json())
        response.raise_for_status()
        return response.json().get("candidates", [])
    except requests.exceptions.RequestException as e:
        st.error(f"Error al obtener candidatos: {str(e)}")
        return []

# App principal
def main():
    st.title("📋 Recruitment System for Trainee Students")

    tab_1, tab_2 = st.tabs(["Search Candidates", "Create New Candidate"])

    with tab_1:
        st.header("🔍 Search Filters")
        col_1, col_2 = st.columns(2)
        with col_1:
            name_filter = st.text_input("Name 🧑🏻")
            degree_filter = st.text_input("Degree 📚")
        with col_2:
            college_filter = st.text_input("College 🏛️")
            col_min, col_max = st.columns(2)
            with col_min:
                min_score_filter = st.text_input("Min. Score")
            with col_max:
                max_score_filter = st.text_input("Max. Score")

        if st.button("Buscar"):
            candidates = get_candidates(
                name=name_filter if name_filter else None,
                college=college_filter if college_filter else None,
                degree=degree_filter if degree_filter else None,
                min_score=min_score_filter if min_score_filter else None,
                max_score=max_score_filter if max_score_filter else None,
            )
            st.dataframe(candidates, use_container_width=True)

if __name__ == "__main__":
    main()