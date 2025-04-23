import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()  

class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=100), unique=True)\
    
    books = relationship("Book", back_populates="publisher")

class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=100), unique=True)

    stock = relationship("Stock", back_populates="shops")

class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=100), unique=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'))

    publisher = relationship("Publisher", back_populates="books")
    stock = relationship("Stock", back_populates="books")

class Stock(Base):
    __tablename__ = "stock"
    
    id = sq.Column(sq.Integer, primary_key=True)
    id_book =  sq.Column(sq.Integer, sq.ForeignKey('book.id'))
    id_shop =  sq.Column(sq.Integer, sq.ForeignKey('shop.id'))
    count =  sq.Column(sq.Integer, default=0)
    
    books = relationship("Book", back_populates="stock")
    shops = relationship("Shop", back_populates="stock")
    sales = relationship("Sale", back_populates="stocks")

class Sale(Base):
    __tablename__ = "sale"
    
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Numeric(10, 2), nullable=False)
    date_sale = sq.Column(sq.DateTime, default=sq.func.now(), nullable=False)
    id_stock =  sq.Column(sq.Integer, sq.ForeignKey('stock.id'))
    count =  sq.Column(sq.Integer, default=0)
    
    stocks = relationship("Stock", back_populates="sales")

def create_tables(engine):
    Base.metadata.create_all(engine)

