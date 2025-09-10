from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    password2 = PasswordField(
        'Repita a Senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Por favor, use um nome de usuário diferente.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Por favor, use um endereço de email diferente.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')

class LoteForm(FlaskForm):
    # Este formulário permanece o mesmo
    origem = StringField('Origem (Endereço e Cidade)', validators=[DataRequired()])
    data_colheita = DateField('Data da Colheita', format='%Y-%m-%d', validators=[DataRequired()])
    produtor = StringField('Nome do Produtor', validators=[DataRequired()])
    documento_produtor = StringField('CNPJ/CPF do Produtor')
    validade = DateField('Validade', format='%Y-%m-%d', validators=[DataRequired()])
    boas_praticas = TextAreaField('Boas Práticas Utilizadas')
    submit = SubmitField('Gerar QR Code')