from flask import Blueprint, redirect, render_template, request, session
from flask.helpers import url_for

from app import Produto, db, Vendedor, TipoProduto, Usuario
from app.forms.bolo_form import boloForm
from ...models.compra_model import Compra, CompraProduto

from ...forms.compra_form import CompraForm

from datetime import datetime

compra_bp = Blueprint('compra_bp', __name__, url_prefix='/carrinho')

@compra_bp.before_request
def populate():
  print(session.get('cart'))
  if session.get('cart') is None:
    session['cart'] = []

@compra_bp.route('/listar', methods=['GET'])
def listar():
  items = session.get('cart')
  return render_template('carrinho.html', items=items, preco_total=sum([item['preco']*item['quantidade'] for item in items]))

@compra_bp.route('/add', methods=['GET'])
def add():
  cod = request.args.get('cod')
  quantity = request.args.get('quantity')
  if quantity is None:
    quantity = 1
  quantity = int(quantity)
  produto = Produto.query.filter_by(cod=cod).first()
  if produto.quantidade >= 1:
    found = False
    for i, p in enumerate(session['cart']):
      if p['cod'] is produto.cod:
        if p['quantidade'] + quantity <= produto.quantidade and p['quantidade'] + quantity >= 0:
          p['quantidade'] += quantity
          session['cart'][i] = p
          session['cart'] = session['cart']
        found = True
    if not found:
      session['cart'].append(produto.toJSON())
      session['cart'] = session['cart']
  return redirect(url_for('compra_bp.listar'))

@compra_bp.route('/finalizar', methods=['GET', 'POST'])
def finalizar():
  form = CompraForm(request.form)
  items = session.get('cart')
  if form.validate_on_submit():
    compra = Compra()
    usuario = Usuario.query.filter_by(cod=session.get('codusuario')).first()
    compra.usuario = usuario
    compra.pagamento = form.pagamento.data
    compra.data = datetime.now()
    for produto_session in session['cart']:
      produto = Produto.query.filter_by(cod=produto_session['cod']).first()
      produto.quantidade -= produto_session['quantidade']
      lote = CompraProduto()
      lote.produto = produto 
      lote.quantidade = produto_session['quantidade']
      lote.compra = compra
      #compra.lotes.append(lote)
      print(lote)
    db.session.add(compra)
    db.session.commit()
    session['cart'] = []
    return redirect(url_for('home_bp.home'))  
  return render_template('finalizarCompra.html', form=form, route='compra_bp.finalizar',items=items, preco_total=sum([item['preco']*item['quantidade'] for item in items]))

