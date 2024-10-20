from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_ckeditor import CKEditor



app = Flask(__name__)

app.config[
    "SECRET_KEY"
] = "776e148a01d7ea1f8ca6ac7f62831e4d2ac84ec21f779dd81fb60bca320697fc"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///orca_data_base.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
ckeditor = CKEditor(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
from app import routes
