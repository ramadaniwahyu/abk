import os
import secrets

from flask import flash, redirect, render_template, url_for, request, current_app
from flask_login import login_required
from . import pegawai
from ...models import Pegawai
from .forms import PegawaiForm, FotoForm
from werkzeug.utils import secure_filename
from ... import db

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@pegawai.route('/data-pegawai', methods=['GET', 'POST'])
@login_required
def list():
    list = enumerate(Pegawai.query.all(), start=1)
    form = PegawaiForm()
    if form.validate_on_submit():
        new = Pegawai(
            name = form.name.data,
            nomor = form.nomor.data,
            jabatan = form.jabatan.data,
            pangkat = form.pangkat.data,
            satker  = form.satker.data
            )
        db.session.add(new)
        db.session.commit()
        flash('Data berhasil ditambahkan')
        return redirect(url_for('pegawai.list'))
    
    return render_template('pegawai/list.html', form=form, list=list, title='Daftar Pegawai')

@pegawai.route('/data-pegawai/<id>', methods=['GET', 'POST'])
@login_required
def view(id):
    item = Pegawai.query.get_or_404(id)
    form = FotoForm()
    if form.validate_on_submit():
        file = request.files['foto']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ext_type = filename.split('.')[-1]
            file_name = secrets.token_hex(16)
            storage_filename = str(file_name) + '.' +ext_type
            old_name = item.foto
            item.foto = storage_filename
            
            filepath = os.path.join(current_app.root_path, 'assets/uploads/foto', storage_filename) 
            file.save(filepath)
            
            if old_name:
                try: 
                    del_old = os.path.join(current_app.root_path, 'assets/uploads/foto', old_name)
                    os.remove(del_old)
                except FileNotFoundError:
                    pass
        
            db.session.commit()
            flash('Data berhasil diubah')
            return redirect(url_for('pegawai.view', id=id))
    
    return render_template('pegawai/view.html', form=form, item=item, title='Lihat Data Pegawai')
    
@pegawai.route('/data-pegawai/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    item = Pegawai.query.get_or_404(id)
    form =  PegawaiForm(obj=item)
    if form.validate_on_submit():
        item.name = form.name.data
        item.nomor = form.nomor.data
        item.jabatan = form.jabatan.data
        item.pangkat = form.pangkat.data
        item.satker = form.satker.data
        
        db.session.commit()
        flash('Data berhasil diubah')
        return redirect(url_for('pegawai.view', id=id))
    
    return render_template('pegawai/edit.html', form=form, item=item, title='Ubah Data Pegawai')

@pegawai.route('/data-pegawai/<id>/hapus', methods=['GET', 'POST'])
@login_required
def delete(id):
    item = Pegawai.query.get_or_404(id)
    if item.foto is not None :
        try:
            filepath = os.path.join(current_app.root_path, 'assets/uploads/foto', item.foto)
            os.remove(filepath)
        except FileNotFoundError:
            pass
        
    db.session.delete(item)
    db.session.commit()
    flash('Data berhasil dihapus')
    return redirect(url_for('pegawai.list'))