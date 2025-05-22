from app.src.models import StudentCandidate
from app.src.services import CandidateService
from constants import *
from pdf_report import PDFReportGenerator

if __name__ == "__main__":
    candidatos = [
        StudentCandidate(
            full_name="Ana Gómez",
            email="ana@example.com",
            college="Universidad de Buenos Aires",
            degree="Data Science",
            academic_average=9.1,
            skills=["Python", "Rust", "Java"],
            work_experience="Internship at XYZ, 2022 - 2024"
        ),
        StudentCandidate(
            full_name="Luis Fernández",
            email="luisf@example.com",
            college="Stanford University",
            degree="Computer Science",
            academic_average=5,
            skills=["Python", "SQL", "Docker"],
        ),
        StudentCandidate(
            full_name="María Pérez",
            email="maria.p@example.com",
            college="UNAM",
            degree="Software Engineering",
            academic_average=6.3,
            skills=["Java"],
            work_experience="Volunteer projects"
        ),
        StudentCandidate(
            full_name="Carlos Ruiz",
            email="carlos.ruiz@example.com",
            college="Harvard University",
            degree="Information Systems",
            academic_average=9.5,
            skills=["AWS"],
            work_experience="Research assistant"
        ),
        StudentCandidate(
            full_name="Sofía Martínez",
            email="sofia.m@example.com",
            college="Massachusetts Institute of Technology",
            degree="Computer Science",
            academic_average=6.8,
            skills=["C++", "Python", "SQL"],
            work_experience="Summer internship"
        ),
    ]

    candidate_service = CandidateService(CANDIDATES_DATA_PATH, HEADER, PRESTIGE_COLLEGES, RELEVANT_SKILLS_FOR_TRAINEE_ROLE)

    candidate_service.clear_all_candidates()

    for candidato in candidatos:
        candidate_service.save_candidate(candidato)

    print("Todos los candidatos:")
    print(candidate_service.get_all_candidates())

    print("\nTop 10 candidatos preseleccionados:")
    print(candidate_service.get_preselected_candidates(with_score=False))
    preselected = candidate_service.get_preselected_candidates(with_score=True)

    PDFReportGenerator().generate(preselected)