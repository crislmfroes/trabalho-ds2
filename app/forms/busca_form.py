from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class BuscaForm(FlaskForm):
    termo = StringField()
    submit = SubmitField('Buscar')
