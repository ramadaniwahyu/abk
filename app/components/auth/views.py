from flask import flash, redirect, render_template, url_for, request, session, app
from flask_login import login_required, login_user, logout_user, current_user
from . import auth
from ...models import User
from .forms import LoginForm, PenggunaForm, PasswordForm
from ... import db


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
    pass
    # return render_template('auth/profil.html', pengguna=pengguna, form=form, title='Profil Pengguna')

@auth.route('/profil/ganti-password', methods=['GET', 'POST'])
@login_required
def profil_password():
    pass
    # id = current_user.id
    # pengguna = Pengguna.query.get_or_404(id)
    # form = PasswordForm(obj=pengguna)
    # if form.validate_on_submit():
    #     if pengguna.verify_password(form.old_password.data):
    #         pengguna.password = form.password.data
    #         db.session.commit()
    #         flash('Password telah diganti')
    #         return redirect(url_for('auth.profile'))
    #     else:
    #         flash('Password lama salah.')
    
    # return render_template('auth/password.html', form=form, pengguna=pengguna, title='Ganti Password')