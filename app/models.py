# app/models.py

from app import db
from datetime import datetime

class Produtor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    documento = db.Column(db.String(20), unique=True, index=True) # CPF ou CNPJ
    propriedades = db.relationship('Propriedade', backref='produtor', lazy='dynamic')

    def __repr__(self):
        return f'<Produtor {self.nome}>'

class Propriedade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_propriedade = db.Column(db.String(150), nullable=False)
    endereco = db.Column(db.String(250))
    cidade = db.Column(db.String(100))
    produtor_id = db.Column(db.Integer, db.ForeignKey('produtor.id'))
    lotes = db.relationship('Lote', backref='propriedade', lazy='dynamic')

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