from flask import Blueprint, redirect, render_template, request, session
from flask.helpers import url_for

from app import Produto, db, TipoProduto, Vendedor
from app.forms.bolo_form import boloForm
from app.forms.busca_form import BuscaForm

from sqlalchemy import and_

home_bp = Blueprint('home_bp', __name__, url_prefix='/home')




@home_bp.route('/pesquisar', methods=['GET', 'POST'])
def pesquisar():
    form = BuscaForm(request.form)
    p = request.form["pesquisa"]
    v = request.form["vendedor"]
    tipos=TipoProduto.query.all()

    t = request.form["tipos"]
    checkados = request.form.getlist('checkbox')

    nome=Produto.nome != 'NULL'
    massa=Produto.sabor_massa != 'NULL'
    recheio=Produto.sabor_recheio != 'NULL'
    cobertura=Produto.sabor_cobertura != 'NULL'

    
    for c in checkados:
      
      infobolo = c #massa, #recheio, #cobertura
      
      if infobolo=="nome":
        nome=Produto.nome.like('%'+p+'%')

      if infobolo=="massa":
        massa=Produto.sabor_massa.like('%'+p+'%')
      
      if infobolo=="recheio":
        recheio=Produto.sabor_recheio.like('%'+p+'%')
      
      if infobolo=="cobertura":
        cobertura=Produto.sabor_cobertura.like('%'+p+'%')
         

    if v=="umvendedor":
      nv=request.form["nomevendedor"]

      if (t=="todostipos"): #qualquer tipo
        list=Produto.query.filter(nome,massa,recheio,cobertura).join(Produto.vendedor).filter(Vendedor.nome.like('%'+nv+'%'))

        return render_template('home.html',form=form,tipos=tipos, bolos=list, route=request.endpoint)
      
      else: #tipo especifico
        list=Produto.query.filter(nome,massa,recheio,cobertura).join(Produto.tipo).filter(TipoProduto.nome.like('%'+t+'%')).join(Produto.vendedor).filter(Vendedor.nome.like('%'+nv+'%'))
        return render_template('home.html',form=form,tipos=tipos, bolos=list, route=request.endpoint)
    else:

      if (t=="todostipos"): #qualquer tipo
        list=Produto.query.filter(nome,massa,recheio,cobertura)
        return render_template('home.html',form=form,tipos=tipos, bolos=list, route=request.endpoint)
      
      else: #tipo especifico
        list=Produto.query.filter(nome,massa,recheio,cobertura).join(Produto.tipo).filter(TipoProduto.nome.like('%'+t+'%'))
        return render_template('home.html',form=form,tipos=tipos, bolos=list, route=request.endpoint)  
    
    


    
    
    
    #list=aux.all()
    #return render_template('home.html',form=form,tipos=tipos, bolos=list, route=request.endpoint)


@home_bp.route('/', methods=['GET', 'POST'])
def home():
  tipos=TipoProduto.query.all()
  form = BuscaForm(request.form)
  if form.validate_on_submit():
    term = form.termo.data
    bolos = Produto.query.whooshee_search(
        term).order_by(Produto.cod.desc()).all()
    #tipos = [(t.cod, t.nome) for t in TipoProduto.query.all()]
    return render_template('home.html', form=form, bolos=bolos,tipos=tipos, route=request.endpoint)
  bolos = Produto.query.all()
  return render_template('home.html', form=form, bolos=bolos, route=request.endpoint, tipos=tipos)