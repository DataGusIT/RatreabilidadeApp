# app/routes.py

from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Produtor, Propriedade, Lote
import qrcode
import os
from datetime import datetime

# Rota principal que redireciona para a página de registro
@app.route('/')
def index():
    return redirect(url_for('registrar_lote'))

# Rota para exibir a página de sucesso após o registro
@app.route('/lote/<int:lote_id>/sucesso')
def registro_sucesso(lote_id):
    """Exibe a página de sucesso com o QR Code pronto para impressão."""
    lote = Lote.query.get_or_404(lote_id)
    return render_template('registro_sucesso.html', title='Lote Registrado!', lote=lote)

# Rota para o consumidor ver as informações do lote
@app.route('/lote/<int:lote_id>')
def ver_lote(lote_id):
    """Exibe a página pública com as informações de rastreabilidade do lote."""
    lote = Lote.query.get_or_404(lote_id)
    
    # --- ALTERAÇÃO AQUI ---
    # Passamos a data e hora atuais para o template
    hora_atual = datetime.now()
    return render_template('info_lote.html', 
                           title=f'Informações do Lote #{lote_id}', 
                           lote=lote, 
                           hora_atual=hora_atual)

# Rota para registrar um novo lote
@app.route('/registrar', methods=['GET', 'POST'])
def registrar_lote():
    if request.method == 'POST':
        # Obter dados do formulário
        nome_produtor = request.form.get('nome_produtor')
        documento_produtor = request.form.get('documento_produtor')
        nome_propriedade = request.form.get('nome_propriedade')
        cidade = request.form.get('cidade')
        endereco = request.form.get('endereco')
        data_colheita_str = request.form.get('data_colheita')
        validade_str = request.form.get('validade')
        boas_praticas = request.form.get('boas_praticas')

        # Converte as strings de data para objetos date
        data_colheita = datetime.strptime(data_colheita_str, '%Y-%m-%d').date()
        validade = datetime.strptime(validade_str, '%Y-%m-%d').date()
        
        # Lógica para encontrar ou criar Produtor e Propriedade
        produtor = Produtor.query.filter_by(documento=documento_produtor).first()
        if not produtor:
            produtor = Produtor(nome=nome_produtor, documento=documento_produtor)
            db.session.add(produtor)
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

        # Cria o novo lote
        novo_lote = Lote(
            data_colheita=data_colheita,
            validade=validade,
            boas_praticas=boas_praticas,
            propriedade_id=propriedade.id
        )
        db.session.add(novo_lote)
        db.session.commit()

        # --- LINHA CRÍTICA ---
        # Garante que a URL gerada aponte para a função 'ver_lote'
        qr_code_url = url_for('ver_lote', lote_id=novo_lote.id, _external=True)
        # ---------------------
        
        qr_img = qrcode.make(qr_code_url)
        qr_code_filename = f'lote_{novo_lote.id}.png'
        qr_code_path = os.path.join(app.root_path, 'static/qrcodes', qr_code_filename)
        
        os.makedirs(os.path.dirname(qr_code_path), exist_ok=True)
        qr_img.save(qr_code_path)

        # Atualiza o lote com o caminho do QR Code
        novo_lote.qr_code_path = qr_code_filename
        db.session.commit()

        # Redireciona para a página de sucesso
        return redirect(url_for('registro_sucesso', lote_id=novo_lote.id))
        
    return render_template('registro_lote.html', title='Registrar Lote')    