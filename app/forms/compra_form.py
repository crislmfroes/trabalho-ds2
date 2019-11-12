from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField


class CompraForm(FlaskForm):
  pagamento = SelectField('Pagamento', choices=[
    ('boleto', 'Boleto'),
    ('cartao', 'Cartão')
  ])
  submit = SubmitField("Finalizar Compra")
