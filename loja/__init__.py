import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_manager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import (IMAGES, UploadSet, configure_uploads,
                           patch_request_class)



basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///minhaloja.db"
app.config["SECRET_KEY"] = 'adsajod09u90q9009f'
# configuring the flask files destination
app.config["UPLOADED_PHOTOS_DEST"] = os.path.join(basedir, 'static/images/')

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)
# initialize the app with the extension
db = SQLAlchemy(app)
criptografia = Bcrypt(app)
login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'clienteLogin'
login_manager.needs_refresh_message_category = 'danger'
login_manager.login_message = 'Favor, fazer o Login para entrar no sistema.'


migrate = Migrate(app, db)
with app.app_context():
    if db.engine.url.drivername == 'sqlite':
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

from loja.admin import rotas
from loja.carrinho import carrinho
from loja.clientes import rotas
from loja.produtos import rotas
