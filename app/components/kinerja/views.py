from flask import flash, redirect, render_template, url_for, request, session, app, abort
from flask_login import login_required, current_user
from . import kinerja
from ...models import Perjanjian_Kinerja, Capaian_Bulanan, Realisasi_Kinerja, Sasaran_Kinerja, Indikator_Kinerja, Ikhtisar_Jabatan
from ... import db

from .forms import PerjanjianKinerjaForm, CapaianBulananForm, RealisasiKinerjaForm, SasaranKinerjaForm, IndikatorKinerjaForm, IkhtisarJabatanForm

def check_admin():
    
    if not(current_user.is_admin):
        abort(403)


@kinerja.route('/penilaian-kinerja', methods=['GET', 'POST'])
@login_required
def tahunan():

    list = enumerate(Perjanjian_Kinerja.query.filter(Perjanjian_Kinerja.pegawai_id==current_user.pegawai_id).all(), start=1)
    form = PerjanjianKinerjaForm()
    if form.validate_on_submit():
        new = Perjanjian_Kinerja(tgl=form.tgl.data, tahun=form.tahun.data,
                                 pegawai_id=current_user.pegawai_id, penilai=form.penilai.data,
                                 atasan_penilai=form.atasan_penilai.data)
        
        db.session.add(new)
        db.session.commit()
        db.session.refresh(new)
        flash('Perjanjian Kinerja baru berhasil ditambahkan', category='success')
        return redirect(url_for('kinerja.capaian', id=new.id))

    return render_template('kinerja/list.html', list=list, form=form, title='Perjanjian Kinerja')

@kinerja.route('/penilaian-kinerja/<id>', methods=['GET', 'POST'])
@login_required
def capaian(id):
    item = Perjanjian_Kinerja.query.get_or_404(id)
    list = enumerate(Capaian_Bulanan.query.filter(Capaian_Bulanan.perjanjian_kinerja_id == item.id).order_by(Capaian_Bulanan.tgl.asc()).all(), start=1)
    form = CapaianBulananForm()
    if form.validate_on_submit():
        new = Capaian_Bulanan(tgl=form.tgl.data, bulan=form.bulan.data, perjanjian_kinerja_id=item.id,
                                 pegawai_id=item.pegawai_id, penilai_id=item.penilai_id)
        db.session.add(new)
        db.session.commit()
        flash('Capaian Kinerja baru berhasil ditambahkan', category='success')
        return redirect(url_for('kinerja.capaian', id=item.id))
    
    return render_template('kinerja/view.html', list=list, item=item, form=form, title='Penilaian Capaian Kinerja')

@kinerja.route('/penilaian-kinerja/<id>/hapus', methods=['GET', 'POST'])
@login_required
def delete(id):
    pass

@kinerja.route('/penilaian-kinerja/<tahun_id>/capaian/<id>', methods=['GET', 'POST'])
@login_required
def view_capaian(id, tahun_id):
    item = Perjanjian_Kinerja.query.get_or_404(tahun_id)
    item2 = Capaian_Bulanan.query.get_or_404(id)
    hasil = Realisasi_Kinerja.query.filter(Realisasi_Kinerja.capaian_bulanan_id==item2.id).all()
    sasaran = []
    indikator = []
    total = 0
    for a in hasil:
        if a.ikhtisar_jabatan.indikator_kinerja not in indikator:
            indikator.append(a.ikhtisar_jabatan.indikator_kinerja)
        if a.ikhtisar_jabatan.indikator_kinerja.sasaran_kinerja not in sasaran:
            sasaran.append(a.ikhtisar_jabatan.indikator_kinerja.sasaran_kinerja)

    for i in indikator:
        nilai_indikator = 0
        qty = 0
        for a in hasil:
            if a.ikhtisar_jabatan.indikator_kinerja==i:
                nilai = round(a.realisasi/a.target*100, 2)
                nilai_indikator += (a.realisasi/a.target)*100
                qty +=1
        
        if qty==0:
            nilai_indikator+=0
        else:
            nilai_indikator = round(nilai_indikator/qty, 2)
        setattr(i, 'nilai', nilai_indikator)
        total += nilai_indikator

    total = round(total / len(indikator), 2)
    if total < 50:
        p = 'Buruk'
    elif total <= 60:
        p = 'Sedang'
    elif total <=75:
        p = 'Cukup'
    elif total <=90:
        p = 'Baik'
    else:
        p = 'Sangat Baik'
    form = RealisasiKinerjaForm()
    if form.validate_on_submit():
        new = Realisasi_Kinerja(capaian_bulanan_id=item2.id, ikhtisar_jabatan=form.uraian.data,
                                target=form.target.data, realisasi=form.realisasi.data)
        print(new)
        db.session.add(new)
        db.session.commit()
        flash('Uraian Tugas baru berhasil ditambahkan', category='success')
        return redirect(url_for('kinerja.view_capaian', id=item2.id, tahun_id=item.id))
    
    return render_template('kinerja/view_capaian.html', item=item, item2=item2, hasil=hasil, indikator=indikator, sasaran=sasaran, total=total, p=p, form=form, title='Penilaian Capaian Kinerja Bulanan')

