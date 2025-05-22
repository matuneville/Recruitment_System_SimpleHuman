"""
services,py

Lógica principal del sistema.
Se definen las principales acciones que dan función y comportamiento al sistema.
"""

# Librerias para guardado y procesamiento de csv
import pandas as pd
import pathlib

from app.src.constants import CANDIDATES_DATA_PATH, HEADER, PRESTIGE_COLLEGES, RELEVANT_SKILLS_FOR_TRAINEE_ROLE

from models import StudentCandidate

CANDIDATES_DATA = pathlib.Path(CANDIDATES_DATA_PATH)

def save_candidate(candidate: StudentCandidate):
    data = candidate.model_dump()
    # Conveirto la lista de skills a un string con comas
    data['skills'] = ','.join(data['skills'])
    df_new_candidate = pd.DataFrame([data])

    if CANDIDATES_DATA.exists():
        # Agrega el candidato al csv (modo append)
        df_new_candidate.to_csv(CANDIDATES_DATA, mode='a', header=False, index=False)
    else:
        # Agrega al candidato creando el archivo nuevo con encabezado
        df_new_candidate.to_csv(CANDIDATES_DATA, mode='w', header=True, index=False)


def read_candidates() -> pd.DataFrame:
    if CANDIDATES_DATA.exists():
        df = pd.read_csv(CANDIDATES_DATA)
        # Convierto skills separadas por coma a lista nuevamente, siempre que no sea NaN ni sea string vacio
        df['skills'] = df['skills'].apply(lambda skills: skills.split(',') if pd.notna(skills) and skills else [])
        return df
    else:
        return pd.DataFrame(columns=HEADER)


def preselect_candidates() -> pd.DataFrame:
    df = pd.read_csv(CANDIDATES_DATA)
    df['score'] = df.apply(lambda row: calculate_score(row), axis=1)

    return df.sort_values(by=['score'], ascending=False).drop(columns='score').head(10)


def calculate_score(row):
    score = 0

    if row['academic_average'] > 7.5:
        score += 0.5
    if row['college'] in PRESTIGE_COLLEGES:
        score += 0.3
    for skill in row['skills']:
        if skill in RELEVANT_SKILLS_FOR_TRAINEE_ROLE:
            score += 0.01

    return score