from app import db

class Usuario(db.Model):
    __tablename__ = "usuarios"
    cod = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    telefone = db.Column(db.String(11))
    email = db.Column(db.String(100))
    senha = db.Column(db.String(256))
