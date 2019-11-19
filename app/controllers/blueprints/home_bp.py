from flask import Blueprint, redirect, render_template, request, session
from flask.helpers import url_for

from app import Produto, db, TipoProduto
from app.forms.bolo_form import boloForm
from app.forms.busca_form import BuscaForm

home_bp = Blueprint('home_bp', __name__, url_prefix='/home')



@home_bp.route('/pesquisar', methods=['GET', 'POST'])
def pesquisar():
    form = BuscaForm(request.form)
    p = request.form["pesquisa"]
    filtro = request.form["filtro"]
    tipo = request.form["tipo"]
      

    if tipo=="todostipos":
        if filtro=="massa":
          list=Produto.query.filter(Produto.sabor_massa.like('%'+p+'%')).all()
        
        if filtro=="produto":
          list=Produto.query.filter(Produto.nome.like('%'+p+'%')).all()
        
        if filtro=="recheio":
          list=Produto.query.filter(Produto.sabor_recheio.like('%'+p+'%')).all()

        if filtro=="cobertura":
          list=Produto.query.filter(Produto.sabor_cobertura.like('%'+p+'%')).all()

        if filtro=="tudo":
          list=Produto.query.all()

    else:

        if filtro=="massa":
          list=Produto.query.filter(Produto.sabor_massa.like('%'+p+'%')).join(Produto.tipo).filter(TipoProduto.nome.like('%'+tipo+'%')).all()
        
        if filtro=="produto":
          list=Produto.query.filter(Produto.nome.like('%'+p+'%')).filter(Produto.tipo.nome.like('%'+tipo+'%')).all()
        
        if filtro=="recheio":
          list=Produto.query.filter(Produto.sabor_recheio.like('%'+p+'%')).filter(Produto.tipo.nome.like('%'+tipo+'%')).all()

        if filtro=="cobertura":
          list=Produto.query.filter(Produto.sabor_cobertura.like('%'+p+'%')).filter(Produto.tipo.nome.like('%'+tipo+'%')).all()

        if filtro=="tudo":
          list=Produto.query.filter(Produto.tipo.nome.like('%'+tipo+'%')).all()

      
    return render_template('home.html', form=form, bolos=list, route=request.endpoint)


    #list=Produto.query.filter(Produto.nome==p).all()
    #return render_template('home.html',form=form, bolos=list, route=request.endpoint)





@home_bp.route('/', methods=['GET', 'POST'])
def home():
  tipos=TipoProduto.query.all()
  form = BuscaForm(request.form)
  if form.validate_on_submit():
    term = form.termo.data
    bolos = Produto.query.whooshee_search(
        term).order_by(Produto.cod.desc()).all()
    #tipos = [(t.cod, t.nome) for t in TipoProduto.query.all()]
    return render_template('home.html', form=form, bolos=bolos, route=request.endpoint)
  bolos = Produto.query.all()
  return render_template('home.html', form=form, bolos=bolos, route=request.endpoint, tipos=tipos)