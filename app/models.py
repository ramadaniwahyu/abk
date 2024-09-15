from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import declared_attr

from  app import db, login_manager


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

class User(Base, UserMixin):
    name = db.Column(db.String(60))
    password_hash = db.Column(db.String(500))
    email =  db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    pegawai_id = db.Column(db.Integer, db.ForeignKey('pegawai.id'))

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password  
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '{}'.format(self.name)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Pegawai(Base):
    name = db.Column(db.String(100))
    nomor = db.Column(db.String(60))
    foto = db.Column(db.String(200))
    jabatan_id = db.Column(db.Integer, db.ForeignKey('jabatan.id'))
    satker_id = db.Column(db.Integer, db.ForeignKey('satker.id'))
    pangkat_id = db.Column(db.Integer, db.ForeignKey('pangkat.id'))
    user = db.relationship('User', backref='pegawai')

    def __repr__(self):
        return '{}'.format(self.name)

class Jabatan(Base):
    name = db.Column(db.String(255), nullable=False)
    desc = db.Column(db.Text)
    level = db.Column(db.Integer, default=100)
    pegawai = db.relationship('Pegawai', backref='jabatan')
    ikhtisar_jabatan = db.relationship('Ikhtisar_Jabatan', backref='jabatan')
    sasaran_kinerja = db.relationship('Sasaran_Kinerja', backref='jabatan')
    indikator_kinerja = db.relationship('Indikator_Kinerja', backref='jabatan')

    def __repr__(self):
        return '{}'.format(self.name)

class Pangkat(Base):
    name = db.Column(db.String(255), nullable=False)
    gol = db.Column(db.String(100))
    ruang = db.Column(db.String(100))
    pegawai = db.relationship('Pegawai', backref='pangkat')

    def __repr__(self):
        return '{}'.format(self.name)

class Satker(Base):
    name = db.Column(db.String(255), nullable=False)
    desc = db.Column(db.Text)
    pegawai = db.relationship('Pegawai', backref='satker')

    def __repr__(self):
        return '{}'.format(self.name)
    
class Sasaran_Kinerja(Base):
    jabatan_id = db.Column(db.Integer, db.ForeignKey('jabatan.id'))
    name = db.Column(db.Text)
    desc = db.Column(db.Text)
    indikator_kinerja = db.relationship('Indikator_Kinerja', backref='sasaran_kinerja')
    
    def __repr__(self):
        return '{}'.format(self.name)
    
class Indikator_Kinerja(Base):
    jabatan_id = db.Column(db.Integer, db.ForeignKey('jabatan.id'))
    sasaran_kinerja_id = db.Column(db.Integer, db.ForeignKey('sasaran_kinerja.id'))
    name = db.Column(db.Text)
    desc = db.Column(db.Text)
    ikhtisar_jabatan = db.relationship('Ikhtisar_Jabatan', backref='indikator_kinerja')
    
    def __repr__(self):
        return '{}'.format(self.name)
    
class Ikhtisar_Jabatan(Base):
    jabatan_id = db.Column(db.Integer, db.ForeignKey('jabatan.id'))
    indikator_kinerja_id = db.Column(db.Integer, db.ForeignKey('indikator_kinerja.id'))
    uraian_tugas = db.Column(db.Text)
    satuan = db.Column(db.String(100))
    volume = db.Column(db.Float)
    waktu = db.Column(db.Integer)
    peralatan = db.Column(db.Text)
    desc = db.Column(db.Text)
    realisasi_kinerja = db.relationship('Realisasi_Kinerja', backref='ikhtisar_jabatan')
    
    def __repr__(self):
        return '{}'.format(self.uraian_tugas)
    
class Perjanjian_Kinerja(Base):
    tgl = db.Column(db.Date)
    tahun = db.Column(db.String(10))
    pegawai_id = db.Column(db.Integer, db.ForeignKey('pegawai.id'))
    penilai_id = db.Column(db.Integer, db.ForeignKey('pegawai.id'))
    atasan_penilai_id = db.Column(db.Integer, db.ForeignKey('pegawai.id'))
    pegawai = db.relationship('Pegawai', foreign_keys='Perjanjian_Kinerja.pegawai_id', lazy='joined')
    penilai = db.relationship('Pegawai', foreign_keys='Perjanjian_Kinerja.penilai_id', lazy='joined')
    atasan_penilai = db.relationship('Pegawai', foreign_keys='Perjanjian_Kinerja.atasan_penilai_id', lazy='joined')
    capaian_bulanan = db.relationship('Capaian_Bulanan', backref='perjanjian_kinerja')
    
    def __repr__(self):
        return '{}'.format(self.tahun)
    
class Capaian_Bulanan(Base):
    pegawai_id = db.Column(db.Integer, db.ForeignKey('pegawai.id'))
    penilai_id = db.Column(db.Integer, db.ForeignKey('pegawai.id'))
    perjanjian_kinerja_id = db.Column(db.Integer, db.ForeignKey('perjanjian_kinerja.id'))
    tgl = db.Column(db.Date)
    bulan = db.Column(db.String(20))
    pegawai = db.relationship('Pegawai', foreign_keys='Capaian_Bulanan.pegawai_id', lazy='joined')
    penilai = db.relationship('Pegawai', foreign_keys='Capaian_Bulanan.penilai_id', lazy='joined')
    realisasi_kinerja = db.relationship('Realisasi_Kinerja', backref='capaian_bulanan')
    
    def __repr__(self):
        return '{}'.format(self.bulan)
    
class Realisasi_Kinerja(Base):
    capaian_bulanan_id = db.Column(db.Integer, db.ForeignKey('capaian_bulanan.id'))
    ikhtisar_jabatan_id = db.Column(db.Integer, db.ForeignKey('ikhtisar_jabatan.id'))
    target = db.Column(db.Integer)
    realisasi = db.Column(db.Integer)
    eviden = db.Column(db.Text)
    
    def __repr__(self):
        return '{}'.format(self.realisasi)