from app import db

class Vendedor(db.Model):
    __tablename__ = 'vendedores'
    cod = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(11))
    senha = db.Column(db.String(256))
    admin = db.Column(db.Boolean, default=False)
