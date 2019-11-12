from app import db, TipoProduto

if len(TipoProduto.query.all()) == 0:
  db.session.add(TipoProduto(nome='bolo'))
  db.session.add(TipoProduto(nome='doce'))
  db.session.add(TipoProduto(nome='salgado'))
  db.session.commit()