@kinerja.route('/penilaian-kinerja/<tahun_id>/capaian/<id>/hapus', methods=['GET', 'POST'])
@login_required
def del_capaian(id, tahun_id):
    item = Perjanjian_Kinerja.query.get_or_404(tahun_id)
    item2 = Realisasi_Kinerja.query.get_or_404(id)
    db.session.delete(item2)
    db.session.commit()
    flash(flash('Realisasi berhasil dihapus', category='danger'))
    return redirect(url_for('kinerja.view_capaian', id=item2.id, tahun_id=item.id))

@kinerja.route('/sasaran-kinerja', methods=['GET', 'POST'])
@login_required
def sasaran():
    list = Sasaran_Kinerja.query.filter(Sasaran_Kinerja.jabatan_id==current_user.pegawai.jabatan_id).all()
    list = enumerate(list, start=1)
    uraian = Ikhtisar_Jabatan.query.filter(Ikhtisar_Jabatan.jabatan_id==current_user.pegawai.jabatan_id).all()
    total = 0
    # for i in uraian:
    #     beban = i.volume * i.waktu
    #     total = total + beban
    form = IkhtisarJabatanForm()
    list_uraian = enumerate(uraian, start=1)

    form = SasaranKinerjaForm()
    if form.validate_on_submit():
        new = Sasaran_Kinerja(jabatan_id=current_user.pegawai.jabatan_id, name=form.name.data, desc=form.desc.data)
        db.session.add(new)
        db.session.commit()
        
        flash('Data Sasaran Kinerja berhasil ditambahkan', category='success')
        return redirect(url_for('kinerja.sasaran'))

    return render_template('kinerja/sasaran.html', list=list, list_uraian=list_uraian, total=total, form=form, title='Daftar Sasaran Kinerja')

@kinerja.route('/sasaran-kinerja/<id>', methods=['GET', 'POST'])
@login_required
def sasaran_view(id):
    item = Sasaran_Kinerja.query.get_or_404(id)
    list = enumerate(Indikator_Kinerja.query.filter(Indikator_Kinerja.sasaran_kinerja_id==item.id).all(), start=1)
    form = IndikatorKinerjaForm()
    if form.validate_on_submit():
        new = Indikator_Kinerja(jabatan_id=item.jabatan_id, sasaran_kinerja_id=item.id, name=form.name.data, desc=form.desc.data)
        db.session.add(new)
        db.session.commit()
        
        flash('Indikator Kinerja baru berhasil ditambahkan', category='success')
        return redirect(url_for('kinerja.sasaran_view', id=item.id))
    
    return render_template('kinerja/sasaran-view.html', item=item, list=list, form=form, title='View Sasaran Kinerja Jabatan')

@kinerja.route('/sasaran-kinerja/<id>/edit', methods=['GET', 'POST'])
@login_required
def sasaran_edit(id):
    item = Sasaran_Kinerja.query.get_or_404(id)
    form = SasaranKinerjaForm(obj=item)
    if form.validate_on_submit():
        item.name=form.name.data
        item.desc=form.desc.data
        
        db.session.commit()
        
        flash('Data Sasaran Kinerja berhasil diubah', category='success')
        return redirect(url_for('kinerja.sasaran'))
    
    return render_template('kinerja/sasaran-edit.html', item=item, form=form, title='Edit Sasaran Kinerja Jabatan')

@kinerja.route('/sasaran-kinerja/<id>/hapus', methods=['GET', 'POST'])
@login_required
def sasaran_del(id):
    item = Sasaran_Kinerja.query.get_or_404(id)
    list_i = Indikator_Kinerja.query.filter(Indikator_Kinerja.sasaran_kinerja_id==item.id).all()
    if list_i:
        for i in list_i:
            list = Ikhtisar_Jabatan.query.filter(Ikhtisar_Jabatan.indikator_kinerja_id==i.id).all()
            if list:
                for a in list:
                    db.session.delete(a)

            db.session.delete(i)

    db.session.delete(item)
    db.session.commit()
    flash('Data Sasaran Kinerja serta Indikator Kinerja dan Uraian Tugasnya berhasil dihapus', category='success')
    return redirect(url_for('kinerja.sasaran', id=id))

