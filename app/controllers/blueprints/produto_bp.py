from flask import Blueprint, redirect, render_template, request, session
from flask.helpers import url_for

from app import Produto, db, Vendedor, TipoProduto, Compra
from ...models.compra_model import Compra, CompraProduto
from app.forms.bolo_form import boloForm


from flask_sqlalchemy import SQLAlchemy
import flask_sqlalchemy
from sqlalchemy import or_

from app import app
from app import Produto, db, Vendedor, Arquivo
from app.forms.bolo_form import boloForm

from werkzeug.utils import secure_filename
from flask.helpers import url_for
import os
import sys
import time

bolo_bp = Blueprint('bolo_bp', __name__, url_prefix='/bolos')


@bolo_bp.before_request
def filtra():
    if request.endpoint == 'bolo_bp.compras':
        if session.get('isvendedor') or session.get('codusuario') is None:
            return redirect(url_for('usuario_bp.login'))
    else:
        if not session.get('isvendedor'):
            return redirect(url_for('vendedor_bp.login'))
    '''if not session.get('isvendedor') and request.endpoint not in ['bolo_bp.compras']:
        return redirect(url_for('vendedor_bp.login'))
    if not session.get('isvendedor') and session.get('codusuario') and request.endpoint == 'bolo_bp.compras':
        '''

@bolo_bp.route('/listar', methods=['GET'])
def listar():
    bolo = Produto()
    pdao = bolo.query.all()
    return render_template('lista_produtos.html',blistar=pdao)




@bolo_bp.route('/compras')
def compras():
    compras = Compra.query.all()
    return render_template('historico_compras.html', compras=compras)

@bolo_bp.route('/vendas')
def vendas():
    compras = Compra.query.all()
    return render_template('historico_vendas.html', compras=compras)




@bolo_bp.route('/cadastrar', methods=['GET', 'POST'])
def cadastro():
    form = boloForm(request.form)
    form.tipo.choices = [(t.cod, t.nome) for t in TipoProduto.query.all()]
    vendedor = Vendedor.query.filter_by(cod=session.get('codvendedor')).first()
    
    if request.method == 'POST':
        bolo = Produto()
        bolo.nome = form.nome.data
        bolo.sabor_massa = form.saborMassa.data
        bolo.sabor_recheio = form.saborRecheio.data
        bolo.sabor_cobertura = form.saborCobertura.data
        bolo.quantidade = form.estoque.data
        bolo.preco = form.preco.data
        bolo.foto = form.foto.data
        bolo.tipo = TipoProduto.query.filter_by(cod=form.tipo.data).first()
        bolo.vendedor = vendedor
        arquivo = request.files['foto']
        if arquivo and bolo.permitido(arquivo.filename):
            nome_arquivo = secure_filename(arquivo.filename)
            arquivo.save(os.path.join('./app/static', app.config['UPLOAD_FOLDER'], nome_arquivo))
            arquivo_data = Arquivo(caminho=os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo))
            bolo.foto = arquivo_data.caminho

        db.session.add(bolo)
        db.session.commit()
        return redirect("/bolos/cadastrar")
    return render_template('cadastro_produto.html', form=form, route='bolo_bp.cadastro', title='Cadastrar Produto')


@bolo_bp.route('/editar1', methods=['GET', 'POST'])
def editar1():
    cod = request.args.get('cod')
    bolo = Produto.query.filter_by(cod=cod).first()
    form = boloForm(request.form)
    form.tipo.choices = [(t.cod, t.nome) for t in TipoProduto.query.all()]
    if form.validate_on_submit():
        bolo.nome = form.nome.data
        bolo.sabor_massa = form.saborMassa.data
        bolo.sabor_recheio = form.saborRecheio.data
        bolo.sabor_cobertura = form.saborCobertura.data
        bolo.quantidade = form.estoque.data
        bolo.preco = form.preco.data
        bolo.foto = form.foto.data
        bolo.tipo = TipoProduto.query.filter_by(cod=form.tipo.data).first()
        arquivo = request.files['foto']
        if arquivo and bolo.permitido(arquivo.filename):
            nome_arquivo = secure_filename(arquivo.filename)
            arquivo.save(os.path.join('./app/static', app.config['UPLOAD_FOLDER'], nome_arquivo))
            arquivo_data = Arquivo(caminho=os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo))
            bolo.foto = arquivo_data.caminho
        db.session.add(bolo)
        db.session.commit()
        return redirect(url_for('bolo_bp.listar'))
    form.nome.data = bolo.nome
    form.saborMassa.data = bolo.sabor_massa
    form.saborRecheio.data = bolo.sabor_recheio
    form.saborCobertura.data = bolo.sabor_cobertura
    form.estoque.data = bolo.quantidade
    form.preco.data = bolo.preco
    form.tipo.data = bolo.tipo.cod
    return render_template('cadastro_produto.html', form=form, route='bolo_bp.editar1', title='Editar Produto', cod=cod)



@bolo_bp.route('/excluir', methods=['GET'])
def excluir():
    bolo = Produto()
    cod = request.values['cod']
    p = bolo.query.get(cod)
    db.session.delete(p)
    db.session.commit()  
    return redirect("/bolos/listar")


@bolo_bp.route('/editar',  methods=['GET'])
def editar():
    bolo = Produto()
    cod = request.values['cod']
    produto = bolo.query.get(cod)

    return render_template('editar_produto.html',produto=produto, route='bolo_bp.editar')
