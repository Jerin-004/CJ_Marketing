from unicodedata import name
from market import app
from flask import abort, render_template, redirect,url_for,flash,get_flashed_messages, request
from market.model import Item,User
from market.forms import LoginForm, RegisterForm, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user,logout_user, login_required, current_user
import os
from market import admin
from flask_admin.contrib.sqla import ModelView


pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'CJ_Logo_2.png')
titlepic = os.path.join(app.config['UPLOAD_FOLDER'], 'shopping-cart.png')



@app.route("/") # are called as decorator
@app.route("/home")
def home_page():
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'CJ_Logo_2.png')
    return render_template("home.html",comp_logo=pic1, title_logo=titlepic)

@app.route("/market",methods=['GET','POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == 'POST':
        #purchase item login
        purchase_item = request.form.get('purchase_item')
        p_item_object = Item.query.filter_by(name=purchase_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations! you purchased {p_item_object.name}'s share for {p_item_object.price}$", category='success')

            else:
                flash(f"Unfortunately, you dont't enough money to purchase {p_item_object.name}'s share for {p_item_object.price}$", category='danger')
        
        #sold item login
        sold_item = request.form.get('sold_item')
        changed_price = request.form.get('changed_price')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.price = changed_price
                s_item_object.sell(current_user)
                flash(f"Congratulations! You Sold {s_item_object.name}'s share back to market!", category='success')

            else:
                flash(f"Something went wrong while selling {s_item_object.name}'s share", category='danger')

        return redirect(url_for("market_page"))
    
    if request.method == "GET":    
        owned_items = Item.query.filter_by(owner=current_user.id)
        items = Item.query.filter_by(owner=None)
        return render_template("market.html",items=items, title_logo=titlepic,purchase_form=purchase_form, owned_items = owned_items, selling_form=selling_form,comp_logo=pic1) 

@app.route("/register" ,methods=['GET','POST'])
def register_page():
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'CJ_Logo_2.png')
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, 
                              email_address=form.email_address.data,
                              password_hash=form.password1.data,)
                              #password=form.password1.data) :}  uncomment this if you are a baby
        
        db.session.add(user_to_create)
        db.session.commit()
        
        login_user(user_to_create)
        flash(f"Account Created Successfully! You are now logged in as {user_to_create.username}", category='success')

        return redirect(url_for('market_page'))

    if form.errors != {}: # If there is errors from the validations
        for err_msg in form.errors.values():
            flash(f"There was an unexpected {err_msg}", category='danger')

    return render_template("register.html", form=form, comp_logo=pic1, title_logo=titlepic)


@app.route("/login",methods=['GET','POST'])
def login_page():
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'CJ_Logo_2.png')
    form = LoginForm()

    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        attempted_password = User.query.filter_by(password_hash=form.password.data).first()
        if attempted_password and attempted_user:
            login_user(attempted_user)
            flash(f"Succesfully logged in as {attempted_user.username}", category='success')
            return redirect(url_for("market_page"))

        else:
            flash("Username and password are not match! Please try again", category="danger")

    return render_template("login.html", form=form, comp_logo=pic1, title_logo=titlepic)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("Logged out successfully!", category="info")
    return redirect(url_for('home_page'))


class Controller(ModelView):
    def is_accessible(self):
        if current_user.username == "Jerin":
            return current_user.is_authenticated
        
        else:
            return flash("You are not authorized to use the admin dashboard",category="danger")
            return redirect(url_for("market_page"))
            

    def not_auth(self):
        flash("You are not authorized to use the admin dashboard",category="danger")
        return redirect(url_for("market_page"))

admin.add_view(Controller(User, db.session))
admin.add_view(Controller(Item, db.session))