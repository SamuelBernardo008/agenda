from flask import Flask, redirect, render_template, request, url_for
from models.database import init_db
from models.tarefa import Tarefa

app = Flask(__name__)

init_db()

@app.route("/", methods=["GET", "POST"])
def agenda():

    if request.method == "POST":
        titulo_tarefa = request.form["titulo-tarefa"]
        data_conclusao = request.form["data-conclusao"]

        tarefa = Tarefa(titulo_tarefa=titulo_tarefa, data_conclusao=
                        data_conclusao)
        tarefa.salvar_tarefa()

        return redirect(url_for("agenda"))

    tarefas = Tarefa.obter_tarefas()

    return render_template(
        "agenda.html", titulo="Agenda", tarefas=tarefas, tarefa_selecionada=None
    )


@app.route("/delete/<int:idTarefa>")
def delete(idTarefa):
    tarefa = Tarefa.id(idTarefa)
    tarefa.excluir_tarefa()
    return redirect(url_for("agenda"))


@app.route("/update/<int:idTarefa>", methods=["GET", "POST"])
def update(idTarefa):

    if request.method == "POST":
        titulo = request.form["titulo-tarefa"]
        data = request.form["data-conclusao"]
        tarefa = Tarefa(titulo, data, idTarefa)
        tarefa.atualizar_tarefa()
        return redirect(url_for("agenda"))

    tarefas = Tarefa.obter_tarefas()
    tarefa_selecionada = Tarefa.id(idTarefa)

    return render_template(
        "agenda.html",
        titulo="Agenda",
        tarefa=tarefas,
        tarefa_selecionada=tarefa_selecionada,
    )
