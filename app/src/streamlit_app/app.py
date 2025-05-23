"""
app.py

Front-End principal de la app.
Hecho con StreamLit, un framework simple de diseño de aplicaciones.
"""
import streamlit as st
from api_client import *

# Configuración de página y layout
st.set_page_config(page_title="Recruitment System", layout="wide")

# App principal
def main():
    st.title("📋 Recruitment System for Trainee Students")

    tab_1, tab_2 = st.tabs(["Search Candidates", "Create New Candidate"])

    # Creo primera tab de la app: donde se buscan candidatos totales, por su nombre,
    # los top-k mejores, o se imprime el reporte PDF
    with tab_1:
        st.header("Search Filters")
        col_1, col_2 = st.columns(2)
        with col_1:
            name_filter = st.text_input("Name 🧑🏻")
            degree_filter = st.text_input("Degree 📚")
        with col_2:
            college_filter = st.text_input("College 🏛️")
            col_min, col_max = st.columns(2)
            with col_min:
                min_score_filter = st.number_input("Min. Score", min_value=0.0, max_value=1.0, step=0.01)
            with col_max:
                max_score_filter = st.number_input("Max. Score", min_value=0.0, max_value=1.0, step=0.01)

        if st.button("🔍 Search"):
            candidates = get_candidates(
                name=name_filter if name_filter else None,
                college=college_filter if college_filter else None,
                degree=degree_filter if degree_filter else None,
                min_score=min_score_filter if min_score_filter else None,
                max_score=max_score_filter if max_score_filter else None,
            )
            st.dataframe(candidates, use_container_width=True)

        st.markdown("---")

        st.subheader("🔎 Search Candidate by ID")
        candidate_id = st.number_input("Candidate ID", min_value=0, step=1)
        if st.button("🔍 Search by ID"):
            candidate = get_candidate_by_id(candidate_id)
            if candidate:
                st.dataframe([candidate], use_container_width=True, height=100)

        st.markdown("---")

        st.subheader("🏆 Get Top-K Candidates")
        top_k = st.number_input("Top K", min_value=1, value=5, step=1)
        if st.button("🔍 Search Top-K"):
            top_candidates = get_top_k_candidates(top_k)
            st.dataframe(top_candidates, use_container_width=True)

        st.markdown("---")
        st.subheader("📄 Generate PDF Report for Top-K Candidates")
        top_k_report = st.number_input("Top K for Report", min_value=1, value=5, step=1)
        if st.button("Generate PDF Report"):
            generate_and_download_pdf_report(top_k_report)

    # Creo la segunda tab de la app: donde se crea un nuevo usuario para la db (csv en este caso)
    with tab_2:
        st.header("🆕 Create New Candidate")

        with st.form("create_candidate_form"):
            full_name = st.text_input("Full Name 🧑‍💼")
            email = st.text_input("Email 📧")
            degree = st.text_input("Degree 📘")
            college = st.text_input("College 🏫")
            academic_average = st.number_input("Academic Average 📊", min_value=3.0, max_value=10.0, step=0.1)
            skills = st.text_input("Skills (comma-separated) 🛠️")
            work_experience = st.text_area("Work Experience 💼", placeholder="Optional")
            submit_button = st.form_submit_button("Create Candidate")

        if submit_button:
            if not full_name or not email or not degree or not college:
                st.warning("Full Name, Email, Degree and College are required.")
            else:
                candidate_data = {
                    "full_name": full_name,
                    "email": email,
                    "college": college,
                    "degree": degree,
                    "academic_average": academic_average,
                    "skills": [s.strip() for s in skills.split(",") if s.strip()],
                    "work_experience": work_experience if work_experience else "-"
                }

                result = create_candidate(candidate_data)
                if result and result.get("message") == "success":
                    st.success("✅ Candidate created successfully!")
                    st.json(result.get("candidate"))
                else:
                    st.error("❌ Failed to create candidate")

if __name__ == "__main__":
    main()