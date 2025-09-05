# app/routes.py

from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import Produtor, Propriedade, Lote
# AINDA NÃO TEMOS O FORM, VAMOS PEGAR OS DADOS DIRETAMENTE DO REQUEST POR ENQUANTO
# from app.forms import LoteForm 
import qrcode
import os
from datetime import datetime

# NOVA ROTA - A "PORTA DA FRENTE"
@app.route('/')
def index():
    # Redireciona o usuário da rota '/' para a rota '/registrar'
    return redirect(url_for('registrar_lote'))

# NOVA ROTA PARA A PÁGINA DE SUCESSO
@app.route('/lote/<int:lote_id>/sucesso')
def registro_sucesso(lote_id):
    """Exibe a página de sucesso após o registro de um lote."""
    lote = Lote.query.get_or_404(lote_id)
    return render_template('registro_sucesso.html', title='Sucesso!', lote=lote)

# Rota para exibir e registrar lotes
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
            # Commit para que o produtor tenha um ID para a propriedade
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
            # Commit para que a propriedade tenha um ID para o lote
            db.session.commit()

        # Cria o novo lote
        novo_lote = Lote(
            data_colheita=data_colheita,
            validade=validade,
            boas_praticas=boas_praticas,
            propriedade_id=propriedade.id
        )
        db.session.add(novo_lote)
        db.session.commit() # Commit para que o lote tenha um ID

        # Gerar o QR Code
        qr_code_url = url_for('ver_lote', lote_id=novo_lote.id, _external=True)
        qr_img = qrcode.make(qr_code_url)
        qr_code_filename = f'lote_{novo_lote.id}.png'
        qr_code_path = os.path.join(app.root_path, 'static/qrcodes', qr_code_filename)
        
        # --- LINHA NOVA ADICIONADA AQUI ---
        # Garante que o diretório de destino existe antes de tentar salvar o arquivo
        os.makedirs(os.path.dirname(qr_code_path), exist_ok=True)
        # ------------------------------------

        qr_img.save(qr_code_path)

        # Atualiza o lote com o caminho do QR Code
        novo_lote.qr_code_path = qr_code_filename
        db.session.commit()

         # --- MODIFIQUE APENAS ESTA PARTE FINAL ---

        # flash(f'Lote {novo_lote.id} registrado e QR Code gerado com sucesso!') # Podemos remover o flash
        # return redirect(url_for('registrar_lote')) # << LINHA ANTIGA
        
        # vv LINHA NOVA vv
        return redirect(url_for('registro_sucesso', lote_id=novo_lote.id))
        
    return render_template('registro_lote.html', title='Registrar Lote')

@app.route('/lote/<int:lote_id>')
def ver_lote(lote_id):
    # Usando o ORM para buscar o lote pelo ID
    lote = Lote.query.get_or_404(lote_id)
    return render_template('info_lote.html', lote=lote)