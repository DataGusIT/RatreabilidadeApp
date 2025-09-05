# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from markupsafe import Markup
import os

app = Flask(__name__)

# --- CÓDIGO PARA ADICIONAR ---
@app.template_filter('nl2br')
def nl2br(s):
    # Converte quebras de linha em tags <br>
    # Usar Markup garante que o HTML seja renderizado corretamente e com segurança
    return Markup(s.replace('\n', '<br>\n'))

# Configuração da Chave Secreta
app.config['SECRET_KEY'] = 'uma-chave-secreta-bem-segura'

# Configuração do Banco de Dados PostgreSQL
basedir = os.path.abspath(os.path.dirname(__file__))
# Substitua com seus dados do PostgreSQL
# Formato: 'postgresql://usuario:senha@host:porta/database'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
    'postgresql://postgres:2468@localhost/rastreabilidade'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização das extensões
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Importa as rotas e modelos no final para evitar importações circulares
from app import routes, models