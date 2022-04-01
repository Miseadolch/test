from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField


class MessageForm(FlaskForm):
    message = TextAreaField('message')
    submit = SubmitField('Enter')
