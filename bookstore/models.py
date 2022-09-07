from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200), nullable=False, unique=False)
    last_name = db.Column(db.String(200), nullable=False, unique=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable =False, unique=False)
    image_file = db.Column(db.String(20), nullable =False, default='default.jpg')
    admin_status = db.Column(db.Boolean, default=False)
    cart_totals = db.Column(db.Integer, nullable=False,default=0)
    


class Book(db.Model):
    __tablename__ = 'Book'
    isbn = db.Column(db.Integer, primary_key=True, unique=True)
    author = db.Column(db.String(128), nullable=False, unique=False)
    title = db.Column(db.String(256), nullable=False, unique=False)
    price = db.Column(db.Float, nullable=False, unique=False)
    stock_quantity = db.Column(db.Integer, nullable=False, unique=False)
    description = db.Column(db.String, nullable=False, unique=False)
    category = db.Column(db.String, nullable=False, unique=False)
    image_file = db.Column(db.String(20), nullable =False, default='stock.jpg')


class Cart(db.Model):
    __tablename__ = 'Cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('User.id'), nullable=False, unique=False)
    isbn = db.Column(db.ForeignKey('Book.isbn'), nullable=False, unique=False)
    quantity = db.Column(db.Integer, nullable=False, unique=False)

class Order(db.Model):
    __tablename__ = 'Order'
    order_id = db.Column(db.Integer, primary_key=True)
    order_num = db.Column(db.Integer, nullable=False, unique=False)
    user_id = db.Column(db.ForeignKey('User.id'), nullable=False, unique=False)
    isbn = db.Column(db.ForeignKey('Book.isbn'), nullable=False, unique=False)
    quantity = db.Column(db.Integer, nullable=False, unique=False)