@kinerja.route('/sasaran-kinerja/<id>/indikator-kinerja/<indikator_id>', methods=['GET', 'POST'])
@login_required
def indikator_view(id, indikator_id):
    item = Sasaran_Kinerja.query.get_or_404(id)
    item2 = Indikator_Kinerja.query.get_or_404(indikator_id)
    uraian = Ikhtisar_Jabatan.query.filter(Ikhtisar_Jabatan.indikator_kinerja_id==item2.id).all()
    total = 0
    # for i in uraian:
    #     beban = i.volume * i.waktu
    #     total = total + beban
    list = enumerate(uraian, start=1)
    form = IkhtisarJabatanForm()
    if form.validate_on_submit():
        new = Ikhtisar_Jabatan(
                jabatan_id = item.jabatan_id,
                indikator_kinerja_id = item2.id,
                uraian_tugas = form.uraian_tugas.data,
                volume = 0,
                waktu = 0,
                satuan = form.satuan.data,
                peralatan = form.peralatan.data,
                desc = form.desc.data
            )
        db.session.add(new)
        db.session.commit()
        
        flash('Uraian Tugas baru berhasil ditambahkan', category='success')
        return redirect(url_for('kinerja.indikator_view', id=item.id, indikator_id=item2.id))
    
    return render_template('kinerja/indikator-view.html', item=item, item2=item2, total=total, list=list, form=form, title='View Indikator Kinerja')

@kinerja.route('/sasaran-kinerja/<id>/indikator-kinerja/<indikator_id>/edit', methods=['GET', 'POST'])
@login_required
def indikator_edit(id, indikator_id):
    item = Sasaran_Kinerja.query.get_or_404(id)
    item2 = Indikator_Kinerja.query.get_or_404(indikator_id)
    form = IndikatorKinerjaForm(obj=item2)
    if form.validate_on_submit():
        item2.name=form.name.data
        item2.desc=form.desc.data
        
        db.session.commit()
        
        flash('Data Indikator Kinerja berhasil diubah', category='success')
        return redirect(url_for('kinerja.sasaran_view', id=item.id))
    
    return render_template('kinerja/indikator-edit.html', item=item, item2=item2, form=form, title='Edit Sasaran Kinerja Jabatan')

@kinerja.route('/sasaran-kinerja/<id>/indikator-kinerja/<indikator_id>/hapus', methods=['GET', 'POST'])
@login_required
def indikator_del(id, indikator_id):
    item = Sasaran_Kinerja.query.get_or_404(id)
    item2 = Indikator_Kinerja.query.get_or_404(indikator_id)
    list = Ikhtisar_Jabatan.query.filter(Ikhtisar_Jabatan.indikator_kinerja_id==item2.id).all()
    if list:
        for i in list:
            db.session.delete(i)

    db.session.delete(item2)
    db.session.commit()
    flash('Data indikator Kinerja dan  berhasil dihapus', category='success')
    return redirect(url_for('kinerja.sasaran_view', id=item.id))

@kinerja.route('/sasaran-kinerja/<id>/indikator-kinerja/<indikator_id>/uraian/<uraian_id>/edit', methods=['GET', 'POST'])
@login_required
def uraian_edit(id, indikator_id, uraian_id):
    item = Sasaran_Kinerja.query.get_or_404(id)
    item2 = Indikator_Kinerja.query.get_or_404(indikator_id)
    item3 = Ikhtisar_Jabatan.query.get_or_404(uraian_id)
    form = IkhtisarJabatanForm(obj=item3)
    if form.validate_on_submit():
        item3.uraian_tugas = form.uraian_tugas.data
        item3.satuan = form.satuan.data
        item3.peralatan = form.peralatan.data
        item3.desc = form.desc.data

        db.session.commit()
        
        flash('Data Uraian Tugas berhasil diubah', category='success')
        return redirect(url_for('kinerja.indikator_view', id=item.id, indikator_id=item2.id))
    
    return render_template('kinerja/uraian-edit.html', item=item, item2=item2, item3=item3, form=form, title='Edit Uraian Tugas Jabatan')

@kinerja.route('/sasaran-kinerja/<id>/indikator-kinerja/<indikator_id>/uraian/<uraian_id>/hapus', methods=['GET', 'POST'])
@login_required
def uraian_del(id, indikator_id, uraian_id):
    item = Sasaran_Kinerja.query.get_or_404(id)
    item2 = Indikator_Kinerja.query.get_or_404(indikator_id)
    item3 = Ikhtisar_Jabatan.query.get_or_404(uraian_id)
    db.session.delete(item3)
    db.session.commit()
    flash('Data Uraian Tugas berhasil dihapus', category='danger')
    return redirect(url_for('kinerja.indikator_view', id=item.id, indikator_id=item2.id))