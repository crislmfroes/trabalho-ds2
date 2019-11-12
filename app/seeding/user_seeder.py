from app import db, Vendedor
from hashlib import md5

if Vendedor.query.filter_by(admin=True).first() == None:
    adm = Vendedor()
    adm.nome = 'Cris Lima Froes'
    adm.admin = True
    adm.cep = '123456789'
    adm.email = 'admin@gmail.com'
    adm.senha = md5('GlaDOS'.encode('utf-8')).hexdigest()
    db.session.add(adm)
    db.session.commit()
