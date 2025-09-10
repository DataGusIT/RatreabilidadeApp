from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    produtor = db.relationship('Produtor', backref='user', uselist=False, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Produtor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    documento = db.Column(db.String(20), unique=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # Mude de True para False
    propriedades = db.relationship('Propriedade', backref='produtor', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Produtor {self.nome}>'

class Propriedade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_propriedade = db.Column(db.String(150), nullable=False)
    endereco = db.Column(db.String(250))
    cidade = db.Column(db.String(100))
    produtor_id = db.Column(db.Integer, db.ForeignKey('produtor.id'))
    lotes = db.relationship('Lote', backref='propriedade', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Propriedade {self.nome_propriedade}>'

class Lote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_colheita = db.Column(db.Date, nullable=False)
    validade = db.Column(db.Date, nullable=False)
    boas_praticas = db.Column(db.Text)
    qr_code_path = db.Column(db.String(200))
    data_criacao = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    propriedade_id = db.Column(db.Integer, db.ForeignKey('propriedade.id'))

    def __repr__(self):
        return f'<Lote {self.id}>'