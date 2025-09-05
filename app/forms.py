# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class LoteForm(FlaskForm):
    origem = StringField('Origem (Endereço e Cidade)', validators=[DataRequired()])
    data_colheita = DateField('Data da Colheita', format='%Y-%m-%d', validators=[DataRequired()])
    produtor = StringField('Nome do Produtor', validators=[DataRequired()])
    documento_produtor = StringField('CNPJ/CPF do Produtor')
    validade = DateField('Validade', format='%Y-%m-%d', validators=[DataRequired()])
    boas_praticas = TextAreaField('Boas Práticas Utilizadas')
    submit = SubmitField('Gerar QR Code')