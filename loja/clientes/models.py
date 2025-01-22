
import json
from datetime import datetime

from flask_login import UserMixin

from loja import app, db, login_manager


class JsonEncoderDict(db.TypeDecorator):
    impl = db.Text  # Define o tipo base como TEXT

    # Método para converter o valor Python antes de salvar no banco
    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        return json.dumps(value)  # Converte o dicionário em JSON

    # Método para converter o valor JSON do banco para Python
    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        return json.loads(value)  # Converte o JSON em dicionário



@login_manager.user_loader
def carregar_user(user_id):
    return Cadastro.query.get(user_id)

class Cadastro(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True, unique=False)
    username = db.Column(db.String(40), nullable=True, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False)
    country = db.Column(db.String(80), nullable=True, unique=False)
    state = db.Column(db.String(80), nullable=True, unique=False)
    city = db.Column(db.String(80), nullable=True, unique=False)
    contact = db.Column(db.String(20), nullable=True, unique=True)
    address = db.Column(db.String(80), nullable=True, unique=False)
    zipcode = db.Column(db.String(80), nullable=True, unique=False)
    profile = db.Column(db.String(180), unique=False, nullable=False, default='profile.jpg')
    data_criado = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Cadastro %r>' % self.name



class ClientePedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notafiscal = db.Column(db.String(20), nullable=True, unique=False)
    status = db.Column(db.String(20), default='pendente', nullable=True, unique=False)
    cliente_id = db.Column(db.Integer, nullable=False, unique=False)
    data_criado = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    pedido = db.Column(JsonEncoderDict)

    def __repr__(self):
        return '<ClientePedido %r>' % self.notafiscal

with app.app_context():
    db.create_all()