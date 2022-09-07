from random import randint
from flask import Blueprint, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from PIL import Image
from .models import Book, Cart, User,Order
from . import db
from bookstore.forms import PurchaseForm
import secrets
import os


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    books = Book.query.all()
    categories = {book.category for book in books}   
    if request.method == "POST":
        books = filter_books_by(books, request.form.get("cat_option"))
    return render_template("home.html", user=current_user, books=books, categories=categories)


@views.route('/add_to_cart/<isbn>', methods=["GET"])
@login_required
def add_to_cart(isbn):
    isbn = int(isbn)
    count = 1
    for book in Cart.query.filter_by(user_id=current_user.id):
        if isbn == book.isbn:
            count = book.quantity + 1
            break

    item = Cart(isbn=isbn, user_id=current_user.id, quantity=count)
    
    stock_quantity = Book.query.filter_by(isbn=isbn).first().stock_quantity
    if stock_quantity > 0:
        if count == 1:
            db.session.add(item)
        else:
            db.session.query(Cart).filter_by(isbn=isbn, user_id=current_user.id).update({'quantity': count})
        db.session.query(Book).filter_by(isbn=isbn).update({
            'stock_quantity': stock_quantity-1
        })
        db.session.commit()
        add_to_user_cart_total()
    else:
        flash("No more books in stock", 'error')
    return redirect(url_for('views.home'))


@views.route('/cart')
@login_required
def cart():
    cart = Cart.query.filter_by(user_id=current_user.id) 
    class Cart_Item():
        def __init__(self, title: str, price: float, quantity: int, image_file: str):
            self.title = title
            self.price = price
            self.quantity = quantity
            self.image_file = image_file
    cart_items = []
    total_price = 0
    total_items = 0
    for item in cart:
        data = Book.query.filter_by(isbn=item.isbn).first()
        cart_item = Cart_Item(data.title, (data.price * item.quantity), item.quantity, data.image_file)
        print(cart_item.quantity)
        cart_items.append(cart_item)
        total_items += cart_item.quantity
        total_price += cart_item.price
    
    update_user_cart_totals(total_items)

    return render_template("cart.html", user=current_user, cart=cart_items, total_price=f"${total_price:.2f}", total_items=total_items)

@views.route('/cart/delete/<user_id>/<title>')
@login_required
def remove_cart_item(user_id, title):

    print(f'Delete book: {title} from the cart for user_id: {user_id}')
    book = Book.query.filter_by(title=title).first()
    cart_item = Cart.query.filter_by(user_id=user_id, isbn=book.isbn).first()

    if cart_item.quantity > 1:
        cart_item.quantity = cart_item.quantity - 1
        db.session.commit()
    else:
        db.session.delete(cart_item)
        db.session.commit()
    
    book.stock_quantity += 1 
    db.session.commit()
    
    return redirect(url_for('views.cart'))

@views.route('/check_out', methods=["POST","GET"])
@login_required
def check_out():

    form = PurchaseForm()
    count=Cart.query.filter_by(user_id=current_user.id).count()
    cart = Cart.query.filter_by(user_id=current_user.id) 
   
    if request.method == "POST":
        if count>0:
           
            cart = Cart.query.filter_by(user_id=current_user.id) 

            #add item to Order table
            order_num = randint(100_000_000, 999_999_999)
            for item in cart:
                order_item=Order(order_num=order_num, user_id=current_user.id, isbn=item.isbn, quantity=item.quantity)
                db.session.add(order_item)
                db.session.commit()


            #Delete item from Cart
            Cart.query.filter_by(user_id=current_user.id).delete()
            db.session.commit()
            flash("Thank you for your purchase", category='success')
            update_user_cart_totals(0)
        else:
            flash ( "Empty Cart", category='error')
        return redirect(url_for("views.home"))
    return render_template("checkout.html", user=current_user, form=form)


@views.route('/my_profile/<id>', methods=['GET', 'POST'])
@login_required
def my_profile(id):
    
    if request.method == 'POST':
        image = request.files['image_file']
        new_image_name = check_image_file_and_save(image, 'profile_images')
        if new_image_name:
            current_user.image_file = new_image_name
        current_user.first_name = request.form.get('firstname')
        current_user.last_name = request.form.get('lastname')
        current_user.email = request.form.get('email')
        db.session.commit()
        return redirect(url_for('views.my_profile',id = current_user.id))

                
    return render_template('my_profile.html', user=current_user)


def update_user_cart_totals(total_items):
    user = User.query.filter_by(id=current_user.id).first()
    user.cart_totals = total_items
    db.session.commit()

def add_to_user_cart_total():
    user = User.query.filter_by(id=current_user.id).first()
    user.cart_totals += 1
    db.session.commit()


def check_image_file_and_save(image, img_folder):
    image_name = image.filename
    _, ext = os.path.splitext(image_name)
    if image_name:
        if ext != '.jpg' and ext != '.png':
            flash('Not proper file format. Must be .jpg or .png, default image selected.', category='error')
        else:
            file_hex = secrets.token_hex(8)
            path_hex = file_hex + ext
            full_img_path = os.path.join(os.path.realpath("bookstore"), f'static/{img_folder}', path_hex)
            new_size = (300, 300)
            resized_image = Image.open(image)
            resized_image.thumbnail(new_size)
            resized_image.save(full_img_path)
            return path_hex

def filter_books_by(books: list, filter: str):
    if filter == 'All':
        return books

    filtered_books = []
    for book in books:
        if book.category == filter:
            filtered_books.append(book)
    return filtered_books