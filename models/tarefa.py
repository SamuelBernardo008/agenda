from datetime import datetime
from sqlite3 import Cursor
from models.database import Database
from typing import Self, Any, Optional

class Tarefa:
    """
    Classe que representa uma tarefa a ser realizada.
    """
    def __init__(self: Self, titulo_tarefa: Optional[str] = '', data_conclusao: Optional[str] = None, tipo: Optional[str] = None, id_tarefa: Optional[int] = None, concluida: Optional[int] = 0, data_finalizacao: Optional[str] = None, indicado: Optional[str] = None) -> None:
        self.titulo_tarefa: Optional[str] = titulo_tarefa
        self.data_conclusao: Optional[str] = data_conclusao
        self.tipo: Optional[str] = tipo
        self.id_tarefa: Optional[int] = id_tarefa
        self.concluida: Optional[int] = concluida
        self.data_finalizacao: Optional[str] = data_finalizacao
        self.indicado: Optional[str] = indicado


    @classmethod
    def id(cls, id: int) -> Self:
        with Database() as db:
            query: str = "SELECT titulo_tarefa, data_conclusao FROM tarefas WHERE id = ?;"
            params:tuple = (id,)
            resultado: list[Any] = db.buscar_tudo(query, params)

            [[titulo, data]] = resultado

        return cls(id_tarefa=id, titulo_tarefa=titulo, data_conclusao=data)

    def salvar_tarefa(self: Self) -> None:
        with Database() as db:
            query: str = "INSERT INTO tarefas (titulo_tarefa, data_conclusao) VALUES (?,?);"
            params: tuple = (self.titulo_tarefa, self.data_conclusao)
            db.executar(query, params)

    @classmethod
    def obter_tarefas(cls) -> list[Self]:
        with Database() as db:
            query: str = 'SELECT titulo_tarefa, data_conclusao, id FROM tarefas;'
            resultados: list[Any] = db.buscar_tudo(query)
            tarefas: list[Self] = [cls(titulo, data, id) for titulo, data, id in resultados]
            return tarefas
        
    def excluir_tarefa(self) -> Cursor:
        with Database() as db:
            query: str = "DELETE FROM tarefas WHERE id = ?;"
            params: tuple = (self.id_tarefa,)
            return db.executar(query, params)
        
    def atualizar_tarefa(self) -> Cursor:
        with Database() as db:
            query: str = "UPDATE tarefas SET titulo_tarefa = ?, data_conclusao = ? WHERE id = ?;"
            params: tuple = (self.titulo_tarefa, self.data_conclusao, self.id_tarefa)
            resultado: Cursor = db.executar(query, params)
            return resultado 
        
    def toggle_conclusao(self):

            with Database() as db:

                if self.concluida:
                    query = """
                    UPDATE tarefas
                    SET concluida = 0, data_finalizacao = NULL
                    WHERE id = ?;
                    """
                    params = (self.id_tarefa,)

                    self.concluida = 0
                    self.data_finalizacao = None

                else:
                    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    query = """
                    UPDATE tarefas
                    SET concluida = 1, data_finalizacao = ?
                    WHERE id = ?;
                    """
                    params = (agora, self.id_tarefa)

                    self.concluida = 1
                    self.data_finalizacao = agora

                db.executar(query, params)