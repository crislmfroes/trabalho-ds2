from flask import session
from app import Produto

class ShoppingCart:
  def __init__(self):
    if session.get('cart') is None:
      self.produtos = []
      session['cart'] = self.produtos
    else:
      for p in session['cart']:
        self.produtos.append(Produto.fromJSON(p))
  def add(self, produto):
    if produto not in self.produtos:
      self.produtos.append(produto)
    else:
      self.produtos[self.produtos.index(produto)] = produto
    session['cart'] = [p.toJSON() for p in self.produtos]