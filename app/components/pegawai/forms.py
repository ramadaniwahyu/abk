from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_wtf.file import FileField, FileAllowed, FileRequired

from app.models import Jabatan, Pangkat

class PegawaiForm(FlaskForm):
    name = StringField('Nama Jabatan', validators=[DataRequired()])
    nomor = IntegerField('Nomor Induk Pegawai', validators=[DataRequired()], description='Masukkan 18 digit nomor induk pegawai')
    jabatan = QuerySelectField('Jabatan', query_factory=lambda: Jabatan.query.order_by(Jabatan.created_on.asc()).all(), get_label='name', allow_blank=True, blank_text='Belum ada pilihan')
    pangkat = QuerySelectField('Pangkat', query_factory=lambda: Pangkat.query.order_by(Pangkat.created_on.asc()).all(), get_label='name', allow_blank=True, blank_text='Belum ada pilihan')
    submit = SubmitField('Simpan')
    
class FotoForm(FlaskForm):
    foto = FileField('Foto Pegawai', description='File format JPG, JPEG, atau PNG!', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Simpan')