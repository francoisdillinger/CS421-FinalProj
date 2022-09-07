from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Book, Order, User
from . import db
from flask_login import login_required, current_user
from .views import check_image_file_and_save

admin = Blueprint('admin', __name__)

@admin.route('/admin_book_add', methods=['GET', 'POST'])
@login_required
def admin_book_add():
    if not check_if_admin():
        return redirect(url_for('views.home'))
    if request.method == 'POST':

        isbn = int(request.form.get('isbn'))
        book_exists = Book.query.filter_by(isbn=isbn).first()

        if not book_exists:   
            image = request.files['image_file']
            new_image_name = check_image_file_and_save(image, 'book_images')
            book_image = 'stock.jpg'
            if new_image_name:
                book_image = new_image_name

            title = request.form.get('title')
            author = request.form.get('author')
            description = request.form.get('description')
            price = float(request.form.get('price'))
            category = request.form.get('category')
            stock_quantity = int(request.form.get('stock-quantity'))

            book = Book(isbn=isbn, author=author, title=title, price=price,
                        stock_quantity=stock_quantity, description=description, category=category, image_file=book_image)
            db.session.add(book)
            db.session.commit()

            return redirect(url_for('views.home'))
        else:
            flash('Book already exists.', category='error')
            # This redirect with a GET request attempts to clear form.
            return redirect(url_for('views.home'))
    return render_template('admin_book_add.html', user=current_user)


@admin.route('/admin_book_edit/<isbn>', methods=['GET', 'POST'])
@login_required
def admin_book_edit(isbn):
    if not check_if_admin():
        return redirect(url_for('views.home'))
    book = Book.query.filter_by(isbn=isbn).first()

    if request.method == 'POST':
        image = request.files['image_file']
        new_image_name = check_image_file_and_save(image, 'book_images')
        book_image = book.image_file
        if new_image_name:
            book_image = new_image_name
        isbn = int(request.form.get('isbn'))
        title = request.form.get('title')
        author = request.form.get('author')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        category = request.form.get('category')
        stock_quantity = int(request.form.get('stock-quantity'))
        db.session.query(Book).filter_by(isbn=book.isbn).update({
                'isbn': isbn, 
                'title': title, 
                'author': author, 
                'description': description, 
                'price': price, 
                'category': category, 
                'stock_quantity': stock_quantity,
                'image_file': book_image
            }, synchronize_session=False)

        db.session.commit()
        return redirect(url_for('views.home'))

    return render_template('admin_book_edit.html', user=current_user, book=book)


@admin.route('/admin_book_delete/<isbn>', methods=['GET', 'POST'])
@login_required
def admin_book_delete(isbn):
    if not check_if_admin():
        return redirect(url_for('views.home'))

    book = Book.query.filter_by(isbn=isbn).first()
    print('We in the deletes!')
    db.session.query(Book).filter_by(isbn=book.isbn).delete()
    db.session.commit()
    return redirect(url_for('views.home'))





@admin.route("/admin_view_order")
@login_required
def view_order():
    if not check_if_admin():
        return redirect(url_for('views.home'))
    orders = Order.query.all()

    order_nums = set()
    for order in orders:
        order_nums.add(order.order_num)
        
    desired_order_data=[]
    for order_num in order_nums:

        order = {'order_num': order_num, 'order_items': []}
        order_items = Order.query.filter_by(order_num=order_num)
        print(f"Order number: {order_num}")
        for item in order_items:
            data = {
                'user_email': User.query.filter_by(id=item.user_id).first().email,
                'book_title': Book.query.filter_by(isbn=item.isbn).first().title,
                'quantity': item.quantity
            }
            order['order_items'].append(data)
        desired_order_data.append(order)
    return render_template("order.html", orders=desired_order_data, user=current_user)


def check_if_admin():
    admin = current_user.admin_status
    if admin:
        return True
