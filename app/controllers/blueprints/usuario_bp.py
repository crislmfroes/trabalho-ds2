from hashlib import md5

from flask import Blueprint, render_template, request, session
from flask.helpers import url_for
from werkzeug.utils import redirect

from app import Usuario, db, Vendedor
from app.forms.generic_form import GenericForm, GenericLoginForm, GenericFormSemTipo

usuario_bp = Blueprint('generic_bp', __name__, url_prefix='/usuario')


@usuario_bp.route('/cadastrar', methods=['GET', 'POST'])
def cadastro():
    form = GenericForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.tipo.data == 'cliente':
            usuario = Usuario()
        elif form.tipo.data == 'vendedor':
            usuario = Vendedor()
            usuario.admin = False
        usuario.nome = form.nome.data
        usuario.email = form.email.data
        usuario.telefone = form.telefone.data
        usuario.senha = md5(form.senha.data.encode('utf-8')).hexdigest()
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('generic_bp.login'))
    return render_template('cadastro_user.html', form=form, route='generic_bp.cadastro')

@usuario_bp.route('/editar', methods=['GET', 'POST'])
def editar():
    cod = request.args.get('cod')
    print(cod)
    if session.get('isvendedor') == True:
        usuario = Vendedor.query.filter_by(cod=cod).first()
    else:
        usuario = Usuario.query.filter_by(cod=cod).first()
    form = GenericFormSemTipo(request.form)
    if form.validate_on_submit():
        usuario.nome = form.nome.data
        usuario.email = form.email.data
        usuario.telefone = form.telefone.data
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('home_bp.home'))
    form.nome.data = usuario.nome
    form.email.data = usuario.email
    form.telefone.data = usuario.telefone
    return render_template('editar_user.html', form=form, route='generic_bp.editar', cod=cod)


@usuario_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = GenericLoginForm(request.form)
    if form.validate_on_submit():
        if form.tipo.data == 'cliente':
            usuario = Usuario.query.filter(Usuario.email == form.email.data, Usuario.senha == md5(
                form.senha.data.encode('utf-8')).hexdigest()).first()
        elif form.tipo.data == 'vendedor':
            usuario = Vendedor.query.filter(Vendedor.email == form.email.data, Vendedor.senha == md5(
                form.senha.data.encode('utf-8')).hexdigest()).first()
        if usuario is not None:
            session.clear()
            if form.tipo.data == 'cliente':
                session['codusuario'] = usuario.cod
                session['nomeusuario'] = usuario.nome
                session['isvendedor'] = form.tipo.data == False
                return redirect(url_for('home_bp.home'))
            elif form.tipo.data == 'vendedor':
                session.clear()
                session['codvendedor'] = usuario.cod
                session['nomevendedor'] = usuario.nome
                session['isvendedor'] = True
                if usuario.admin == True:
                    session['admin'] = True
                else:
                    session['admin'] = False
                return redirect(url_for('bolo_bp.listar'))
        else:
            return redirect(url_for('generic_bp.cadastro'))
    return render_template('login_user.html', form=form, route='generic_bp.login')


@usuario_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('home_bp.home'))
