from flask import Flask, redirect, render_template, request, url_for
from models.tarefa import Tarefa

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', titulo='Home')


@app.route('/ola')
def ola_mundo():
    return "olá, mundo"

@app.route('/agenda', methods=['GET', 'POST'])
def agenda():
    tarefas = None
    
    if request.method == 'POST':
        titulo_tarefa = request.form ['titulo-tarefa']
        data_conclusao = request.form['data-conclusao']
        tarefa = Tarefa(titulo_tarefa, data_conclusao) 
        tarefa.salvar_tarefa()

    tarefas = Tarefa.obter_tarefas()
    return render_template('agenda.html', titulo= 'Agenda', tarefas=tarefas)

@app.route('/delete/<int:idTarefa>')
def delete(idTarefa):
    tarefa = Tarefa.id(idTarefa)
    tarefa.excluir_tarefa()
    return redirect(url_for('agenda'))