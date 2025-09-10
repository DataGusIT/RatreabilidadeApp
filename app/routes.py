# app/routes.py

from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import User, Produtor, Propriedade, Lote
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
import qrcode
import os
from datetime import datetime

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Email ou senha inválidos', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('profile'))
    return render_template('login.html', title='Entrar', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Parabéns, você foi registrado com sucesso!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registrar', form=form)

@app.route('/profile')
@login_required
def profile():
    # Encontra todos os lotes associados ao produtor do usuário logado
    lotes = Lote.query.join(Propriedade).join(Produtor).filter(Produtor.user_id == current_user.id).order_by(Lote.data_criacao.desc()).all()
    return render_template('profile.html', title='Meu Perfil', lotes=lotes)

@app.route('/registrar', methods=['GET', 'POST'])
@login_required
def registrar_lote():
    if request.method == 'POST':
        nome_produtor = request.form.get('nome_produtor')
        documento_produtor = request.form.get('documento_produtor')
        nome_propriedade = request.form.get('nome_propriedade')
        cidade = request.form.get('cidade')
        endereco = request.form.get('endereco')
        data_colheita_str = request.form.get('data_colheita')
        validade_str = request.form.get('validade')
        boas_praticas = request.form.get('boas_praticas')

        data_colheita = datetime.strptime(data_colheita_str, '%Y-%m-%d').date()
        validade = datetime.strptime(validade_str, '%Y-%m-%d').date()
        
        produtor = Produtor.query.filter_by(user_id=current_user.id).first()
        if not produtor:
            produtor = Produtor(nome=nome_produtor, documento=documento_produtor, user_id=current_user.id)
            db.session.add(produtor)
        else:
            # Atualiza os dados do produtor se necessário
            produtor.nome = nome_produtor
            produtor.documento = documento_produtor
        db.session.commit()
        
        propriedade = Propriedade.query.filter_by(nome_propriedade=nome_propriedade, produtor_id=produtor.id).first()
        if not propriedade:
            propriedade = Propriedade(
                nome_propriedade=nome_propriedade,
                cidade=cidade,
                endereco=endereco,
                produtor_id=produtor.id
            )
            db.session.add(propriedade)
        db.session.commit()

        novo_lote = Lote(
            data_colheita=data_colheita,
            validade=validade,
            boas_praticas=boas_praticas,
            propriedade_id=propriedade.id
        )
        db.session.add(novo_lote)
        db.session.commit()

        qr_code_url = url_for('ver_lote', lote_id=novo_lote.id, _external=True)
        
        qr_img = qrcode.make(qr_code_url)
        qr_code_filename = f'lote_{novo_lote.id}.png'
        qr_code_path = os.path.join(app.root_path, 'static/qrcodes', qr_code_filename)
        
        os.makedirs(os.path.dirname(qr_code_path), exist_ok=True)
        qr_img.save(qr_code_path)

        novo_lote.qr_code_path = qr_code_filename
        db.session.commit()

        return redirect(url_for('registro_sucesso', lote_id=novo_lote.id))
        
    # Preenche o formulário com dados do produtor existente, se houver
    produtor = current_user.produtor
    return render_template('registro_lote.html', title='Registrar Lote', produtor=produtor)

@app.route('/lote/<int:lote_id>/sucesso')
@login_required
def registro_sucesso(lote_id):
    lote = Lote.query.get_or_404(lote_id)
    return render_template('registro_sucesso.html', title='Lote Registrado!', lote=lote)

@app.route('/lote/<int:lote_id>')
def ver_lote(lote_id):
    lote = Lote.query.get_or_404(lote_id)
    hora_atual = datetime.now()
    return render_template('info_lote.html', 
                           title=f'Informações do Lote #{lote_id}', 
                           lote=lote, 
                           hora_atual=hora_atual)

