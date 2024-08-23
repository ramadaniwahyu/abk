from flask import flash, redirect, render_template, url_for, request, session, app, abort
from flask_login import login_required, current_user
from . import kinerja
from ...models import Perjanjian_Kinerja, Capaian_Bulanan
from ... import db

from .forms import PerjanjianKinerjaForm, CapaianBulananForm

def check_admin():
    
    if not(current_user.is_admin):
        abort(403)


@kinerja.route('/penilaian-kinerja', methods=['GET', 'POST'])
@login_required
def kinerja_tahunan():

    list = Perjanjian_Kinerja.query.filter(Perjanjian_Kinerja.pegawai_id==current_user.pegawai_id).all()
    form = PerjanjianKinerjaForm()
    if form.validate_on_submit():
        new = Perjanjian_Kinerja(tgl=form.tgl.data, tahun=form.tahun.data,
                                 pegawai_id=current_user.pegawai_id, penilai=form.penilai.data,
                                 atasan_penilai=form.atasan_penilai.data)
        
        db.session.add(new)
        db.session.refresh(new)
        db.session.commit()
        flash('Perjanjian Kinerja baru berhasil ditambahkan', category='success')
        return redirect(url_for('kinerja.kinerja_capaian', id=new.id))

    return render_template('kinerja/list.html', list=list, form=form, title='Perjanjian Kinerja')

@kinerja.route('/penilaian-kinerja/<id>', methods=['GET', 'POST'])
@login_required
def kinerja_capaian(id):
    item = Perjanjian_Kinerja.query.get_or_404(id)
    list = Capaian_Bulanan.query.filter(Capaian_Bulanan.perjanjian_kinerja_id == item.id).all()
    form = CapaianBulananForm()
    if form.validate_on_submit():
        new = Capaian_Bulanan(tgl=form.tgl.data, bulan=form.bulan.data,
                                 pegawai_id=current_user.pegawai_id, penilai=form.penilai.data)
        db.session.add(new)
        db.session.commit()
        flash('Perjanjian Kinerja baru berhasil ditambahkan', category='success')
        return redirect(url_for('kinerja.kinerja_capaian', id=item.id))
    
    return render_template('kinerja/view.html', list=list, form=form, title='Penilaian Capaian Kinerja')