from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField, FloatField, DateField
from wtforms.validators import DataRequired
from wtforms.widgets import NumberInput

from wtforms_sqlalchemy.fields import QuerySelectField

from app.models import Pegawai, Perjanjian_Kinerja, Ikhtisar_Jabatan, Sasaran_Kinerja, Indikator_Kinerja
class PerjanjianKinerjaForm(FlaskForm):
    tgl = DateField('Tanggal Perjanjian Kinerja', validators=[DataRequired()])
    tahun = StringField('Tahun', validators=[DataRequired()], widget=NumberInput())
    penilai = QuerySelectField('Penilai', validators=[DataRequired()],
                               query_factory=lambda: Pegawai.query.order_by(Pegawai.created_on.asc()).all(), 
                               get_label='name', allow_blank=True, blank_text='Belum ada pilihan')
    atasan_penilai = QuerySelectField('Atasan Penilai', validators=[DataRequired()],
                               query_factory=lambda: Pegawai.query.order_by(Pegawai.created_on.asc()).all(), 
                               get_label='name', allow_blank=True, blank_text='Belum ada pilihan')
    submit = SubmitField('Simpan')
    
class CapaianBulananForm(FlaskForm):
    # penilai = QuerySelectField('Penilai', validators=[DataRequired()],
    #                            query_factory=lambda: Pegawai.query.order_by(Pegawai.created_on.asc()).all(), 
    #                            get_label='name', allow_blank=True, blank_text='Belum ada pilihan')
    tgl = DateField('Tanggal Penilaian Kinerja Bulanan', validators=[DataRequired()])
    # bulan = StringField('Bulan', validators=[DataRequired()], widget=NumberInput())
    bulan = SelectField("Bulan Penilaian Kinerja", choices=[("", "Belum ada pilihan"), ("Januari", "Januari"), ("Februari", "Februari"),
                                                            ("Maret", "Maret"), ("April", "April"), ("Mei", "Mei"),
                                                            ("Juni", "Juni"), ("Juli", "Juli"), ("Agustus", "Agustus"),
                                                            ("September", "September"), ("Oktober", "Oktober"), ("November", "November"),
                                                            ("Desember", "Desember")])
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
    sasaran = QuerySelectField('Sasaran Kinerja', validators=[DataRequired()],
                               query_factory=lambda: Sasaran_Kinerja.query.order_by(Sasaran_Kinerja.created_on.asc()).all(), 
                               get_label='name', allow_blank=True, blank_text='Belum ada pilihan')
    indikator = QuerySelectField('Indikator Kinerja', validators=[DataRequired()],
                               query_factory=lambda: Indikator_Kinerja.query.order_by(Indikator_Kinerja.created_on.asc()).all(), 
                               get_label='name', allow_blank=True, blank_text='Belum ada pilihan')
    uraian_tugas = TextAreaField('Uraian Tugas', validators=[DataRequired()], render_kw={"rows": 5})
    satuan = SelectField('Satuan', choices=[('', 'Belum ada pilihan'), ('Kegiatan', 'Kegiatan'), ('Dokumen', 'Dokumen')], validators=[DataRequired()])
    volume = FloatField('Volume Kerja', validators=[DataRequired()])
    waktu = IntegerField('Norma Waktu (menit)', validators=[DataRequired()])
    peralatan = TextAreaField('Peralatan yang digunakan', render_kw={"rows": 5})
    desc = TextAreaField('Keterangan', render_kw={"rows": 5})
    submit = SubmitField('Simpan')
class RealisasiKinerjaForm(FlaskForm):
    sasaran = QuerySelectField('Sasaran Kinerja', validators=[DataRequired()],
                               query_factory=lambda: Sasaran_Kinerja.query.order_by(Sasaran_Kinerja.created_on.asc()).all(), 
                               get_label='name', allow_blank=True, blank_text='Belum ada pilihan')
    indikator = QuerySelectField('Indikator Kinerja', validators=[DataRequired()],
                               query_factory=lambda: Indikator_Kinerja.query.order_by(Indikator_Kinerja.created_on.asc()).all(), 
                               get_label='name', allow_blank=True, blank_text='Belum ada pilihan')
    uraian = QuerySelectField('Uraian Tugas', validators=[DataRequired()],
                               query_factory=lambda: Ikhtisar_Jabatan.query.order_by(Ikhtisar_Jabatan.created_on.asc()).all(), 
                               get_label='uraian_tugas', allow_blank=True, blank_text='Belum ada pilihan')
    target = IntegerField('Target Capaian', validators=[DataRequired()])
    realisasi = IntegerField('Realisasi Capaian', validators=[DataRequired()])
    submit = SubmitField('Simpan')