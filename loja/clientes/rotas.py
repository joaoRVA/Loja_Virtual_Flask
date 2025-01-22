import os
import secrets

import pdfkit
import stripe
from flask import (current_app, flash, make_response, redirect,
                   render_template, request, session, url_for)
from flask_login import current_user, login_required, login_user, logout_user

from loja import app, criptografia, db, photos

from .form import CadastroClienteForm, LoginClienteForm
from .models import Cadastro, ClientePedido

# chaves da api do stripe para pagamento

publishable_key = "pk_test_51QjlkjLXPjM9Gplj3esS3OszI8m81T2XfFqxScMlPiGAkXug1Qwm58fuPkuWz9cqtGNpm9NZjjtg4xKNfXFnLRpc00kJ5aG2jg"
stripe.api_key = "sk_test_51QjlkjLXPjM9Gpljlghtx3F8my2GSNQqlMRwmwG4dUAzFRbZQ2yN5eLajNU9KCaLT10oluG03HYyQu1qSfCbThZL0077wqs6pw"

# /===================================/


def atualizarSession():
    for _key, produto in session['LojainCarrinho'].items():
        session.modified = True
        del produto['Imagem']
        del produto['Cor']
    return atualizarSession


@app.route("/cliente/pagamento", methods=["POST"])
@login_required
def pagamento():
    amount = request.form.get('amount')
    notafiscal = request.form.get('invoice')

    customer = stripe.Customer.create(
    email=request.form['stripeEmail'],
    source=request.form['stripeToken'],
    )

    charge = stripe.Charge.create(
    customer=customer.id,
    description='Loja_Virtual',
    amount=amount,
    currency='brl',
    )
    cliente_pedido = ClientePedido.query.filter_by(cliente_id=current_user.id, notafiscal=notafiscal).order_by(ClientePedido.id.desc()).first()
    cliente_pedido.status = 'PAGO'
    db.session.commit()
    return redirect(url_for('obrigado'))


@app.route("/cliente/obrigado")
def obrigado():
    return render_template("/cliente/obrigado.html")


@app.route("/cliente/cadastrar", methods=["GET", "POST"])
def cadastrar_cliente():
    form = CadastroClienteForm()

    if form.validate_on_submit():
        hash_password = criptografia.generate_password_hash(form.password.data)
        cadastro = Cadastro(
            name=form.name.data, username=form.username.data, email=form.email.data, 
            password=hash_password, country=form.country.data, state=form.state.data, 
            city=form.city.data, contact=form.contact.data, address=form.address.data,
            zipcode=form.zipcode.data, profile=form.profile.data)
        
        try:
            db.session.add(cadastro)
            db.session.commit()
            flash(f"Obrigado por cadastrar, {form.username.data}", "success")
            return redirect(url_for('clienteLogin'))
        except Exception as e:
            print(e)
            return redirect(url_for('cadastrar_cliente'))
        
    return render_template("cliente/clientes.html", form=form)


@app.route('/cliente/login', methods=['GET', 'POST'])
def clienteLogin():
    form = LoginClienteForm(request.form)
    if form.validate_on_submit():
        user = Cadastro.query.filter_by(email=form.email.data).first()
        if user and criptografia.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f"Olá, {form.email.data}", "success")
            return redirect(request.args.get('next') or url_for('home'))
        else:
            flash("Erro ao tentar entrar no site", 'danger')
            return redirect(url_for('clienteLogin'))
    return render_template('cliente/loginCliente.html', form=form, title='Login Cliente')

@app.route('/cliente/logout', methods=['GET', 'POST'])
def LogoutCliente():
 
    logout_user()
    flash("Você deslogou do sistema.", "warning")
    return redirect(url_for('home'))


@app.route("/pedido_order")
@login_required
def pedido_order():
    if current_user.is_authenticated:
        cliente_id = current_user.id
        notafiscal = secrets.token_hex(5)
        atualizarSession()
        try:
            p_order = ClientePedido(cliente_id=cliente_id, notafiscal=notafiscal, pedido=session['LojainCarrinho'])
            db.session.add(p_order)
            db.session.commit()
            session.pop('LojainCarrinho')
            flash("Seu pedido foi salvo com sucesso!", "success")
            return redirect(url_for('pedidos', notafiscal=notafiscal))

        except Exception as e:
            print(e)
            flash("Não foi possível processar seu pedido.", "danger")
            return redirect(url_for('getCarro'))
        

@app.route("/pedidos/<notafiscal>")
@login_required
def pedidos(notafiscal):
    if current_user.is_authenticated:
        total = 0
        subtotal = 0
        cliente_id = current_user.id 

        cliente = Cadastro.query.filter_by(id=cliente_id).first()
        pedidos = ClientePedido.query.filter_by(cliente_id=cliente_id, notafiscal=notafiscal).order_by(ClientePedido.id.desc()).first()

        for _key, pedido in pedidos.pedido.items():
            desconto = (pedido['Desconto']/100) * float(pedido['Preco'])
            subtotal += float(pedido['Preco']) * int(pedido['Quantidade'])
            subtotal -= desconto
            imposto = (f"{.06 * float(subtotal):.2f}")
            total = (f"{1.06 * float(subtotal):.2f}")
    else:
        return redirect(url_for('clienteLogin'))
    
    return render_template('cliente/pedido.html', 
                           title='Pedido', 
                           notafiscal=notafiscal, 
                           total=total, 
                           imposto=imposto,
                           subtotal=subtotal,
                           desconto=desconto,
                           cliente=cliente,
                           pedidos=pedidos,
                           )


@app.route("/get_pdf/<notafiscal>", methods=['POST'])
@login_required
def get_pdf(notafiscal):
    if current_user.is_authenticated:
        total = 0
        subtotal = 0
        cliente_id = current_user.id 
        if request.method == 'POST':
            cliente = Cadastro.query.filter_by(id=cliente_id).first()
            pedidos = ClientePedido.query.filter_by(cliente_id=cliente_id, notafiscal=notafiscal).order_by(ClientePedido.id.desc()).first()
            for _key, pedido in pedidos.pedido.items():
                desconto = (pedido['Desconto']/100) * float(pedido['Preco'])
                subtotal += float(pedido['Preco']) * int(pedido['Quantidade'])
                subtotal -= desconto
                imposto = (f"{.06 * float(subtotal):.2f}")
                total = (f"{1.06 * float(subtotal):.2f}")
    
        rendered = render_template('cliente/pdf.html', 
                           title='Pedido', 
                           notafiscal=notafiscal, 
                           total=total, 
                           imposto=imposto,
                           subtotal=subtotal,
                           desconto=desconto,
                           cliente=cliente,
                           pedidos=pedidos)
        
        # === configuração do pdfkit para localizar o arquivo wkhtmltopdf ===
        options = {'enable-local-file-access': None}
        config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
        pdf = pdfkit.from_string(rendered, False, configuration=config, options=options)
      
        response = make_response(pdf)
        response.headers['content-Type'] = 'application/pdf'
        response.headers['content-Disposition'] = 'inline:filename=' + notafiscal + '.pdf'
        return response
        # /=======================================/
    return redirect(url_for('pedidos'))