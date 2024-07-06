from flask import Blueprint

pegawai = Blueprint('pegawai', __name__)

from . import views