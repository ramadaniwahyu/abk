from flask import flash, redirect, render_template, url_for, request, abort
from flask_login import login_required, login_user, logout_user, current_user
from . import auth
from ...models import User
from .forms import LoginForm, UserAdminForm, UserForm, PasswordForm
from ... import db

def check_admin():
    
    if not(current_user.is_admin):
        abort(403)
    

@auth.route('/masuk', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    next= request.args.get('next')
    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(name=form.name.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            # session.permanent = True

            if next :
                return redirect(next)
            else:
                return redirect(url_for('index'))

        else:
            flash('Nama Pengguna dan/atau password salah.', 'danger')

    return render_template('auth/login.html', form=form, title='Halaman Login')

@auth.route('/keluar')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('Anda telah berhasil keluar dari sistem.', 'success')

    # redirect to the login page
    return redirect(url_for('auth.login'))

@auth.route('/profil', methods=['GET', 'POST'])
@login_required
def profile():
    # pass
    pengguna = User.query.get_or_404(current_user.id)
    form = UserForm(obj=pengguna)
    if form.validate_on_submit():
        pengguna.name = form.name.data
        pengguna.email = form.email.data

        db.session.commit()
        
        flash('Pengguna telah diupdated.', 'info')
        return redirect(url_for('index'))
    
    return render_template('auth/profil.html', pengguna=pengguna, form=form, title='Profil Pengguna')

@auth.route('/profil/ganti-password', methods=['GET', 'POST'])
@login_required
def profile_password():
    # pass
    id = current_user.id
    pengguna = User.query.get_or_404(id)
    form = PasswordForm(obj=pengguna)
    if form.validate_on_submit():
        if pengguna.verify_password(form.old_password.data):
            pengguna.password = form.password.data
            db.session.commit()
            flash('Password telah diganti')
            return redirect(url_for('auth.profile'))
        else:
            flash('Password lama salah.')
    
    return render_template('auth/password.html', form=form, pengguna=pengguna, title='Ganti Password')
    
@auth.route('/pengguna', methods=['GET', 'POST'])
@login_required
def user_list():
    check_admin()
    
    list = enumerate(User.query.all(), start=1)
    form = UserAdminForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data, 
            email=form.email.data, 
            password=form.password.data,
            is_admin = form.is_admin.data,
            pegawai = form.pegawai.data
            )
        user_exist = User.query.filter_by(name=form.name.data).first()
        if user_exist is None:
            db.session.add(user)
            db.session.commit()
            # db.session.refresh(user)
            flash('Pengguna telah ditambahkan.', 'info')
            return redirect(url_for('auth.user_list'))
        else:
            flash('Nama Pengguna sudah ada.', 'danger')
    
    return render_template('auth/user-list.html', list=list, form=form, title='Daftar Pengguna')

@auth.route('/pengguna/<id>', methods=['GET', 'POST'])
@login_required
def user_edit(id):
    check_admin()
    
    item = User.query.get_or_404(id)
    form = UserAdminForm(obj=item)
    if form.validate_on_submit():
        item.email = form.email.data
        item.is_admin = form.is_admin.data
        item.password = form.password.data
        item.pegawai = form.pegawai.data
        
        db.session.commit()
        flash('Nama telah diubah.', 'info')
        return redirect(url_for('auth.user_list'))
    
    return render_template('auth/user-edit.html', list=list, form=form, title='Edit Pengguna')
    
    
@auth.route('/pengguna/<id>/hapus', methods=['GET', 'POST'])
@login_required
def user_delete(id):
    check_admin()
    
    item = User.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Data Pengguna telah dihapus.', 'success')
    return redirect(url_for('auth.user_list'))