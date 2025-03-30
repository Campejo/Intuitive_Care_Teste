import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD =os.getenv('DB_PASSWORD')

def abrir_conexao():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print('Conexão estabelecida com sucesso')
        return conn
    
    except Exception as e:
        print('Falha ao conectar ao Banco de Dados!')
        return None


def fechar_conexao(conn):
    if conn:
        conn.close()
        print('Conexão fechada com sucesso!')