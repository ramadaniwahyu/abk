from flask import flash, redirect, render_template, url_for, request, session, app, abort
from flask_login import login_required, current_user
from . import kinerja
from ...models import Perjanjian_Kinerja, Capaian_Bulanan, Realisasi_Kinerja
from ... import db

from .forms import PerjanjianKinerjaForm, CapaianBulananForm, RealisasiKinerjaForm

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