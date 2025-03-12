from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    """User registration form"""
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=3, max=64)
    ])
    email = StringField('Email', validators=[
        DataRequired(), 
        Email()
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password')
    ])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        """Check if username is already taken"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')
    
    def validate_email(self, email):
        """Check if email is already registered"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different one.')

class LoginForm(FlaskForm):
    """User login form"""
    email = StringField('Email', validators=[
        DataRequired(), 
        Email()
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    """Form for creating and editing posts"""
    title = StringField('Title', validators=[
        DataRequired(),
        Length(min=3, max=120)
    ])
    content = TextAreaField('Content', validators=[
        DataRequired()
    ])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    """Form for creating and editing comments"""
    content = TextAreaField('Comment', validators=[
        DataRequired(),
        Length(min=1, max=1000)
    ])
    submit = SubmitField('Submit')

class RatingForm(FlaskForm):
    """Form for rating posts"""
    value = RadioField('Rating', choices=[
        ('1', '1 Star'),
        ('2', '2 Stars'),
        ('3', '3 Stars'),
        ('4', '4 Stars'),
        ('5', '5 Stars')
    ], validators=[DataRequired()])
    submit = SubmitField('Rate')