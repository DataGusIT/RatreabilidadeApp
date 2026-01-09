from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[
        DataRequired(message='O e-mail é obrigatório.'), 
        Email(message='Insira um endereço de e-mail válido.')
    ])
    password = PasswordField('Senha', validators=[DataRequired()])
    password2 = PasswordField(
        'Repita a Senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            # Removi o "Por favor," para ser mais direto e moderno
            raise ValidationError('Este nome de usuário já está em uso')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Este endereço de email já está cadastrado')
    
    password = PasswordField('Senha', validators=[
        DataRequired(message='A senha é obrigatória.')
    ])
    
    password2 = PasswordField(
        'Repita a Senha', validators=[
            DataRequired(message='A confirmação de senha é obrigatória.'), 
            EqualTo('password', message='As senhas não coincidem.') 
        ])
    
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