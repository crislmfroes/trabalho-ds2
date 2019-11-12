from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField, StringField, PasswordField, SubmitField, IntegerField, FileField
from wtforms.validators import Email, Required, EqualTo, DataRequired, Length
from flask_bootstrap import Bootstrap

class boloForm(FlaskForm):
    nome = StringField(label='Digite o nome do item')

    saborMassa = StringField(label='Digite o Sabor da Massa')

    saborRecheio = StringField(label='Digite o Sabor do Recheio')

    saborCobertura = StringField(label='Digite o Sabor da Cobertura')

    foto = FileField(label='photo')

    #tipo = StringField(label='Digite o tipo')
    tipo = SelectField(label='Selecione o tipo', coerce=int)

    estoque = IntegerField("Digite a quantidade que há no estoque")

    preco = FloatField("Preço")

    submit = SubmitField('Enviar')

