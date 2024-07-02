from datetime import datetime, date, time

from flask_login import UserMixin, current_user
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

    def __repr__(self):
        return '{}'.format(self.name)

class Jabatan(Base):
    name = db.Column(db.String(255), nullable=False)
    desc = db.Column(db.Text)
    pegawai = db.relationship('Pegawai', backref='jabatan')
    ikhtisar_jabatan = db.relationship('Ikhtisar_Jabatan', backref='jabatan')

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
    
class Ikhtisar_Jabatan(Base):
    jabatan_id = db.Column(db.Integer, db.ForeignKey('jabatan.id'))
    uraian_tugas = db.Column(db.Text)
    satuan = db.Column(db.String(100))
    volume = db.Column(db.Float)
    waktu = db.Column(db.Integer)
    peralatan = db.Column(db.Text)
    desc = db.Column(db.Text)