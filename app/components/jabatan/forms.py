from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField, FloatField
from wtforms.validators import DataRequired

from wtforms_sqlalchemy.fields import QuerySelectField

from app.models import Sasaran_Kinerja, Indikator_Kinerja
class JabatanForm(FlaskForm):
    name = StringField('Nama Jabatan', validators=[DataRequired()])
    desc = TextAreaField('Keterangan')
    submit = SubmitField('Simpan')
    
class SasaranKinerjaForm(FlaskForm):
    name = TextAreaField('Sasaran Kinerja', validators=[DataRequired()])
    desc = TextAreaField('Keterangan')
    submit = SubmitField('Simpan')
    
class IndikatorKinerjaForm(FlaskForm):
    name = TextAreaField('Indikator Kinerja', validators=[DataRequired()])
    desc = TextAreaField('Keterangan')
    submit = SubmitField('Simpan')
    
class IkhtisarJabatanForm(FlaskForm):
    uraian_tugas = TextAreaField('Uraian Tugas', validators=[DataRequired()])
    satuan = SelectField('Satuan', choices=[('', 'Belum ada pilihan'), ('Kegiatan', 'Kegiatan'), ('Dokumen', 'Dokumen')], validators=[DataRequired()])
    volume = FloatField('Volume Kerja', validators=[DataRequired()])
    waktu = IntegerField('Norma Waktu (menit)', validators=[DataRequired()])
    peralatan = TextAreaField('Peralatan yang digunakan')
    desc = TextAreaField('Keterangan')
    submit = SubmitField('Simpan')
    
class IkhtisarJabatanForm(FlaskForm):
    sasaran = QuerySelectField('Sasaran Kinerja', 
                               query_factory=lambda: Sasaran_Kinerja.query.order_by(Sasaran_Kinerja.created_on.asc()).all(), 
                               get_label='name', allow_blank=True, blank_text='Belum ada pilihan')
    indikator = QuerySelectField('Indikator Kinerja', 
                               query_factory=lambda: Indikator_Kinerja.query.order_by(Indikator_Kinerja.created_on.asc()).all(), 
                               get_label='name', allow_blank=True, blank_text='Belum ada pilihan')
    uraian_tugas = TextAreaField('Uraian Tugas', validators=[DataRequired()])
    satuan = SelectField('Satuan', choices=[('', 'Belum ada pilihan'), ('Kegiatan', 'Kegiatan'), ('Dokumen', 'Dokumen')], validators=[DataRequired()])
    volume = FloatField('Volume Kerja', validators=[DataRequired()])
    waktu = IntegerField('Norma Waktu (menit)', validators=[DataRequired()])
    peralatan = TextAreaField('Peralatan yang digunakan')
    desc = TextAreaField('Keterangan')
    submit = SubmitField('Simpan')