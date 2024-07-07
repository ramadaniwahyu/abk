from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField, FloatField
from wtforms.validators import DataRequired

class JabatanForm(FlaskForm):
    name = StringField('Nama Jabatan', validators=[DataRequired()])
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