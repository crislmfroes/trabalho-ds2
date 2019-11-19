from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import Email, EqualTo, DataRequired, Length
from flask_bootstrap import Bootstrap


class GenericForm(FlaskForm):
    nome = StringField(label='Digite seu nome de usuário')
    email = StringField(
        label='Digite seu endereço de Email', validators=[Email()])
    telefone = StringField(label='Digite seu telefone',
                           validators=[Length(min=11, max=11)])
    senha = PasswordField(label='Digite sua Senha', validators=[
                          EqualTo('confirmado'), DataRequired()])
    confirmado = PasswordField(label='Confirme sua Senha')

    tipo = RadioField(label='Tipo de Usuário', choices=[
      ('cliente', 'Cliente'),
      ('vendedor', 'Vendedor')
    ])

    submit = SubmitField('Enviar')


class GenericFormSemTipo(FlaskForm):
    nome = StringField(label='Digite seu nome de usuário')
    email = StringField(
        label='Digite seu endereço de Email', validators=[Email()])
    telefone = StringField(label='Digite seu telefone',
                           validators=[Length(min=11, max=11)])

    submit = SubmitField('Enviar')


class GenericLoginForm(FlaskForm):
    email = StringField(
        label='Digite seu endereço de Email', validators=[Email()])
    senha = PasswordField(label='Digite sua Senha',
                          validators=[DataRequired()])

    tipo = RadioField(label='Tipo de Usuário', choices=[
        ('cliente', 'Cliente'),
        ('vendedor', 'Vendedor')
    ])

    submit = SubmitField('Enviar')
