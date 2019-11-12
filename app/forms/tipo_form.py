from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class TipoForm(FlaskForm):
  nome = StringField("Nome")
  submit = SubmitField("Enviar")