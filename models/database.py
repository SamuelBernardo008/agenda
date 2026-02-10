from sqlite3 import Connection, connect, Cursor
import traceback
from types import TracebackType
from typing import Any, Optional, Self, Type
from dotenv import load_dotenv
import os

load_dotenv()
DB_PATH = os.getenv("DATABASE", "./data/tarefas.sqlite3")

def init_db(db_name: str = DB_PATH):
    with connect(db_name) as conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id  INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo_tarefa TEXT NOT NULL,
            data_conclusao TEXT);
        ''')
        conn.commit()

class Database:
    """
    Classe que representa a conexão com o banco de dados SQLite e fornece métodos para executar consultas.
    """

    def __init__(self, db_name: str = DB_PATH) -> None:
        self.connection: Connection = connect(db_name)
        self.cursor: Cursor = self.connection.cursor()

    def executar(self, query: str, params: tuple = ()) -> Cursor:
        self.cursor.execute(query, params)
        self.connection.commit()
        return self.cursor
    
    def buscar_tudo(self, query: str, params: tuple = ()) -> list[Any]:
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def close(self) -> None:
        self.connection.close()


    def __enter__(self) -> Self:
        return self
    
    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_value: Optional[BaseException], tb: Optional[TracebackType]) -> None:

        if exc_type is not None:
            print("Se lascoukkk")
            print(f"Tipo: {exc_type.__name__}")
            print(f"menagem: {exc_value}")
            print("traceback completo")
            traceback.print_tb(tb)

        self.close()


try: 
    db = Database('./data/tarefas.sqlite3')
    db.executar('''
    CREATE TABLE IF NOT EXISTS tarefas (
        id  INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo_tarefa TEXT NOT NULL,
        data_conclusao TEXT);
    ''')
    db.executar('INSERT INTO tarefas (titulo_tarefa, data_conclusao) VALUES (?,?);', ('Estudar Python', '2026-02-02'))
except Exception as e:
    print(f"erro ao criar tabela: {e}")
finally:
    db.close()