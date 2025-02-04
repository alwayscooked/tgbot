import configparser
import psycopg2
import logging
import sys

config = configparser.ConfigParser()
config.read('config.ini')

database = config['database.client']['database_name']
user = config['database.client']['user']
password = config['database.client']['password']
port = config['database.client']['port']
host = config['database.client']['host']

def request(command:str, database:str = database, user:str = user, password:str = password, host:str = host, port:str = port):
    try:
        with psycopg2.connect(database = database, user=user, password = password, port=port,host=host) as db:
            with db.cursor() as session:
                session.execute(command)
                if command.split()[0]=='SELECT':
                    data = session.fetchall()
                    return data

    except psycopg2.Error as e:
        logging.error(f'{e}')
        return -1

    return 0

if not __name__=='__main__':

    comm = '''CREATE TABLE IF NOT EXISTS users (
        id_card varchar(9) PRIMARY KEY, 
        first_name varchar(50) NOT NULL,
        last_name varchar(50) NOT NULL, 
        number varchar(15) NOT NULL,
        balance int NOT NULL DEFAULT 0
    );'''
    
    if request(comm)==-1:
        logging.error("[!]Error during create table! Please, change some parameters in config.ini file!")
        sys.exit(-1)