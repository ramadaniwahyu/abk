from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo

from flask_wtf.file import FileField, FileAllowed

class LoginForm(FlaskForm):
    name = StringField('Nama Pengguna', validators=[DataRequired()])
    password = PasswordField('Kata Kunci', validators=[DataRequired()])
    submit = SubmitField('Masuk')

class PenggunaForm(FlaskForm):
    name = StringField('Nama Pengguna', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    foto = FileField('Upload Foto', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'File gambar saja')])
    submit = SubmitField('Simpan')

class PasswordForm(FlaskForm):
    old_password = PasswordField('Password Lama', validators=[DataRequired()])
    password = PasswordField('Password Baru', validators=[DataRequired()])
    confirm_password = PasswordField('Konfirmasi Password Baru', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Ganti Password')