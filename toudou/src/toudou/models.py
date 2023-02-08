import os
import pickle
import uuid
import sqlite3

from sqlalchemy import *
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


TODO_FOLDER = os.path.join("sqlite:///Z:\\archi_log\\toudou_starter_models\\toudou\\db\\", "todos.db")


@dataclass
class Todo:
    id: int
    task: str
    complete: bool
    due: Optional[datetime]

engine = create_engine(TODO_FOLDER, echo=True)
metadata_obj = MetaData()
todo_table = Table(
    "todos",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("task", String(1000), nullable=False),
    Column("complete", Boolean, nullable=False),
    Column("due", DateTime, nullable=True)
)

def init_db() -> None:
    metadata_obj.create_all(engine)

def create_todo(id : int, task: str, complete: bool = False, due: Optional[datetime] = None,) -> None:

    stmt = insert(todo_table).values(id=id, task=task, complete=complete, due=due)

    with engine.connect() as conn:
        result = conn.execute(stmt)
        conn.commit()


def get_todo(id: int) -> Todo:
    stmt = select(todo_table).where(todo_table.c.id == id)

    with engine.connect() as conn:

        for row in conn.execute(stmt):

            print(row)

def modify_task(id: int, task: str) -> None:

    stmt = (update(todo_table).where(todo_table.c.id == id).values(task=task))

    with engine.connect() as conn:
        result = conn.execute(stmt)
        conn.commit()

def get_todos() -> list[Todo]:
    stmt = select(todo_table)

    with engine.connect() as conn:

        for row in conn.execute(stmt):

            print(row)


def update_todo(id: int) -> None:

    stmt = (update(todo_table).where(todo_table.c.id == id).values(complete=True))

    with engine.connect() as conn:
        result = conn.execute(stmt)
        conn.commit()

def delete_todo(id: int) -> None:

    stmt = (delete(todo_table).where(todo_table.c.id == id))

    with engine.connect() as conn:
        result = conn.execute(stmt)
        conn.commit()
