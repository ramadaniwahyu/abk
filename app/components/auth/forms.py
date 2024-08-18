from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms_sqlalchemy.fields import QuerySelectField

from app.models import Pegawai

class LoginForm(FlaskForm):
    name = StringField('Nama Pengguna', validators=[DataRequired()])
    password = PasswordField('Kata Kunci', validators=[DataRequired()])
    submit = SubmitField('Masuk')

class UserForm(FlaskForm):
    name = StringField('Nama Pengguna', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Simpan')

class PasswordForm(FlaskForm):
    old_password = PasswordField('Password Lama', validators=[DataRequired()])
    password = PasswordField('Password Baru', validators=[DataRequired()])
    confirm_password = PasswordField('Konfirmasi Password Baru', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Ganti Password')
    
class UserAdminForm(FlaskForm):
    pegawai = QuerySelectField('Pegawai', query_factory=lambda: Pegawai.query.order_by(Pegawai.created_on.asc()).all(), get_label='name', allow_blank=True, blank_text='Belum ada pilihan')
    name = StringField('Nama Pengguna', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Konfirmasi Password', validators=[DataRequired(), EqualTo('password')])
    is_admin = BooleanField('Centing bila pengguna administrator')
    submit = SubmitField('Simpan')