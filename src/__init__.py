# Lib Imports
from bottle import run, route, get, post, request, delete
from json import dumps

tasks = {
    1: ["Prova"],
    2: ["Pesquisa", "Prova"],
    3: ["Trabalho"]
}

subjects = {
    "calculo-diferencial": { "id": 1, "name": "Calculo Diferencial" },
    "analise-de-dados": { "id": 2, "name": "Analise de Dados" },
    "sistemas-operacionais": { "id": 3, "name": "Sistemas Operacionais" }
}


# Route Definitions
@get("/api/subject")
def get_subjects():
    return dumps(subjects)


#
@post("/api/subject")
def add_subject():
    body = request.json
    key = list(body)[0]  # converte dict em list e pega a chave
    subjects[key] = body[key]


@get("/api/subject/<subject>")
def get_subject(subject):
    return dumps(subjects[subject])


@get("/api/subject/<_id:int>/task")
def get_tasks(_id):
    return dumps(tasks[_id])


@post("/api/subject/<_id:int>/task")
def add_task(_id):
    body = request.json
    tasks[_id].append(body)
    return tasks


run(host="localhost", port=8080, reloader=True, debug=False)
