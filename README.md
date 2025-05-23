# Recruitment System: SimpleHuman

Sistema simple de reclutamiento de candidatos estudiantes que permite visualizar y generar reportes. El sistema incluye una API desarrollada con FastAPI y una interfaz interactiva construida con Streamlit que permite operar con el sistema y visualizar la información.

## Características
- Interfaz principal del sistema proveída por `CandidateService`
- Guardado de información de candidatos desde un archivo CSV (`app/data/candidates.csv` cuando se genera por primera vez).
- API RESTful para comunicación entre componentes.
- Interfaz web con Streamlit.
- Generación de reportes PDF.

> Constantes: incluyen valores como 'universidades de prestigio' o 'habilidades pertinentes'. Editables desde `app/src/.py`

## Requisitos
- Python 3.10+
- pip

## Instalación

Clonar el repositorio (o descargar):
```bash
git clone https://github.com/matuneville/Recruitment_System_SimpleHuman
cd Recruitment_System_SimpleHuman/app
```
Crear y activar virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

Levantar server de API:

```bash
uvicorn src.api:app --reload
```
En otro terminal, iniciar app de Streamlit:

```bash
streamlit run src/streamlit_app/app.py
```