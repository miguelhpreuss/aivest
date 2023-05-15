import sqlalchemy
import os

def create_sqlalchemy_connection_string(db_type, host, username, password, port, db_name=None, service_name=None):
    if db_type.lower() == 'oracle':
        con_str = f'oracle+cx_oracle://{username}:{password}@{host}:{port}'
        if service_name is not None:
            con_str += f'/?service_name={service_name}'
        return con_str

    if db_type.lower() == 'postgres':
        if db_name is None:
            raise TypeError('Postgres need athe parameter db_name to be able to create connection string')
        con_str = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}'
        return con_str


def try_to_create_engine(sql_alchemy_string):
    try:
        engine = sqlalchemy.create_engine(sql_alchemy_string)
        con = engine.connect()
        con.close()
        return engine
    except:
        raise Exception("Wasn't able to connect to database!!")

POSTGRES_STRING = create_sqlalchemy_connection_string('postgres', 'localhost',
        'postgres', 'asd', '5432',
        db_name="postgres")

ALCHEMY_POSTGRES_ENGINE = try_to_create_engine(POSTGRES_STRING)