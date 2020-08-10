from flask_wtf import FlaskForm
from wtforms import PasswordField,StringField
from wtforms.validators import DataRequired, InputRequired, Length, Email



class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators= [DataRequired()])
    
    
class Register(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
    
class Edituserform(FlaskForm):
    '''editing a user '''
    
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
    location = StringField('Enter 2char Country Code eg: AU,US', validators=[Length(min=2)])
    