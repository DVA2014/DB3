import sqlalchemy
from sqlalchemy.orm import sessionmaker

DSN = 'postgresql://postgres:postgres@localhost:5432/clients_db'

engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

session.close()

from models import create_tables, Publisher, Book, Sale, Shop, Stock

create_tables(engine)

publisher_name = input("Введите имя издателя: ")

results = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale) \
    .join(Stock, Stock.id_book == Book.id) \
    .join(Shop, Stock.id_shop == Shop.id) \
    .join(Sale, Sale.id_stock == Stock.id) \
    .filter(Book.id_publisher == Publisher.id).all()

if results:
    for result in results:
        print(f"Книга: {result[0]} | Магазин: {result[1]} | Стоимость: {result[2]} | Дата покупки: {result[3]}")
else:
    print("Нет покупок для данного издателя.")