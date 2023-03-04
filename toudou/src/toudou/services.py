import csv
import dataclasses
import io
import shutil
from datetime import datetime

from toudou.models import *

from toudou.models import Todo, get_todos

def export_to_csv() -> bool:

    with open('todos.csv', 'w') as file:
        writer = csv.writer(file, delimiter=',')
        for todo in get_todos():
            writer.writerow(todo)
    return True

def import_from_csv(data: str) -> None:
    with io.StringIO(data) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:

            print(row)
            print(row[0])

            create_todo(int(row[0]), row[1])

            # create_todo(
            #     task=row["task"],
            #     due=datetime.fromisoformat(row["due"]) if row["due"] else None,
            #     complete=bool(row["complete"])
            # )
