from flask import flash, redirect, render_template, url_for, request, session, app, jsonify
from flask_login import login_required
from . import jabatan
from ...models import Jabatan, Sasaran_Kinerja, Indikator_Kinerja, Ikhtisar_Jabatan
from .forms import JabatanForm, SasaranKinerjaForm, IndikatorKinerjaForm, IkhtisarJabatanForm
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

@jabatan.route('/data-jabatan/<id>/sasaran-kinerja', methods=['GET', 'POST'])
@login_required
def view_jabatan_sasaran(id):
    item = Jabatan.query.get_or_404(id)
    list = enumerate(Sasaran_Kinerja.query.filter(Sasaran_Kinerja.jabatan_id==item.id).all(), start=1)
    form = SasaranKinerjaForm()
    if form.validate_on_submit():
        new = Sasaran_Kinerja(jabatan_id=id, name=form.name.data, desc=form.desc.data)
        db.session.add(new)
        db.session.commit()
        
        flash('Data Sasaran Kinerja berhasil ditambahkan', category='success')
        return redirect(url_for('jabatan.view', id=item.id))
    
    return render_template('jabatan/view.html', item=item, list=list, form=form, title='View Data Sasaran Jabatan')

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
            indikator = form.indikator.data,
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
    
    return render_template('jabatan/view-jabur.html', item=item, list=list, total=total, form=form, title='View Data Jabatan')

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
    
    list2 = Sasaran_Kinerja.query.filter(Sasaran_Kinerja.jabatan_id==item.id).all()
    if list2:
        for j in list2:
            db.session.delete(j)
    
    list3 = Indikator_Kinerja.query.filter(Indikator_Kinerja.jabatan_id==item.id).all()
    if list3:
        for k in list3:
            db.session.delete(k)
    
    db.session.delete(item)
    db.session.commit()
    flash('Data Jabatan "'+item.name+'" telah dihapus.')
    return redirect(url_for('jabatan.list'))

@jabatan.route('/data-jabatan/<id>/sasaran-kinerja/<sasaran_id>', methods=['GET', 'POST'])
@login_required
def view_sasaran(id, sasaran_id):
    item = Jabatan.query.get_or_404(id)
    item2 = Sasaran_Kinerja.query.get_or_404(sasaran_id)
    list = enumerate(Indikator_Kinerja.query.filter(Indikator_Kinerja.sasaran_kinerja_id==item2.id).all(), start=1)
    form = IndikatorKinerjaForm()
    if form.validate_on_submit():
        new = Indikator_Kinerja(jabatan_id=id, sasaran_kinerja_id=sasaran_id, name=form.name.data, desc=form.desc.data)
        db.session.add(new)
        db.session.commit()
        
        flash('Data Indikator Kinerja berhasil ditambahkan', category='success')
        return redirect(url_for('jabatan.view_sasaran', id=item2.jabatan_id, sasaran_id=item2.id))
    
    return render_template('jabatan/view-sasaran.html', item2=item2, list=list, form=form, title='View Sasaran Kinerja Jabatan')

