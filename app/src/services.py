"""
services,py

Lógica principal del sistema.
Se definen las principales acciones que dan función y comportamiento al sistema.

Provee clase CandidateService que encapsula los principales métodos para trabajar con la información de los candidatos.
Provee una interfaz para la operación de los candidatos.
"""
from typing import List, Optional, Dict

# Librerias para guardado y procesamiento de csv
import pandas as pd
import pathlib

# Constantes y models
# from app.src.constants import CANDIDATES_DATA_PATH, HEADER, PRESTIGE_COLLEGES, RELEVANT_SKILLS_FOR_TRAINEE_ROLE
from models import StudentCandidate


class CandidateService:
    def __init__(
            self,
            data_path: str,
            header: List[str],
            prestige_colleges: List[str],
            relevant_skills: List[str],
            preselection_weights: Optional[Dict[str, float]] = None,
    ):
        self.data_path = pathlib.Path(data_path)
        self.data_header = header
        self.prestige_colleges = prestige_colleges
        self.relevant_skills = relevant_skills
        self.preselection_weights = preselection_weights or {
            'academic_average': 0.5,
            'college': 0.3,
            'skills': 0.01
        }

    def save_candidate(self, candidate: StudentCandidate) -> None:
        """Guarda la data del candidato en el csv"""
        data = candidate.model_dump()
        data['skills'] = ','.join(data['skills'])
        df_new_candidate = pd.DataFrame([data])

        if self.data_path.exists():
            df_new_candidate.to_csv(self.data_path, mode='a', header=False, index=False)
        else:
            pd.DataFrame(self.data_header).to_csv(self.data_path, mode='w', header=False, index=False)
            df_new_candidate.to_csv(self.data_path, mode='w', header=True, index=False)

    def get_all_candidates(self, with_score: bool = True) -> pd.DataFrame:
        """Devuelve pandas dataframe de los de los candidatos"""
        if self.data_path.exists():
            df = pd.read_csv(self.data_path)
            # Convierto skills separadas por coma a lista nuevamente, siempre que no sea NaN ni sea string vacio
            df['skills'] = df['skills'].apply(lambda skills: skills.split(',') if pd.notna(skills) and skills else [])
            if with_score:
                df['score'] = df.apply(lambda row: self._calculate_score(row), axis=1)
            return df
        else:
            return pd.DataFrame(columns=self.data_header)

    def get_preselected_candidates(self, k: int = 10, with_score: bool = True) -> pd.DataFrame:
        """Devuelve pandas dataframe de los primeros k mejores candidatos ordenados descendientemente"""
        df = pd.read_csv(self.data_path)
        df['score'] = df.apply(lambda row: self._calculate_score(row), axis=1)
        sorted_df = df.sort_values(by=['score'], ascending=False)
        if not with_score:
            sorted_df = sorted_df.drop(columns=['score'])
        return sorted_df.head(k)

    def clear_all_candidates(self):
        """Elimina la informacion de los candidatos"""
        if self.data_path.exists():
            self.data_path.unlink()

    def get_candidate_by_id(self, candidate_id: int) -> StudentCandidate | None:
        """Devuelve candidato especifico por su ID (para simplificar, su ID es el índice en el dataframe,
        es deicr, el número de línea, que coincide con el momento en que fue creado).
        Como el enunciado no requiere implementar eliminiación de candidatos, no habría problemas con esta
        implementación, ya que siempre mantendrían su ID = numero de fila"""
        candidates = self.get_all_candidates()
        if candidate_id < 0 or candidate_id >= len(candidates):
            return None
        candidate_row = candidates.iloc[candidate_id]
        candidate_data = candidate_row.to_dict()
        candidate_data['skills'] = candidate_row['skills'] # ya es una lista
        return StudentCandidate(**candidate_data)

    def _calculate_score(self, row):
        """Calcula el puntaje de un candidato (row de pandas dataframe) segun las ponderaciones asignadas"""
        score = 0
        if row['academic_average'] > 7.5:
            score += self.preselection_weights['academic_average']
        if row['college'] in self.prestige_colleges:
            score += self.preselection_weights['college']
        for skill in row['skills']:
            if skill in self.relevant_skills:
                score += self.preselection_weights['skills']
        return score