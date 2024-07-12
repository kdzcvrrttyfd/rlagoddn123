from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User, Item ,Image
from app.forms import RegistrationForm, LoginForm, ImageForm
import os
main = Blueprint('main', __name__)
users = Blueprint('users', __name__)
def extract_filename(url):
    filename = os.path.basename(url)
    name, _ = os.path.splitext(filename)
    return name

@main.route('/')
@main.route('/home')
def home():
    
    return render_template('index.html')

@main.route('/fashion')
def fashion():
    return render_template('it.html')

@main.route('/electronic')
def electronic():
    images = Image.query.all()
    images_with_filenames = [(image.url, extract_filename(image.url)) for image in images]
    return render_template('infa.html', images=images_with_filenames)

@main.route('/jewellery')
def jewellery():
    return render_template('jewellery.html')

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, phone_number=form.phone_number.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/cart')
@login_required
def cart():
    # cart = current_user.cart
    # if not cart:
    #     cart = Cart(user_id=current_user.id)
    #     db.session.add(cart)
    #     db.session.commit()
    return render_template('cart.html', cart=cart)

# @main.route('/add_to_cart/<int:item_id>', methods=['POST'])
# @login_required
# def add_to_cart(item_id):
#     item = Item.query.get_or_404(item_id)
#     cart = current_user.cart
#     if not cart:
#         cart = Cart(user_id=current_user.id)
#         db.session.add(cart)
#         db.session.commit()

#     cart_item = CartItem.query.filter_by(cart_id=cart.id, item_id=item.id).first()
#     if cart_item:
#         cart_item.quantity += 1
#     else:
#         cart_item = CartItem(cart_id=cart.id, item_id=item.id, quantity=1)
#         db.session.add(cart_item)
    
#     db.session.commit()
#     flash(f'Item {item.name} added to cart', 'success')
#     return redirect(url_for('main.home'))

@main.route('/search')
def search():
    query = request.args.get('query')
    items = Item.query.filter(Item.name.like(f'%{query}%')).all()
    return render_template('search_results.html', items=items, query=query)


@users.route('/add_image', methods=['GET', 'POST'])
def add_image():
    form = ImageForm()
    if form.validate_on_submit():
        new_image = Image(url=form.url.data)
        db.session.add(new_image)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('add_image.html', form=form)