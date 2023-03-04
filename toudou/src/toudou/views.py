import os

import click
import io
import csv

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
    return render_template('delete.html', name=name, data="Tâche supprimée !")

@app.post('/createtask')
def create_task(name=None):
    print(request.form)
    id = request.form['id']
    task = request.form['tache']
    date = request.form['date']
    models.create_todo(id, task)
    return render_template('create.html', name=name, data="Tâche enregistrée !")

@app.route('/getall')
def get_all(name=None):
    resutat = models.get_todos()
    return render_template('get_all.html', name=name, resultat=resutat)

@app.route('/gettask')
def get(name=None):
    return render_template('get_task.html', name=name)

@app.post('/gettask')
def get_task(name=None):
    id = request.form['id']
    resutat = models.get_todo(id)
    print(resutat)
    return render_template('get_task_res.html', name=name, resultat=resutat)

@app.route('/update')
def update(name=None):
    return render_template('update.html', name=name)

@app.post('/update')
def update_task(name=None):
    id = request.form['id']
    if request.form['status'] == "oui":
        status = True
    else:
        status = False
    models.update_todo(id, status)
    return render_template('update.html', name=name, data="Status modifié !")

@app.route('/modify')
def modify(name=None):
    return render_template('modify.html', name=name)

@app.post('/modify')
def modify_task(name=None):
    id = request.form['id']
    new_task = request.form['task']
    models.modify_task(id, new_task)
    return render_template('modify.html', name=name, data="La tâche a été modifiée !")

@app.route('/import')
def import_(name=None):
    services.export_to_csv()
    return render_template('import.html', name=name)

@app.post('/importtask')
def import_task(name=None):
    tasks = request.form['story']
    print(tasks)
    print(type(tasks))

    with open('import.csv', 'w') as file:
        writer = csv.writer(file, delimiter=',')
        for todo in tasks:
            writer.writerow(todo)
            print(todo)

    return render_template('import.html', name=name)

@app.route('/upload', methods=['POST'])
def upload():
    csv_file = request.files['csv_file']
    data=[]
    for row in csv_file:
        row_dec = row.decode("utf-8")
        print(row_dec)
        row_dec = row_dec.replace("\n", "")
        row_dec = row_dec.replace("\r", "")
        data.append(row_dec)
    print(data)
    for val in data:
        liste = list(val.split(","))
        models.create_todo(int(liste[0]), liste[1])

    return render_template('import.html')
@app.route('/export')
def export(name=None):
    services.export_to_csv()
    return render_template('export.html', name=name)


###############################################################################################################

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
def export_csv():
    services.export_to_csv()

@cli.command()
@click.option('--id', prompt='id')
def update(id: int):
    models.update_todo(id, True)

@cli.command()
@click.option('--id', prompt='id')
@click.option("-t", "--task", prompt="Your task", help="The task to remember.")
def modify(id: int, task: int):
    models.modify_task(id, task)

@cli.command()
@click.option('--id', prompt='id')
def delete(id: int):
    models.delete_todo(id)
