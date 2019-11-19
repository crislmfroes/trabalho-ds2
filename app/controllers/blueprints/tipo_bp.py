from app import db, TipoProduto
from app.forms.tipo_form import TipoForm
from flask import Blueprint, redirect, url_for, session, jsonify, render_template, request

tipo_bp = Blueprint('tipo_bp', __name__, url_prefix='/tipo_produto')

@tipo_bp.before_request
def filter():
  if session.get('admin') != True:
    return redirect(url_for('generic_bp.login'))

@tipo_bp.route('/listar', methods=['GET'])
def listar():
  tipos = TipoProduto.query.all()
  return render_template('lista_tipos.html', tipos=tipos)

@tipo_bp.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
  form = TipoForm(request.form)
  if request.method == 'POST' and form.validate():
    tipo = TipoProduto()
    tipo.nome = form.nome.data
    db.session.add(tipo)
    db.session.commit()
    return redirect(url_for('tipo_bp.listar'))
  return render_template('tipo_form.html', form=form, route="tipo_bp.cadastrar")

@tipo_bp.route('/editar', methods=['GET', 'POST'])
def editar():
  cod = request.args.get('cod')
  tipo = TipoProduto.query.filter_by(cod=cod).first()
  form = TipoForm(request.form)
  if form.validate_on_submit():
    tipo.nome = form.nome.data
    db.session.add(tipo)
    db.session.commit()
    return redirect(url_for('tipo_bp.listar'))
  form.nome.data = tipo.nome
  return render_template('tipo_form.html', form=form, route="tipo_bp.editar", cod=cod)

@tipo_bp.route('/excluir', methods=['GET'])
def excluir():
  cod = request.values.get('cod')
  tipo = TipoProduto.query.filter_by(cod=cod).first()
  try:
    db.session.delete(tipo)
    db.session.commit()
  except BaseException as e:
    print(e)
  return redirect(url_for('tipo_bp.listar'))
