#import app.seeding
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from app import app, Vendedor
from flask import Blueprint
from flask import redirect, url_for
from flask_bootstrap import Bootstrap
from sqlalchemy.exc import ProgrammingError
from app import usuario_bp
from app import bolo_bp
from app import vendedor_bp
from app import home_bp
from app import tipo_bp
from app import compra_bp
import sys
import time
from flask.helpers import url_for
from werkzeug.utils import secure_filename

#import app.seeding




if not os.path.isdir(os.path.join('app/static')):
        os.mkdir(os.path.join('app/static'))
        if not os.path.isdir(os.path.join('app/static', 'uploads')):
            os.mkdir(os.path.join('app/static', 'uploads'))



from app import usuario_bp
from app import bolo_bp
from app import vendedor_bp
from app import home_bp
from app import tipo_bp
from app import compra_bp

app.register_blueprint(usuario_bp)
app.register_blueprint(bolo_bp)
app.register_blueprint(vendedor_bp)
app.register_blueprint(home_bp)
app.register_blueprint(tipo_bp)
app.register_blueprint(compra_bp)


if __name__ == '__main__':
    app.secret_key = 'minha chave'
    app.env = 'development'
    print("oi")
    app.run(debug=True,port=5001)
