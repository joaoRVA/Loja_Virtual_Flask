import os

from flask import flash, redirect, render_template, request, session, url_for

from loja import app, criptografia, db
from loja.produtos.models import AddProduto, Categoria, Marcas

from .formulario import Login, Registro
from .models import User


@app.route('/admin')
def admin():
    if 'email' not in session:
        flash("Por favor, faça o login antes de entrar no sistema.", 'danger')
        return redirect(url_for('login'))
    produtos = AddProduto.query.all()
    return render_template('admin/index.html', title="Página Administrativa", produtos=produtos)

@app.route('/marcas')
def marcas():
    if 'email' not in session:
        flash("Por favor, faça o login antes de entrar no sistema.", 'danger')
        return redirect(url_for('login'))
    marcas = Marcas.query.order_by(Marcas.id.desc()).all()
    return render_template('admin/marcas.html', title="Página de Fabricantes", marcas=marcas)

@app.route('/categoria')
def categoria():
    if 'email' not in session:
        flash("Por favor, faça o login antes de entrar no sistema.", 'danger')
        return redirect(url_for('login'))
    categorias = Categoria.query.order_by(Categoria.id.desc()).all()
    return render_template('admin/marcas.html', title="Página de Categorias", categorias=categorias)

@app.route('/logout')
def logout():
    session.pop('email', None)
    session.clear()
    flash("Você foi desconectado do login de administrador.", "info")
    return redirect(url_for('home'))

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    form = Registro(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = criptografia.generate_password_hash(form.password.data)
        user = User(name=form.name.data, username=form.username.data, email=form.email.data, password=hash_password)

        try:
            db.session.add(user)
            db.session.commit()
            flash(f"Obrigado por registrar, {form.name.data}", "success")
        except Exception as e:
            print(e)
            db.session.rollback()
            flash("Não foi possível registrar")
            return redirect(url_for('registrar'))
        return redirect(url_for('login'))
    return render_template('admin/registrar.html', form=form, title='Cadastro')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and criptografia.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f"Olá, {form.email.data}", "success")
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash("Erro ao tentar entrar no site", 'danger')
    return render_template('admin/login.html', form=form, title='Login')