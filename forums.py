from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models import User

class ContactForm(FlaskForm):
    name = StringField('Your Name', validators=[
        DataRequired(),
        Length(min=2, max=50)
    ])

    email = StringField('Your Email', validators=[
        DataRequired(),
        Email()
    ])

    message = TextAreaField('Your Message', validators=[
        DataRequired(),
        Length(min=5, max=500)
    ])

    submit = SubmitField('Send')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])

    password = PasswordField('Password', validators=[
        DataRequired()
    ])

    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=2, max=30)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(max=100)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, max=100)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please choose a different one.')

class RemedyForm(FlaskForm):
    
    name        = StringField("Remedy Name", validators=[DataRequired(), Length(max=100)])
    
    description = TextAreaField("Description", validators=[DataRequired()])
   
    audio       = StringField("Audio File (URL or static path)", validators=[DataRequired(), Length(max=120)])
    
    use         = StringField("Use / Purpose", validators=[DataRequired(), Length(max=200)])
    
    dosage      = StringField("Dosage", validators=[DataRequired(), Length(max=200)])
    
    submit      = SubmitField("Save")