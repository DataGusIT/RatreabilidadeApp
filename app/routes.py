# app/routes.py

from flask import render_template, request, redirect, url_for, flash, abort
from app import app, db
from app.models import User, Produtor, Propriedade, Lote
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
import qrcode
import os
from datetime import datetime
from sqlalchemy.exc import IntegrityError 

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
        flash('Parabéns, você foi registrado com sucesso!', 'register_success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registrar', form=form)

@app.route('/profile')
@login_required
def profile():
    # Encontra todos os lotes criados pelo usuário logado
    lotes = Lote.query.filter_by(user_id=current_user.id).order_by(Lote.data_criacao.desc()).all()
    return render_template('profile.html', title='Meu Perfil', lotes=lotes)

@app.route('/registrar', methods=['GET', 'POST'])
@login_required
def registrar_lote():
    if request.method == 'POST':
        nome_produtor = request.form.get('nome_produtor')
        documento_produtor = request.form.get('documento_produtor')
        nome_propriedade = request.form.get('nome_propriedade')
        
        # --- VERIFICAÇÃO DE SEGURANÇA E UNICIDADE ---
        # Procura se esse documento já existe no banco
        produtor_existente = Produtor.query.filter_by(documento=documento_produtor).first()
        
        if produtor_existente and produtor_existente.user_id != current_user.id:
            # Se o documento existe e pertence a OUTRO usuário
            flash(f'O CPF/CNPJ {documento_produtor} já está cadastrado por outro usuário. Verifique os dados.', 'danger')
            return redirect(url_for('registrar_lote'))
        
        # 1. Gerenciar o perfil de Produtor do Usuário atual
        try:
            if not current_user.produtor:
                produtor = Produtor(
                    nome=nome_produtor, 
                    documento=documento_produtor, 
                    user_id=current_user.id
                )
                db.session.add(produtor)
            else:
                produtor = current_user.produtor
                produtor.nome = nome_produtor
                produtor.documento = documento_produtor
            
            db.session.commit()
            
        except IntegrityError:
            db.session.rollback()
            flash('Erro de duplicidade: Este documento já está em uso.', 'danger')
            return redirect(url_for('registrar_lote'))

        # 2. Gerenciar a Propriedade
        propriedade = Propriedade.query.filter_by(nome_propriedade=nome_propriedade, produtor_id=produtor.id).first()
        if not propriedade:
            propriedade = Propriedade(
                nome_propriedade=nome_propriedade,
                cidade=request.form.get('cidade'),
                endereco=request.form.get('endereco'),
                produtor_id=produtor.id
            )
            db.session.add(propriedade)
            db.session.commit()

        # 3. Criar o Lote
        novo_lote = Lote(
            data_colheita=datetime.strptime(request.form.get('data_colheita'), '%Y-%m-%d').date(),
            validade=datetime.strptime(request.form.get('validade'), '%Y-%m-%d').date(),
            boas_praticas=request.form.get('boas_praticas'),
            propriedade_id=propriedade.id,
            user_id=current_user.id
        )
        db.session.add(novo_lote)
        db.session.commit() # Salvamos para o banco gerar o ID

        # --- LÓGICA DO QR CODE CORRIGIDA ---
        qr_code_url = url_for('ver_lote', lote_id=novo_lote.id, _external=True)
        qr_img = qrcode.make(qr_code_url)
        qr_code_filename = f'lote_{novo_lote.id}.png'
        
        # MUDANÇA AQUI: Usamos app.static_folder para apontar para a raiz/static
        qr_code_folder = os.path.join(app.static_folder, 'qrcodes')
        
        os.makedirs(qr_code_folder, exist_ok=True)
        qr_img.save(os.path.join(qr_code_folder, qr_code_filename))
        
        novo_lote.qr_code_path = qr_code_filename
        db.session.commit()

        return redirect(url_for('registro_sucesso', lote_id=novo_lote.id))

    return render_template('registro_lote.html', title='Registrar Lote', produtor=current_user.produtor)

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

@app.route('/lote/<int:lote_id>/delete', methods=['POST'])
@login_required
def delete_lote(lote_id):
    lote = Lote.query.get_or_404(lote_id)

    if lote.user_id != current_user.id:
        abort(403)

    if lote.qr_code_path:
        try:
            # MUDANÇA AQUI: Usamos app.static_folder
            qr_code_full_path = os.path.join(app.static_folder, 'qrcodes', lote.qr_code_path)
            if os.path.exists(qr_code_full_path):
                os.remove(qr_code_full_path)
        except OSError as e:
            print(f"Erro ao deletar o arquivo: {e}")

    db.session.delete(lote)
    db.session.commit()
    flash('Lote excluído com sucesso!', 'success')
    return redirect(url_for('profile'))

@app.route('/logout')
def logout():
    logout_user()
    # Adicione esta linha com a categoria 'logout_success'
    flash('Você saiu com segurança. Até logo!', 'logout_success') 
    return redirect(url_for('index'))