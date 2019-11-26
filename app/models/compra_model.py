from app import db
import enum

'''compra_produto = db.Table(
    'compra_produto',
    db.Column('codcompra', db.Integer, db.ForeignKey('compras.cod'), primary_key=True),
    db.Column('codproduto', db.Integer, db.ForeignKey('produtos.cod'), primary_key=True)
)'''

class CompraProduto(db.Model):
    __tablename__ = 'compra_produto'
    codcompra = db.Column(db.Integer, db.ForeignKey('compras.cod'), primary_key=True)
    codproduto = db.Column(db.Integer, db.ForeignKey('produtos.cod'), primary_key=True)
    quantidade = db.Column(db.Integer)
    preco_unitario = db.Column(db.Float())
    compra = db.relationship('Compra', backref='lotes', cascade="all")
    produto = db.relationship('Produto', backref='lotes', cascade="all, delete-orphan", single_parent=True)

class Compra(db.Model):
    __tablename__ = "compras"
    cod = db.Column(db.Integer, primary_key=True)
    pagamento = db.Column(db.String(100))
    data = db.Column(db.DateTime)
    codusuario = db.Column(db.Integer, db.ForeignKey('usuarios.cod'))
    usuario = db.relationship('Usuario', backref="compras")
    #produtos = db.relationship('Produto', secondary=compra_produto, backref="compras")
