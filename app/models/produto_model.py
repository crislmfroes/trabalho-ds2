from app import db
#import enum

'''
class TipoProduto(enum.Enum):
    bolo = "Bolo"
    acompanhamento = "Acompanhamento"
'''

#@whooshee.register_model('nome', 'sabor_massa', 'sabor_recheio', 'sabor_cobertura', 'tipo')
class Produto(db.Model):
    __tablename__ = "produtos"
    cod = db.Column(db.Integer, primary_key=True)
    foto = db.Column(db.String(200))
    nome = db.Column(db.String(100))
    quantidade = db.Column(db.Integer)
    sabor_massa = db.Column(db.String(100))
    sabor_recheio = db.Column(db.String(100))
    sabor_cobertura = db.Column(db.String(100))
    #tipo = db.Column(db.Enum(TipoProduto))
    #tipo = db.Column(db.String(100))
    codtipo = db.Column(db.Integer, db.ForeignKey('tipos_produto.cod'))
    preco = db.Column(db.Float())
    codvendedor = db.Column(db.Integer, db.ForeignKey('vendedores.cod'))
    vendedor = db.relationship("Vendedor", backref='produtos')
    tipo = db.relationship("TipoProduto", backref="produtos", cascade="all")


    def salva(self):
        if(self.cod):
            self = db.session.merge(self)
    
    def excluir(self):
        db.session.delete(self)
        db.session.commit()   

    def permitido(self,name):
        return '.' in name and name.split('.')[-1].lower() in ['zip', 'png', 'pdf', 'txt','jpg','jpeg']



    def toJSON(self):
        return {
            'cod': self.cod,
            'nome': self.nome,
            'quantidade': 1,
            'preco': self.preco,
        }






class Arquivo:
    def __init__(self, caminho=None, cod=None):
        self.caminho = caminho
        self.cod = cod
    
    def _get_caminho(self):
        try:
            return self._caminho
        except AttributeError:
            return None
    
    def _set_caminho(self, caminho):
        if type(caminho) != str and caminho is not None:
            raise ValueError()
        self._caminho = caminho
    
    caminho = property(_get_caminho, _set_caminho)

    def _get_cod(self):
        try:
            return self._cod
        except AttributeError:
            return None
    
    def _set_cod(self, cod):
        if type(cod) != int and cod is not None:
            raise ValueError()
        self._cod = cod
    
    cod = property(_get_cod, _set_cod)
    caminho = property(_get_caminho, _set_caminho)
