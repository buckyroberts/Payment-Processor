import os
from itertools import groupby
from operator import itemgetter
from pathlib import Path

from config.settings import CONTRIBUTORS_CSV, TASKS_CSV
from utils.files import read_csv, write_json

# Target directories
HOME_DIR = Path.home()
WEBSITE_DATA_DIR = os.path.join(HOME_DIR, 'Desktop/Projects/Website/src/data')

# Target files
CONTRIBUTORS_JSON = os.path.join(WEBSITE_DATA_DIR, 'contributors.json')
TASKS_JSON = os.path.join(WEBSITE_DATA_DIR, 'tasks.json')


def write_contributors():
    """
    Write formatted contributors JSON file to target directory
    """

    results = read_csv(file=CONTRIBUTORS_CSV)
    write_json(file=CONTRIBUTORS_JSON, data=results)


def write_tasks():
    """
    Write formatted task JSON file to target directory
    """

    tasks = read_csv(file=TASKS_CSV)
    tasks.sort(key=itemgetter('completed_by'))
    results = {completed_by: list(items) for completed_by, items in groupby(tasks, key=itemgetter('completed_by'))}
    write_json(file=TASKS_JSON, data=results)


def run():
    """
    Run main application
    """

    write_contributors()
    write_tasks()


if __name__ == '__main__':
    run()
