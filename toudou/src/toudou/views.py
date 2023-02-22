import click
import io

from datetime import datetime

import toudou.models as models
import toudou.services as services

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home(name=None):
    return render_template('home.html', name=name)

@app.route('/create')
def create(name=None):
    return render_template('create.html', name=name)

@app.route('/delete')
def delete(name=None):
    return render_template('delete.html', name=name)

@app.post('/deletetask')
def delete_task(name=None):
    id = request.form['id']
    models.delete_todo(id)
    return render_template('home.html', name=name)

@app.post('/createtask')
def create_task(name=None):
    print(request.form)
    id = request.form['id']
    task = request.form['tache']
    date = request.form['date']
    models.create_todo(id, task)
    return render_template('home.html', name=name, data="ok")

@app.route('/getall')
def get_all(name=None):
    resutat = models.get_todos()
    return render_template('get_all.html', name=name, resultat=resutat)

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
