# Lib Imports
from bottle import run, get, post, request, delete
from json import dumps

tasks = {
    101: { "name": "Prova", "value": 6 },
    202: { "name": "Pesquisa", "value": 2 },
    303: { "name": "Trabalho", "value": 2 },
    404: { "name": "Revisão", "value": 0 }
}

subject_tasks = {
    1: [ { "task": 101, "date": 0 } ],
    2: [ { "task": 101, "date": 0 }, { "task": 202, "date": 0 } ],
    3: [ { "task": 303, "date": 0 } ]
}

subjects = {
    1: { "name": "Calculo Diferencial", "weekday": "Quinta" },
    2: { "name": "Analise de Dados", "weekday": "Segunda" },
    3: { "name": "Sistemas Operacionais", "weekday": "Quarta" }
}


# Subject Route Definitions
@get("/api/subject")
def get_subjects():
    output = []
    for key, value in subjects.items():
        subject = { "id": key, "name": value["name"], "weekday": value["weekday"] }
        output.append(subject)
    return dumps(output)


@post("/api/subject")
def add_subject():
    body = request.json
    _id = generate_subject_id()
    subject = { "name": body["name"], "weekday": body["weekday"] }
    subjects[_id] = subject
    return dumps({ "id": _id })


@get("/api/subject/<_id:int>")
def get_subject(_id):
    return dumps(subjects[_id])


@get("/api/subject/<_id:int>/task")
def get_tasks(_id):
    return dumps(subject_tasks[_id])


@post("/api/subject/<_id:int>/task")
def add_task(_id):
    body = request.json
    subject_tasks[_id].append(body)
    return subject_tasks


# Functions
def generate_subject_id():
    return max(subjects.keys()) + 1


def generate_task_id():
    return max(tasks.keys()) + 101


run(host="localhost", port=8080, reloader=True, debug=False)
