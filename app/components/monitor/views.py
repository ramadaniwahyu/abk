from flask import flash, redirect, render_template, url_for, request, current_app
from flask_login import login_required
from . import monitor

from ... import db
from ...models import Capaian_Bulanan, Pegawai, Perjanjian_Kinerja, Realisasi_Kinerja

import datetime

@monitor.route('/monitoring', methods=['GET', 'POST'])
@login_required
def list():
    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    query = request.args.get('query')
    if query:
        year = query
    else:
        today = datetime.date.today()
        year = today.strftime("%Y")
        
    pegawai = Pegawai.query.all()
    data = []
    
    for p in pegawai:
        peg = {}
        peg['id'] = p.id
        peg['name'] = p.name
        peg['nomor'] = p.nomor
        peg['foto'] = p.foto
        peg['jabatan'] = p.jabatan
        peg['pangkat'] = p.pangkat
        
        nilai_bulan = []
        for n in range(1, 13):
            nil = {}
            nil['predikat'] = ""
            nil['nilai'] = 0
            nil['class'] = ""
            nilai_bulan.append(nil)
            
        pk = Perjanjian_Kinerja.query.filter(Perjanjian_Kinerja.tahun==year, Perjanjian_Kinerja.pegawai_id==p.id).first()
        if pk:
            capaian = Capaian_Bulanan.query.filter(Capaian_Bulanan.perjanjian_kinerja_id==pk.id).all()
            if capaian :
                for c in capaian:
                    hasil = Realisasi_Kinerja.query.filter(Realisasi_Kinerja.capaian_bulanan_id==c.id).all()
                    ind = bulan.index(c.bulan)
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

                    if indikator:
                        total = round(total / len(indikator), 2)

                    if total < 50:
                        p = 'Buruk'
                        c = 'bg-danger'
                    elif total <= 60:
                        p = 'Sedang'
                        c = 'bg-warning'
                    elif total <=75:
                        p = 'Cukup'
                        c = 'bg-success'
                    elif total <=90:
                        p = 'Baik'
                        c = 'bg-success'
                    else:
                        p = 'Sangat Baik'
                        c = 'bg-success'
                    
                    n = {}    
                    n['nilai'] = total
                    n['predikat'] = p
                    n['class'] = c
                    nilai_bulan[ind] = n
                    peg['predikat'] = p
                                
        
        # peg['trial'] = pk
        peg['nilai'] = nilai_bulan
        
        data.append(peg)    
    
    list = enumerate(data, start=1)
    
    
    
    return render_template('monitor/list.html', list=list, title='Monitoring Penilaian Kinerja')
