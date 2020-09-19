from config.settings import CONTRIBUTORS_CSV, CONTRIBUTORS_JSON, TASKS_CSV, TASKS_JSON
from utils.files import read_csv, write_json

contributors = read_csv(file=CONTRIBUTORS_CSV)
write_json(file=CONTRIBUTORS_JSON, data=contributors)

tasks = read_csv(file=TASKS_CSV)
write_json(file=TASKS_JSON, data=tasks)
