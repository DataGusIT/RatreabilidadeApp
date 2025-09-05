# run.py

from app import app, db
from app.models import Produtor, Propriedade, Lote

# Isso torna 'db' e os modelos acessíveis no 'flask shell'
# sem precisar importá-los toda vez. É um facilitador.
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Produtor': Produtor, 'Propriedade': Propriedade, 'Lote': Lote}

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
