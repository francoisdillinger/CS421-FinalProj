from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from os import path
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from .book_data import books

db = SQLAlchemy()
DB_NAME = 'bookstore.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'first_flask_app'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    
    from .views import views
    from .auth import auth
    from .admin import admin

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')

    from .models import User, Book

    create_DB(app, User, Book)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_DB(app, User, Book):
    with app.app_context():
        if not path.exists('bookstore/' + DB_NAME):
            db.create_all(app=app)
            add_admin_user_to_db(User)
            add_initial_book_data(Book)

def add_admin_user_to_db(User):
    print('Creating user: Admin')
    user = User(
        first_name='admin', 
        last_name='admin', 
        email='admin1@gmail.com', 
        password=generate_password_hash('1234567', method='sha256'), 
        admin_status=True
    )
    
    db.session.add(user)
    db.session.commit()

def add_initial_book_data(Book):
    print('Creating initial book data.')
    for book in books:
        new_book = Book(
            isbn = book['isbn'],
            author = book['author'],
            title = book['title'],
            price = book['price'],
            stock_quantity = book['stock_quantity'],
            description = book['description'],
            category = book['category'],
            image_file = book['image_file'],
        )
        db.session.add(new_book)
        db.session.commit()