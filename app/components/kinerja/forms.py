from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField, FloatField, DateField
from wtforms.validators import DataRequired
from wtforms.widgets import NumberInput

from wtforms_sqlalchemy.fields import QuerySelectField

from app.models import Pegawai, Perjanjian_Kinerja
class PerjanjianKinerjaForm(FlaskForm):
    tgl = DateField('Tanggal Perjanjian Kinerja', validators=[DataRequired()])
    tahun = StringField('Tahun', validators=[DataRequired()], widget=NumberInput)
    penilai = QuerySelectField('Penilai', validators=[DataRequired()],
                               query_factory=lambda: Pegawai.query.order_by(Pegawai.created_on.asc()).all(), 
                               get_label='name', allow_blank=True, blank_text='Belum ada pilihan')
    atasan_penilai = QuerySelectField('Atasan Penilai', validators=[DataRequired()],
                               query_factory=lambda: Pegawai.query.order_by(Pegawai.created_on.asc()).all(), 
                               get_label='name', allow_blank=True, blank_text='Belum ada pilihan')
    submit = SubmitField('Simpan')
    
class CapaianBulananForm(FlaskForm):
    penilai = QuerySelectField('Penilai', validators=[DataRequired()],
                               query_factory=lambda: Pegawai.query.order_by(Pegawai.created_on.asc()).all(), 
                               get_label='name', allow_blank=True, blank_text='Belum ada pilihan')
    tgl = DateField('Tanggal Penilaian Kinerja Bulanan', validators=[DataRequired()])
    bulan = StringField('Bulan', validators=[DataRequired()], widget=NumberInput)
    submit = SubmitField('Simpan')