import streamlit as st
import requests

# Puerto default de FastAPI (si no debería traerlo de un .env)
API_URL = "http://localhost:8000"

# Helpers (para API requests)
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
        st.error(f"Error when getting candidates: {str(e)}")
        return []

def get_candidate_by_id(candidate_id: int):
    try:
        response = requests.get(f"{API_URL}/candidates/{candidate_id}")
        response.raise_for_status()
        return response.json().get("candidate")
    except requests.exceptions.RequestException as e:
        st.error(f"Error al obtener candidato por ID: {str(e)}")
        return None

def get_top_k_candidates(k: int):
    try:
        response = requests.get(f"{API_URL}/candidates/", params={"with_score": True})
        response.raise_for_status()
        all_candidates = response.json().get("candidates", [])
        sorted_candidates = sorted(all_candidates, key=lambda c: c.get("score", 0), reverse=True)
        return sorted_candidates[:k]
    except requests.exceptions.RequestException as e:
        st.error(f"Error when getting top-{k} candidatos: {str(e)}")
        return []

def create_candidate(candidate_data: dict):
    try:
        response = requests.post(f"{API_URL}/candidates/", json=candidate_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error when creating candidate: {str(e)}")
        return None

def generate_and_download_pdf_report(top_k: int):
    try:
        response = requests.get(f"{API_URL}/reports/", params={"k": top_k})
        response.raise_for_status()
        pdf_bytes = response.content

        st.download_button(
            label="Download PDF Report",
            data=pdf_bytes,
            file_name="report.pdf",
            mime="application/pdf"
        )
    except requests.exceptions.RequestException as e:
        st.error(f"Error generating PDF report: {str(e)}")