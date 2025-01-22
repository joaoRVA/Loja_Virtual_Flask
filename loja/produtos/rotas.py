import os
import secrets

from flask import (current_app, flash, redirect, render_template, request,
                   url_for)

from loja import app, db, photos
from loja.admin.rotas import session

from .formulario import AddProdutos
from .models import AddProduto, Categoria, Marcas


def marcasNav():
    marcas = Marcas.query.join(AddProduto, (Marcas.id == AddProduto.marca_id)).all() # filtra somente os produtos disponiveis
    return marcas

def categoriasNav():
    categorias = Categoria.query.join(AddProduto, (Categoria.id == AddProduto.categoria_id)).all()
    return categorias


@app.route("/")
def home():
    pagina = request.args.get('pagina', 1, type=int)
    produtos = AddProduto.query.filter(AddProduto.stock > 0).order_by(AddProduto.id.desc()).paginate(page=pagina, per_page=3)
    return render_template("produtos/index.html", title="Página Inicial", produtos=produtos, marcas=marcasNav(), categorias=categoriasNav(), pagina_atual=pagina)


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        search = "%{0}%".format(search_value)
        produtos = AddProduto.query.filter(AddProduto.name.like(search)).all()
        return render_template("/produtos/pesquisar.html", produtos=produtos, marcas=marcasNav(), categorias=categoriasNav())
    else:
        return redirect('/')



@app.route("/marca/<int:id>")
def get_marca(id):
    pagina = request.args.get('pagina', 1, type=int)
    get_id_marca = Categoria.query.filter_by(id=id).first_or_404()
    marca = AddProduto.query.filter_by(marca=get_id_marca).paginate(page=pagina, per_page=3)
    return render_template("produtos/index.html", title="Página Inicial", marca=marca, marcas=marcasNav(), categorias=categoriasNav(), pagina_atual=pagina, get_id_marca=get_id_marca)

@app.route("/categoria/<int:id>")
def get_categoria(id):
    pagina = request.args.get('pagina', 1, type=int)
    get_cat = Categoria.query.filter_by(id=id).first_or_404()
    categoria = AddProduto.query.filter_by(categoria=get_cat).paginate(page=pagina, per_page=3)
    return render_template("produtos/index.html", title="Página Inicial", categoria=categoria, categorias=categoriasNav(), marcas=marcasNav(), pagina_atual=pagina, get_cat=get_cat)

@app.route("/produto/<int:id>")
def pagina_unica(id):
    produto = AddProduto.query.get_or_404(id)

    return render_template("produtos/pagina_unica.html", title='Página Única', produto=produto, marcas=marcasNav(), categorias=categoriasNav())

@app.route("/addmarca", methods=['GET', 'POST'])
def addmarca():
    if 'email' not in session:
        flash("Por favor, faça o login antes de entrar no sistema.", 'danger')
        return redirect(url_for('login'))
    if request.method == 'POST':
        getmarca = request.form.get('marca')

        if not getmarca:
            flash("O campo marca não pode estar vazio.", 'warning')
            return redirect(url_for('addmarca'))
        
        marca = Marcas(name=getmarca)

        try:
            db.session.add(marca)
            db.session.commit()
            flash(f"O fabricante {getmarca} foi cadastrado com sucesso!", 'success')
        except Exception as e:
            db.session.rollback()  # Evita corromper a sessão
            flash("Erro ao cadastrar fabricante. Tente novamente.", 'danger')

        return redirect(url_for('addmarca'))
    return render_template('/produtos/addmarca.html', marcas='marcas', title="Cadastrar Marca")


@app.route("/addcat", methods=['GET', 'POST'])
def addcat():
    if 'email' not in session:
        flash("Por favor, faça o login antes de entrar no sistema.", 'danger')
        return redirect(url_for('login'))
    if request.method == 'POST':
        getcat = request.form.get('Categorias')

        if not getcat:
            flash("O campo não pode estar vazio.", 'warning')
            return redirect(url_for('addcat'))
        
        categoria = Categoria(name=getcat)

        try:
            db.session.add(categoria)
            db.session.commit()
            flash(f"A categoria {getcat} foi cadastrada com sucesso!", 'success')
        except Exception as e:
            db.session.rollback()  # Evita corromper a sessão
            flash("Erro ao cadastrar categoria. Tente novamente.", 'danger')

        return redirect(url_for('addcat'))
    return render_template('/produtos/addmarca.html', title="Cadastrar Categoria")


@app.route("/addproduto", methods=['GET', 'POST'])
def addproduto():
    if 'email' not in session:
        flash("Por favor, faça o login antes de entrar no sistema.", 'danger')
        return redirect(url_for('login'))
    marcas = Marcas.query.all()
    categorias = Categoria.query.all()
    form = AddProdutos(request.form)

    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        description = form.description.data
        colors = form.colors.data
        marca = request.form.get('marca')
        categoria = request.form.get('categoria')

        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10)+".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10)+".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10)+".")

        addprod = AddProduto(name=name,price=price,discount=discount,stock=stock,description=description,colors=colors,
                              marca_id=marca, categoria_id=categoria, image_1=image_1, image_2=image_2, image_3=image_3)

        try:
            db.session.add(addprod)
            db.session.commit()
            flash(f"{name} foi cadastrado com sucesso!", 'success')
        except Exception as e:
            db.session.rollback()  # Evita corromper a sessão
            flash("Erro ao cadastrar. Tente novamente.", 'danger')

        return redirect(url_for('admin'))
    return render_template("/produtos/addprodutos.html", title="Adicionar Produtos", form=form, marcas=marcas, categorias=categorias)


