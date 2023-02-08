import click
import io

from datetime import datetime

import toudou.models as models
import toudou.services as services


@click.group()
def cli():
    pass


@cli.command()
def init_db():
    models.init_db()


@cli.command()
@click.option('--id', prompt='id')
@click.option("-t", "--task", prompt="Your task", help="The task to remember.")
@click.option("-d", "--due", type=click.DateTime(), default=None, help="Due date of the task.")
def create(id:int, task: str, due: datetime):
    models.create_todo(id, task, due=due)


@cli.command()
@click.option('--id', prompt='id')
def get(id: int):
    click.echo(models.get_todo(id))


@cli.command()
@click.option("--as-csv", is_flag=True, help="Ouput a CSV string.")
def get_all(as_csv: bool):
    if as_csv:
        click.echo(services.export_to_csv())
    else:
        click.echo(models.get_todos())


@cli.command()
@click.argument('csv_file', type=click.File('r'))
def import_csv(csv_file: io.TextIOWrapper):
    services.import_from_csv(csv_file.read())


@cli.command()
@click.option('--id', prompt='id')
def update(id: int):
    models.update_todo(id)

@cli.command()
@click.option('--id', prompt='id')
@click.option("-t", "--task", prompt="Your task", help="The task to remember.")
def modify(id: int, task: int):
    models.modify_task(id, task)

@cli.command()
@click.option('--id', prompt='id')
def delete(id: int):
    models.delete_todo(id)
