from flask import Blueprint

abk = Blueprint('abk', __name__)

from . import views