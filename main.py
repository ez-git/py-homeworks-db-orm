import json
from sqlalchemy.orm import sessionmaker
from models import *


def create_engine(login, password, db_name, dbms='postgresql',
                  server='localhost', port=5432):
    dsn = f'{dbms}://{login}:{password}@{server}:{port}/{db_name}'
    return sqlalchemy.create_engine(dsn)


def dict_into_value(object_data):
    lines_list = []
    for key, value in object_data['fields'].items():
        lines_list.append(f'{key}="{value}"')
    line = object_data['model'].capitalize() \
        + '(' + ','.join(lines_list) + ')'
    return eval(line)


def add_data(session):
    with open('tests_data.json', 'r') as file:
        json_file = json.load(file)
        for object_data in json_file:
            object_data_execute = dict_into_value(object_data)
            session.add(object_data_execute)
            session.commit()


def get_sales():

    publisher_name = input('Enter publisher name:')

    engine = create_engine('login', 'password', 'db_name')
    create_tables(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    add_data(session)

    query = session.query(Publisher, Book, Stock, Sale, Shop)
    query = query.join(Book, Publisher.id == Book.id_publisher)
    query = query.join(Stock, Book.id == Stock.id_book)
    query = query.join(Sale, Stock.id == Sale.id_stock)
    query = query.join(Shop, Stock.id_shop == Shop.id)
    query = query.filter(Publisher.name == publisher_name)
    for records_all in query.all():
        print(f'{records_all[0].name} | {records_all[4].name}'
              f' | {records_all[3].price} | {records_all[3].date_sale}')


get_sales()