@app.route("/updatemarca/<int:id>", methods=["GET", "POST"])
def updatemarca(id):
    if 'email' not in session:
        flash("Por favor, faça o login antes de entrar no sistema.", 'danger')
        return redirect(url_for('login'))
    updatemarca = Marcas.query.get_or_404(id)
    marca = request.form.get('marca')

    if request.method == "POST":
        updatemarca.name = marca
        try:
            db.session.commit()
            flash(f" {marca} foi atualizado com sucesso!", 'success')
            return redirect(url_for('marcas'))
        except Exception as e:
            db.session.rollback()
            flash("Erro ao cadastrar. Tente novamente.", 'danger')
            return redirect(url_for('marcas'))

    return render_template("produtos/updatemarca.html", title="Atualizar Fabricantes", updatemarca=updatemarca)

@app.route("/updatecategoria/<int:id>", methods=["GET", "POST"])
def updatecategoria(id):
    if 'email' not in session:
        flash("Por favor, faça o login antes de entrar no sistema.", 'danger')
        return redirect(url_for('login'))
    updatecategoria = Categoria.query.get_or_404(id)
    categoria = request.form.get('categoria')

    if request.method == "POST":
        updatecategoria.name = categoria
        try:
            db.session.commit()
            flash(f" {categoria} foi atualizado com sucesso!", 'success')
            return redirect(url_for('categoria'))
        except Exception as e:
            db.session.rollback()
            flash("Erro ao cadastrar. Tente novamente.", 'danger')
            return redirect(url_for('categoria'))

    return render_template("produtos/updatemarca.html", title="Atualizar Categorias", updatecategoria=updatecategoria)


@app.route("/updateproduto/<int:id>", methods=["GET", "POST"])
def updateproduto(id):
    marcas = Marcas.query.all()
    categorias = Categoria.query.all()
    produtos = AddProduto.query.get_or_404(id)
    marca = request.form.get('marca')
    categoria = request.form.get('categoria')
    form = AddProdutos(request.form)


    if request.method == "POST":
        produtos.name = form.name.data
        produtos.price = form.price.data
        produtos.discount = form.discount.data

        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + produtos.image_1))
                produtos.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10)+".")
            except Exception as e:
                print(f"Erro ao excluir arquivo: {e}")
                produtos.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10)+".")

        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + produtos.image_2))
                produtos.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10)+".")
            except Exception as e:
                print(f"Erro ao excluir arquivo: {e}")
                produtos.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10)+".")

        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + produtos.image_3))
                produtos.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10)+".")
            except Exception as e:
                print(f"Erro ao excluir arquivo: {e}")
                produtos.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10)+".")


        produtos.marca_id = marca
        produtos.categoria_id = categoria
        produtos.stock = form.stock.data
        produtos.description = form.description.data
        produtos.colors = form.colors.data

        try:
            db.session.commit()
            flash(f"Produto atualizado com sucesso!", 'success')
            return redirect(url_for('admin'))
        except Exception as e:
            db.session.rollback()
            flash("Erro ao atualizar. Tente novamente.", 'danger')
            return redirect(url_for('admin'))

    form.name.data = produtos.name
    form.price.data = produtos.price
    form.discount.data = produtos.discount
    form.stock.data = produtos.stock
    form.description.data = produtos.description
    form.colors.data = produtos.colors


    return render_template("produtos/updateproduto.html", title="Atualizar Produto", form=form, marcas=marcas, 
                           categorias=categorias, produto=produtos)


@app.route("/deletarmarca/<int:id>", methods=['POST', 'GET'])
def deletarmarca(id):

    marca = Marcas.query.get_or_404(id)

    if request.method == "POST":
        try:
            db.session.delete(marca)
            db.session.commit()
            flash(f"O fabricante {marca.name} foi deletado com sucesso.", 'success')
            return redirect(url_for('marcas'))
        except Exception as e:
            print(e)
            db.session.rollback()
            flash(f"Não foi possível deletar {marca.name}.", 'warning')
            return redirect(url_for('marcas'))
        
    flash(f"Não foi possível deletar {marca.name}.", 'warning')
    return redirect(url_for('marcas'))

@app.route("/deletarcat/<int:id>", methods=['POST', 'GET'])
def deletarcat(id):

    categoria = Categoria.query.get_or_404(id)

    if request.method == "POST":
        try:
            db.session.delete(categoria)
            db.session.commit()
            flash(f"A categoria {categoria.name} foi deletada com sucesso.", 'success')
            return redirect(url_for('categoria'))
        except Exception as e:
            print(e)
            db.session.rollback()
            flash(f"Não foi possível deletar {categoria.name}.", 'warning')
            return redirect(url_for('categoria'))

    flash(f"Não foi possível deletar {categoria.name}.", 'warning')
    return redirect(url_for('categoria'))


@app.route("/deletarproduto/<int:id>", methods=['POST', 'GET'])
def deletarproduto(id):

    produtos = AddProduto.query.get_or_404(id)

    if request.method == "POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + produtos.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + produtos.image_2))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + produtos.image_3))
        except Exception as e:
            print(e)
                
        db.session.delete(produtos)
        db.session.commit()
        flash(f"O produto {produtos.name} foi deletada com sucesso.", 'success')
        return redirect(url_for('admin'))
    flash(f"Não foi possível deletar {produtos.name}.", 'warning')
    return redirect(url_for('admin'))