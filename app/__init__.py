#import app.seeding
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import sys
import time
from flask import Blueprint, redirect, render_template, request, session
from flask import redirect, url_for
from flask.helpers import url_for
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap

from hashlib import md5


#from flask_whooshee import Whooshee



app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/cakeisnotalie'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'secret'
db = SQLAlchemy(app)
bts = Bootstrap(app)


#whooshee = Whooshee(app)


from app.models.compra_model import Compra
from app.models.produto_model import Produto
from app.models.produto_model import Arquivo
from app.models.usuario_model import Usuario
from app.models.vendedor_model import Vendedor
from app.models.tipo_model import TipoProduto


from app.controllers.blueprints.usuario_bp import usuario_bp
from app.controllers.blueprints.produto_bp import bolo_bp
from app.controllers.blueprints.vendedor_bp import vendedor_bp
from app.controllers.blueprints.home_bp import home_bp
from app.controllers.blueprints.tipo_bp import tipo_bp
from app.controllers.blueprints.compra_bp import compra_bp


@app.route('/cria')
def cria():
    db.create_all()
    if len(TipoProduto.query.all()) == 0:
        db.session.add(TipoProduto(nome='bolo'))
        db.session.add(TipoProduto(nome='doce'))
        db.session.add(TipoProduto(nome='salgado'))
    if Vendedor.query.filter_by(admin=True).first() == None:
        adm = Vendedor()
        adm.nome = 'Cris Lima Froes'
        adm.admin = True
        adm.cep = '123456789'
        adm.email = 'admin@gmail.com'
        adm.senha = md5('GlaDOS'.encode('utf-8')).hexdigest()
        db.session.add(adm)
    db.session.commit()
    return "kjsakldjksal"

@app.route('/drop')
def drop():
    db.drop_all()
    return "kjsakldjksal"

@app.route('/')
def entrar():
    return render_template('entrar.html')
    

'''
if __name__ == '__main__':
    app.secret_key = 'minha chave'
    app.env = 'development'
    app.run(debug = True)
'''
