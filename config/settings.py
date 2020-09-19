import os

# Core
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Data directories
CSVS_DIR = os.path.join(BASE_DIR, 'csvs')

# Results directories
RESULTS_DIR = os.path.join(BASE_DIR, 'results')

# Data files
CONTRIBUTORS_CSV = os.path.join(CSVS_DIR, 'contributors.csv')
TASKS_CSV = os.path.join(CSVS_DIR, 'tasks.csv')

# Results files
CONTRIBUTORS_JSON = os.path.join(RESULTS_DIR, 'contributors.json')
TASKS_JSON = os.path.join(RESULTS_DIR, 'tasks.json')
