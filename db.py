from os import getenv
from dotenv import load_dotenv

import psycopg2

load_dotenv()

database = "client"
user='postgres'
password = "postgres"
host = '0.0.0.0'
port='5432'

def create_users_table(database, user, password,port):
    comm = '''CREATE TABLE users (
        id_card varchar(9) PRIMARY KEY, 
        first_name varchar(50) NOT NULL,
        last_name varchar(50) NOT NULL, 
        number varchar(15) NOT NULL,
        balance int NOT NULL DEFAULT 0
    );'''
    with psycopg2.connect(database = database, user=user, password = password, port=port) as db:
        with db.cursor() as session:
            session.execute(comm)


def select(table, field, id_card=None):
    if not id_card:
        comm = 'SELECT '+field+' FROM '+table+';'
    else:
        comm = 'SELECT '+field+' FROM '+table+' WHERE id_card=\''+id_card+'\';'
    
    with psycopg2.connect(database = database, user=user, password = password, port=port) as db:
        with db.cursor() as session:
            session.execute(comm)
            r = session.fetchall()

    return r[0][0]

def insert(table,id_card, f_name, l_name, number) -> int:
    comm = "INSERT INTO "+table+" (id_card, first_name, last_name, number) VALUES('"+id_card+"','"+f_name+"','"+l_name+"','"+number+"');"
    with psycopg2.connect(database = database, user=user, password = password ,port=port) as db:
        with db.cursor() as session:
            session.execute(comm)

def update(table,id_card, field, value) -> int:
    comm = "UPDATE "+table+" SET "+field +" = "+value+" WHERE id_card='"+id_card+"';"
    with psycopg2.connect(database = database, user=user, password = password, port=port) as db:
        with db.cursor() as session:
            session.execute(comm)

def remove(table, id_card):
    comm = "DELETE FROM "+table+" WHERE id_card="+id_card
    with psycopg2.connect(database = database, user=user, password = password, port=port) as db:
        with db.cursor() as session:
            session.execute(comm)