from hashlib import md5

from flask import Blueprint, render_template, request, session
from flask.helpers import url_for
from werkzeug.utils import redirect

from app import Vendedor, db
from app.forms.usuario_form import UsuarioForm, UsuarioLoginForm
from app.forms.vendedor_form import VendedorForm, VendedorLoginForm

vendedor_bp = Blueprint('vendedor_bp', __name__, url_prefix='/vendedor')


@vendedor_bp.route('/cadastrar', methods=['GET', 'POST'])
def cadastro():
    form = VendedorForm(request.form)
    if request.method == 'POST' and form.validate():
        vendedor = Vendedor()
        vendedor.nome = form.nome.data
        vendedor.email = form.email.data
        vendedor.telefone = form.telefone.data
        vendedor.senha = md5(form.senha.data.encode('utf-8')).hexdigest()
        vendedor.cep = form.cep.data
        db.session.add(vendedor)
        db.session.commit()
        return redirect(url_for('vendedor_bp.login'))
    return render_template('cadastro_user.html', form=form, route='vendedor_bp.cadastro')


@vendedor_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = VendedorLoginForm(request.form)
    if request.method == 'POST' and form.validate():
        vendedor = Vendedor.query.filter(Vendedor.email == form.email.data, Vendedor.senha == 
            md5(form.senha.data.encode('utf-8')).hexdigest()).first()
        if vendedor is not None:
            session.clear()
            session['codvendedor'] = vendedor.cod
            session['nomevendedor'] = vendedor.nome
            session['isvendedor'] = True
            if vendedor.admin == True:
                session['admin'] = True
            else:
                session['admin'] = False
            return redirect(url_for('bolo_bp.listar'))
        else:
            return redirect(url_for('vendedor_bp.cadastro'))
    return render_template('login_user.html', form=form, route='vendedor_bp.login')

@vendedor_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('home_bp.home'))
