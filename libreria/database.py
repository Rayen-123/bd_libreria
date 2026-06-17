import psycopg2

def conectar():
    return psycopg2.connect(
        host="localhost",
        database="libreria",
        user="postgres",
        password="2801",
        port="5432"
    )