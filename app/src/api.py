from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse

from models import StudentCandidate
from services import CandidateService
from pdf_report import PDFReportGenerator
from constants import *

app = FastAPI()
candidates_service = CandidateService(CANDIDATES_DATA_PATH, HEADER, PRESTIGE_COLLEGES, RELEVANT_SKILLS_FOR_TRAINEE_ROLE)
report_generator = PDFReportGenerator()

@app.post('/candidates/')
def create_candidate(candidate: StudentCandidate):
    """Crea nuevo candidato"""
    try:
        candidates_service.save_candidate(candidate)
        return {'message': 'success', 'candidate': candidate}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/candidates/')
def get_candidates(
        name: Optional[str] = Query(None, description="Filter by name"),
        college: Optional[str] = Query(None, description="Filter by college"),
        degree: Optional[str] = Query(None, description="Filter by degree"),
        min_score: Optional[float] = Query(None, ge=0, le=1, description="Filter by minimum score"),
        max_score: Optional[float] = Query(None, ge=0, le=1, description="Filter by maximum score")
):
    """Obtiene lista de candidatos con filtros (opcionales)"""
    candidates = candidates_service.get_all_candidates()

    if name:
        candidates = [c for c in candidates if name.lower() in c.full_name.lower()]
    if college:
        candidates = [c for c in candidates if college.lower() in c.college.lower()]
    if degree:
        candidates = [c for c in candidates if degree.lower() in c.degree.lower()]
    if min_score is not None:
        candidates = [c for c in candidates if c.score >= min_score]
    if max_score is not None:
        candidates = [c for c in candidates if c.score <= max_score]

    return {
        'total': len(candidates),
        'results': candidates
    }


@app.get('/candidates/{candidate_id}')
def get_candidate(candidate_id: int):
    """Obtiene un candidato especifico por su ID"""
    candidate = candidates_service.get_candidate_by_id(candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return {'candidate': candidate}

@app.get('/reports/')
def generate_report(k: int = Query(10, description="Top k candidates to include in report")):
    """Genera el PDF report de los top k candidatos según score de preselección"""
    try:
        preselected_candidates = candidates_service.get_preselected_candidates(k)
        pdf_path = report_generator.generate(preselected_candidates, 'report.pdf')
        return FileResponse(
            path=pdf_path,
            media_type='application/pdf',
            filename='report.pdf'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error generating report: {str(e)}')