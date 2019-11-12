from hashlib import md5

from flask import Blueprint, render_template, request, session
from flask.helpers import url_for
from werkzeug.utils import redirect

from app import Usuario, db
from app.forms.usuario_form import UsuarioForm, UsuarioLoginForm

usuario_bp = Blueprint('usuario_bp', __name__, url_prefix='/usuario')

@usuario_bp.route('listar', methods=['GET'])
def listar():
    usuarios = Usuario.query.all()
    return 'Ok'

@usuario_bp.route('/cadastrar', methods=['GET', 'POST'])
def cadastro():
    form = UsuarioForm(request.form)
    if request.method == 'POST' and form.validate():
        usuario = Usuario()
        usuario.nome = form.nome.data
        usuario.email = form.email.data
        usuario.telefone = form.telefone.data
        usuario.admin = False
        usuario.senha = md5(form.senha.data.encode('utf-8')).hexdigest()
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('usuario_bp.login'))
    return render_template('cadastro_user.html', form=form, route='usuario_bp.cadastro')

@usuario_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = UsuarioLoginForm(request.form)
    if form.validate_on_submit():
        usuario = Usuario.query.filter(Usuario.email==form.email.data, Usuario.senha==md5(form.senha.data.encode('utf-8')).hexdigest()).first()
        if usuario is not None:
            session.clear()
            session['codusuario'] = usuario.cod
            session['nomeusuario'] = usuario.nome
            session['isvendedor'] = False
            return redirect(url_for('home_bp.home'))
        else:
            return redirect(url_for('usuario_bp.cadastro'))
    return render_template('login_user.html', form=form, route='usuario_bp.login')

@usuario_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('home_bp.home'))
