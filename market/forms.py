from ast import Num
from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,IntegerField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError,NumberRange
from market.model import User

class RegisterForm(FlaskForm):

    def validate_username(self, user_to_check):
        user = User.query.filter_by(username=user_to_check.data).first()

        if user:
            raise ValidationError("Username already exits! Please try a different username")

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(username=email_address_to_check.data).first()

        if email_address:
            raise ValidationError("Email already exits! Please try a different email address")

    username = StringField(label="User Name: ", validators=[Length(min=2,max=30), DataRequired()])
    email_address = StringField(label="Email Address: ", validators=[Email(), DataRequired()])
    password1 = PasswordField(label="Password: ", validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label="Confirm Password: ", validators=[EqualTo("password1"), DataRequired()])
    submit = SubmitField(label="Create Account")


class LoginForm(FlaskForm):
    username = StringField(label="User Name: ", validators=[DataRequired()])
    password = PasswordField(label="Password: ", validators=[DataRequired()])
    submit = SubmitField(label="Sign in")

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label="Purchase share!")

class SellItemForm(FlaskForm):
    changed_price = IntegerField(label="Changed price: ", validators=[NumberRange(min=2,max=999999999999999), DataRequired()])
    submit = SubmitField(label="Sell share!")