@jabatan.route('/data-jabatan/<id>/sasaran-kinerja/<sasaran_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_sasaran(id, sasaran_id):
    item = Jabatan.query.get_or_404(id)
    item2 = Sasaran_Kinerja.query.get_or_404(sasaran_id)
    form = SasaranKinerjaForm(obj=item2)
    if form.validate_on_submit():
        item2.name=form.name.data
        item2.desc=form.desc.data
        
        db.session.commit()
        
        flash('Data Sasaran Kinerja berhasil diubah', category='success')
        return redirect(url_for('jabatan.view_sasaran', id=item2.jabatan_id, sasaran_id=item2.id))
    
    return render_template('jabatan/edit-sasaran.html', item2=item2, form=form, title='Edit Sasaran Kinerja Jabatan')

@jabatan.route('/data-jabatan/<id>/sasaran-kinerja/<sasaran_id>/hapus', methods=['GET', 'POST'])
@login_required
def delete_sasaran(id, sasaran_id):
    item2 = Sasaran_Kinerja.query.get_or_404(sasaran_id)
    list = Ikhtisar_Jabatan.query.filter(Ikhtisar_Jabatan.jabatan_id==item2.jabatan_id).all()
    if list:
        for i in list:
            db.session.delete(i)
    
    list3 = Indikator_Kinerja.query.filter(Indikator_Kinerja.jabatan_id==item2.jabatan_id).all()
    if list3:
        for k in list3:
            db.session.delete(k)
    db.session.delete(item2)
    db.session.commit()
    flash('Data Sasaran Kinerja berhasil dihapus', category='success')
    return redirect(url_for('jabatan.list_sasaran', id=id))

@jabatan.route('/data-jabatan/<id>/sasaran-kinerja/<sasaran_id>/indikator-kinerja', methods=['GET', 'POST'])
@login_required
def list_indikator(id, sasaran_id):
    item = Jabatan.query.get_or_404(id)
    list = enumerate(Indikator_Kinerja.query.filter_by(Indikator_Kinerja.jabatan_id==item.id).all(), start=1)
    form = IndikatorKinerjaForm()
    if form.validate_on_submit():
        new = Indikator_Kinerja(jabatan_id=id, sasaran_kinerja=sasaran_id, name=form.name.data, desc=form.desc.data)
        db.session.add(new)
        db.session.commit()
        
        flash('Data Sasaran Kinerja berhasil ditambahkan', category='success')
        return redirect(url_for('jabatan.list_sasaran', id=item.id))
    
    return render_template('jabatan/list-sasaran.html', list=list, form=form, title='Data Indikator Kinerja Jabatan'+{item.name})

@jabatan.route('/data-jabatan/<id>/sasaran-kinerja/<sasaran_id>/indikator-kinerja/<indikator_id>', methods=['GET', 'POST'])
@login_required
def view_indikator(id, sasaran_id, indikator_id):
    item = Jabatan.query.get_or_404(id)
    item2 = Sasaran_Kinerja.query.get_or_404(sasaran_id)
    item3 = Indikator_Kinerja.query.get_or_404(indikator_id)
    uraian = Ikhtisar_Jabatan.query.filter(Ikhtisar_Jabatan.indikator_kinerja_id==item3.id).all()
    total = 0
    for i in uraian:
        beban = i.volume * i.waktu
        total = total + beban
    list = enumerate(uraian, start=1)
    form = IkhtisarJabatanForm()
    if form.validate_on_submit():
        new = Ikhtisar_Jabatan(
                jabatan_id = item.id,
                indikator_kinerja_id = item3.id,
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
        return redirect(url_for('jabatan.view_indikator', id=item.id, sasaran_id=item2.id, indikator_id=item3.id))
    
    return render_template('jabatan/view-indikator.html', item3=item3, list=list, total=total, form=form, title='View Indikator Kinerja Jabatan')

@jabatan.route('/data-jabatan/<id>/sasaran-kinerja/<sasaran_id>/indikator-kinerja/<indikator_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_indikator(id, sasaran_id, indikator_id):
    item = Jabatan.query.get_or_404(id)
    item2 = Sasaran_Kinerja.query.get_or_404(sasaran_id)
    item3 = Indikator_Kinerja.query.get_or_404(indikator_id)
    form = IndikatorKinerjaForm(obj=item3)
    if form.validate_on_submit():
        item3.name=form.name.data
        item3.desc=form.desc.data
        
        db.session.commit()
        flash('Data Indikator Kinerja berhasil diubah', category='success')
        return redirect(url_for('jabatan.view_indikator', id=item3.jabatan_id, sasaran_id=item3.sasaran_kinerja_id, indikator_id=item3.id))
    
    return render_template('jabatan/edit-indikator.html', item3=item3, form=form, title='Edit Indikator Kinerja Jabatan')

@jabatan.route('/data-jabatan/<id>/sasaran-kinerja/<sasaran_id>/indikator-kinerja/<indikator_id>/hapus', methods=['GET', 'POST'])
@login_required
def delete_indikator(id, sasaran_id, indikator_id):
    item3 = Sasaran_Kinerja.query.get_or_404(indikator_id)
    
    list = Ikhtisar_Jabatan.query.filter(Ikhtisar_Jabatan.jabatan_id==item3.jabatan_id).all()
    if list:
        for i in list:
            db.session.delete(i)
            
    db.session.delete(item3)
    db.session.commit()
    flash('Data Indikator Kinerja berhasil dihapus', category='success')
    return redirect(url_for('jabatan.list_indikator', id=sasaran_id))

@jabatan.route('/data-jabatan/<id>/sasaran-kinerja/<sasaran_id>/indikator-kinerja/<indikator_id>/uraian/<uraian_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_uraian_(id, sasaran_id, indikator_id, uraian_id):
    item = Indikator_Kinerja.query.get_or_404(indikator_id)
    item2 = Ikhtisar_Jabatan.query.get_or_404(uraian_id)
    form = IkhtisarJabatanForm(obj=item2)
    if form.validate_on_submit():
        item.uraian_tugas = form.uraian_tugas.data
        item.satuan = form.satuan.data
        item.volume = form.volume.data
        item.waktu = form.waktu.data
        item.peralatan = form.peralatan.data
        item.desc = form.desc.data

        db.session.commit()
        flash('Uraian tugas telah diubah.', category='success')
        return redirect(url_for('jabatan.view_indikator', id=item2.jabatan_id, sasaran_id=item.sasaran_kinerja_id, indikator_id=item.id, uraian_id=item2.id))
    
    return render_template('jabatan/edit-uraian.html', form=form, item=item, item2=item2, title='Edit Ikhtisar Jabatan')

@jabatan.route('/data-jabatan/<id>/uraian/<uraian_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_uraian(id, uraian_id):
    item = Ikhtisar_Jabatan.query.get_or_404(id)
    item2 = Ikhtisar_Jabatan.query.get_or_404(uraian_id)
    form = IkhtisarJabatanForm(obj=item2)
    if form.validate_on_submit():
        item.indikator_kinerja =  form.indikator.data
        item.uraian_tugas = form.uraian_tugas.data
        item.satuan = form.satuan.data
        item.volume = form.volume.data
        item.waktu = form.waktu.data
        item.peralatan = form.peralatan.data
        item.desc = form.desc.data

        db.session.commit()
        flash('Uraian tugas telah diubah.', category='success')
        return redirect(url_for('jabatan.view', id=item.jabatan_id))
    
    return render_template('jabatan/edit-uraian2.html', form=form, item=item, item2=item2,title='Edit Ikhtisar Jabatan')

@jabatan.route('/data-jabatan/uraian/<id>/hapus', methods=['GET', 'POST'])
@login_required
def delete_uraian(id):
    item = Ikhtisar_Jabatan.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Data Uraian Tugas telah dihapus', category='danger')
    return redirect(url_for('jabatan.view', id=item.jabatan_id))

@jabatan.route('/get-sasaran', methods=['GET', 'POST'])
@login_required
def get_sasaran():
    jabatan_id = request.args.get('id')
    sasaran = Sasaran_Kinerja.query.filter(Sasaran_Kinerja.jabatan_id==jabatan_id).all()
    list = []
    for s in sasaran:
        data = {}
        
        #Nama Sasaran
        data['id'] = s.id
        data['name'] = s.name
        data['jabatan_id'] = s.jabatan_id
        data['desc'] = s.desc

        list.append(data)

    return jsonify(list)

@jabatan.route('/get-indikator', methods=['GET', 'POST'])
@login_required
def get_indikator():
    sasaran_id= request.args.get('id')
    indikator = Indikator_Kinerja.query.filter(Indikator_Kinerja.sasaran_kinerja_id==sasaran_id).all()
    list =[]
    for s in indikator:
        data = {}
        
        #Nama Indikator
        data['id'] = s.id
        data['name'] = s.name
        data['jabatan_id'] = s.jabatan_id
        data['sasaran_kinerja_id'] = s.sasaran_kinerja_id
        data['desc'] = s.desc

        list.append(data)

    return jsonify(list)