from flask import flash, redirect, render_template, url_for, request, session, app
from flask_login import login_required
from . import jabatan
from ...models import Jabatan, Ikhtisar_Jabatan
from .forms import JabatanForm, IkhtisarJabatanForm
from ... import db


@jabatan.route('/data-jabatan', methods=['GET', 'POST'])
@login_required
def list():
    list = enumerate(Jabatan.query.all(), start=1)
    form = JabatanForm()
    if form.validate_on_submit():
        newJabatan = Jabatan(name=form.name.data, desc=form.desc.data)
        db.session.add(newJabatan)
        db.session.commit()
        
        flash('Data Jabatan berhasil ditambahkan', category='success')
        return redirect(url_for('jabatan.list'))
    
    return render_template('jabatan/list.html', list=list, form=form, title='Data Jabatan')

@jabatan.route('/data-jabatan/<id>', methods=['GET', 'POST'])
@login_required
def view(id):
    item = Jabatan.query.get_or_404(id)
    uraian = Ikhtisar_Jabatan.query.filter(Ikhtisar_Jabatan.jabatan_id==item.id).all()
    total = 0
    for i in uraian:
        beban = i.volume * i.waktu
        total = total + beban
    form = IkhtisarJabatanForm()
    list = enumerate(uraian, start=1)
    if form.validate_on_submit():
        new = Ikhtisar_Jabatan(
            jabatan_id = item.id,
            uraian_tugas = form.uraian_tugas.data,
            satuan = form.satuan.data,
            volume = form.volume.data,
            waktu = form.waktu.data,
            peralatan = form.peralatan.data,
            desc = form.desc.data
        )
        db.session.add(new)
        db.session.commit()
        flash('Uraian tugas baru telah ditambahkan')
        return redirect(url_for('jabatan.view', id=item.id))
    
    return render_template('jabatan/view.html', item=item, list=list, total=total, form=form, title='View Data Jabatan')

@jabatan.route('/data-jabatan/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    item = Jabatan.query.get_or_404(id)
    form = JabatanForm(obj=item)
    if form.validate_on_submit():
        item.name = form.name.data
        item.desc = form.desc.data
        db.session.commit()
        
        flash('Data jabatan telah diubah', category='success')
        return redirect(url_for('jabatan.view', id=item.id))
    
    return render_template('jabatan/edit.html', item=item, form=form, title='Edit Data Jabatan')

@jabatan.route('/data-jabatan/<id>/hapus', methods=['GET', 'POST'])
@login_required
def delete(id):
    item = Jabatan.query.get_or_404(id)
    list = Ikhtisar_Jabatan.query.filter(Ikhtisar_Jabatan.jabatan_id==item.id).all()
    if list:
        for i in list:
            db.session.delete(i)
    db.session.delete(item)
    db.session.commit()
    flash('Data Jabatan "'+item.name+'" telah dihapus.')
    return redirect(url_for('jabatan.list'))

@jabatan.route('/data-jabatan/uraian/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit_uraian(id):
    item = Ikhtisar_Jabatan.query.get_or_404(id)
    form = IkhtisarJabatanForm(obj=item)
    if form.validate_on_submit():
        item.uraian_tugas = form.uraian_tugas.data
        item.satuan = form.satuan.data
        item.volume = form.volume.data
        item.waktu = form.waktu.data
        item.peralatan = form.peralatan.data
        item.desc = form.desc.data

        db.session.commit()
        flash('Uraian tugas telah diubah.', category='success')
        return redirect(url_for('jabatan.view', id=item.jabatan_id))
    
    return render_template('jabatan/edit-uraian.html', form=form, item=item, title='Edit Ikhtisar Jabatan')

@jabatan.route('/data-jabatan/uraian/<id>/hapus', methods=['GET', 'POST'])
@login_required
def delete_uraian(id):
    item = Ikhtisar_Jabatan.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Data Uraian Tugas telah dihapus', category='danger')
    return redirect(url_for('jabatan.view', id=item.jabatan_id))