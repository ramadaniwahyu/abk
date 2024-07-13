from flask import flash, redirect, render_template, url_for, request, session, app
from flask_login import login_required
from . import abk
from ...models import Jabatan, Pegawai, Ikhtisar_Jabatan
from ... import db


@abk.route('/analisis-beban-kerja', methods=['GET', 'POST'])
@login_required
def form_b():
    # list = enumerate(Jabatan.query.all(), start=1)
    jabatan = Jabatan.query.all()
    list = []
    for j in jabatan:
        i = {}
        
        #Nama Jabatan
        i['name'] = j.name
        
        # Jumlah beban kerja jabatan
        total = 0
        uraian = Ikhtisar_Jabatan.query.filter(Ikhtisar_Jabatan.jabatan_id == j.id).all()
        if uraian:
            for u in uraian:
                if u.volume and u.waktu:
                    beban = u.volume * u.waktu
                else:
                    beban = 0
                total = total + beban
                
        hitung = total/60
        i['beban'] = round(hitung, 2)
        
        # Kebutuhan Pegawai
        kebutuhan = round(hitung/1200)
        i['kebutuhan'] = kebutuhan
        
        # Jumlah Pegawai yang ada
        size = len(j.pegawai)
        i['count'] = size
        
        # +/-
        qty = kebutuhan - size
        i['plusminus'] = qty
        
        # Efisiensi
        if hitung and size :
            ef = hitung / (size*1200)
            ef = round(ef, 2)
        else:
            ef = 0
        i['efisiensi'] = ef
        
        # Prestasi dan Keterangan
        if ef < 0.5 :
            i['prestasi'] = 'E'
            i['ket'] = 'Kurang'
        elif ef <= 0.69:
            i['prestasi'] = 'D'
            i['ket'] = 'Sedang'
        elif ef <= 0.89:
            i['prestasi'] = 'C'
            i['ket'] = 'Cukup'
        elif ef <= 1:
            i['prestasi'] = 'B'
            i['ket'] = 'Baik'
        elif ef > 1:
            i['prestasi'] = 'A'
            i['ket'] = 'Sangat Baik'
            
        # Masukkan list baru
        list.append(i)
        
    list = enumerate(list, start=1)
    
    return render_template('abk/form-b.html', list=list, title='Form ABK')