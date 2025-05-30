# Constantes para data
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # lleva hasta `app/`
CANDIDATES_DATA_PATH = BASE_DIR / "data" / "candidates.csv"
REPORT_DIR = BASE_DIR / "data"
HEADER = ['full_name', 'email', 'college', 'degree', 'academic_average', 'skills', 'work_experience']

# Universidades consideradas de alto prestigio
PRESTIGE_COLLEGES = [
    'Massachusetts Institute of Technology',
    'Stanford University',
    'Harvard University',
    'University of Cambridge',
    'University of Oxford',
    'University of Tokyo',
    'National University of Singapore',
]

# Habilidades relevantes para un puesto de trainee buscado
RELEVANT_SKILLS_FOR_TRAINEE_ROLE = [
    'Programming',
    'Data Science',
    'Machine Learning',
    'Python',
    'JavaScript',
    'SQL',
    'Git',
    'Linux',
    'Algorithms',
    'Data Structures',
    'Cloud Basics',
    'APIs',
    'Docker',
    'Testing'
]