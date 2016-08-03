from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class SForm(Form):
    SECRET_KEY = "skein_test_project"
    search = StringField('Search', validators=[DataRequired()])
    email =  StringField('Email Address', validators=[DataRequired(), Email()])
    submit = SubmitField("Search")
