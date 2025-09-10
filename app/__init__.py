# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from markupsafe import Markup
import os

app = Flask(__name__)

@app.template_filter('nl2br')
def nl2br(s):
    return Markup(s.replace('\n', '<br>\n'))

app.config['SECRET_KEY'] = 'uma-chave-secreta-bem-segura'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
    'postgresql://postgres:2468@localhost/rastreabilidade'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Rota para a qual usuários não logados são redirecionados
login_manager.login_message = "Por favor, faça o login para acessar esta página."
login_manager.login_message_category = "info"

from app import routes, models

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))