from flask import flash, redirect, render_template, url_for, request, session, app
from flask_login import login_required
from . import abk
from ...models import Jabatan, Pegawai
from ... import db


@abk.route('/form-b', methods=['GET', 'POST'])
@login_required
def form_b():
    # list = enumerate(Jabatan.query.all(), start=1)
    jabatan = Jabatan.query.all()
    list = []
    for j in jabatan:
        i = {}
        i['name'] = j.name
        size = len(j.pegawai)
        i['count'] = size
        list.append(i)
        
    list = enumerate(list, start=1)
    
    return render_template('abk/form-b.html', list=list, title='Form B -  Inventarisir Jumlah Pemangku Jabatan')