from config.settings import CONTRIBUTORS_CSV, CONTRIBUTORS_JSON
from utils.files import read_csv, write_json

data = read_csv(file=CONTRIBUTORS_CSV)
write_json(file=CONTRIBUTORS_JSON, data=data)
