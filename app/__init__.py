from flask import Flask, render_template, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
login_manager = LoginManager()

app = Flask(__name__)

# Configuration of application, see configuration.py, choose one and uncomment.
#app.config.from_object('config.ProductionConfig')
app.config.from_object('config.DevelopmentConfig')
#app.config.from_object('config.TestingConfig')

Bootstrap(app)
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "auth.login"
login_manager.login_message = 'Silahkan login untuk akses halaman ini.'
migrate = Migrate(app, db)

from app import models

@app.route('/')
def hello():
    return redirect(url_for('index'))

@app.route('/beranda', methods=['GET', 'POST'])
@login_required
def index():
	return render_template('/index.html', title='Beranda')

@app.route('/<path:resource>')
def serveStaticResource(resource):
	return send_from_directory('assets/', resource)

# Register blueprints
from app.components.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from app.components.jabatan import jabatan as jabatan_blueprint
app.register_blueprint(jabatan_blueprint)

from app.components.pegawai import pegawai as pegawai_blueprint
app.register_blueprint(pegawai_blueprint)

from app.components.abk import abk as abk_blueprint
app.register_blueprint(abk_blueprint)

# Errors Handling
@app.errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html', title='Akses Ditolak'), 403

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html', title='Halaman Tidak Ditemukan'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html', title='Server Internal Eror'), 500
