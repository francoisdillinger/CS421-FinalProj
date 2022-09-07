from tokenize import String
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Regexp

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(message='Use a valid email address.')])
    password = PasswordField("Password.", validators=[DataRequired()])
    submit = SubmitField("Submit")

class PurchaseForm(FlaskForm):
    shipping_address = StringField("Address", validators=[DataRequired()])
    credit_card_number = StringField("Credit Card Number", validators=[DataRequired()])
    csv = StringField("CSV", validators=[DataRequired()])
    expiration = StringField( "Experation Date (MM/YY)", validators=[DataRequired()])
    
    
