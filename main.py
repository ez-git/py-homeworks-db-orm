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

    res = session.query(Book.title, Shop.name, Sale.price, Sale.count,
                        Sale.date_sale). \
        join(Publisher).join(Stock).join(Sale).join(Shop).filter(
        Publisher.name == publisher_name)

    for book, shop, price, count, date in res:
        print(f'{book: <40} | {shop: <10} | {price * count: <8} | {date}')


get_sales()
