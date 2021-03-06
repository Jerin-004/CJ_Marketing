from locale import currency
from flask import current_app, flash
import flask_login
from market import db,login_manager
from market import bcrypt
from flask_login import UserMixin, current_user
from market import admin
from flask_admin.contrib.sqla import ModelView


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(),primary_key=True)
    username = db.Column(db.String(length=30),nullable=False,unique=True)
    email_address = db.Column(db.String(length=50), nullable=False,unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(),nullable=False,default=10)
    items = db.relationship("Item",backref="owned_user",lazy=True)

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f"{str(self.budget)[:-3]},{str(self.budget)[-3:]}"

        else:
            return f"{str(self.budget)}"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self,plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def can_purchase(self, item_obg):
        return self.budget >= item_obg.price

    def can_sell(self, item_obg):
        return item_obg in self.items


    

class Item(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(length=30),nullable=False,unique=True)
    price = db.Column(db.Integer(),nullable=True)
    barcode = db.Column(db.String(length=12),nullable=False,unique=True)
    description = db.Column(db.String(length=1024),nullable=False,unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    

    def buy(self,user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    def sell(self,user):
        self.owner = None
        user.budget += int(self.price)
        db.session.commit()

    def __repr__(self):
        return f"Item {self.name},{self.price}"

