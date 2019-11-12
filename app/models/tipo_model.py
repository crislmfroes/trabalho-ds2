from app import db

class TipoProduto(db.Model):
  __tablename__ = 'tipos_produto'
  cod = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String(100))

  def serialize(self):
    return {
      'cod': self.cod,
      'nome': self.nome
    }

  def find_or_new(self, cod):
    tipo = self.query.filter_by(cod=cod).first()
    if tipo != None:
      return tipo
    else:
      return TipoProduto()
