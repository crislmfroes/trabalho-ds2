from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, Required, EqualTo, DataRequired, Length
from flask_bootstrap import Bootstrap

class UsuarioForm(FlaskForm):
    nome = StringField(label='Digite seu nome de usuário')
    email = StringField(label='Digite seu endereço de Email', validators=[Email()])
    telefone = StringField(label='Digite seu telefone', validators=[Length(min=11, max=11)])
    senha = PasswordField(label='Digite sua Senha', validators=[EqualTo('confirmado'), DataRequired()])
    confirmado = PasswordField(label='Confirme sua Senha')
    submit = SubmitField('Enviar')

class UsuarioLoginForm(FlaskForm):
    email = StringField(label='Digite seu endereço de Email', validators=[Email()])
    senha = PasswordField(label='Digite sua Senha', validators=[DataRequired()])
    submit = SubmitField('Enviar')
