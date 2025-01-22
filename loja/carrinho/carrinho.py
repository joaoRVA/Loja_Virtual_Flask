from flask import (current_app, flash, redirect, render_template, request,
                   session, url_for)

from loja import app, db, photos
from loja.produtos.models import AddProduto
from loja.produtos.rotas import categoriasNav, marcasNav


def M_Dicionario(dict1, dict2):
    """Mescla duas listas ou dicionários."""
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        dict1.update(dict2)
        return dict1
    return False


@app.route('/addCarrinho', methods=['POST'])
def addCarrinho():
    """Adiciona um produto ao carrinho."""
    try:
        # Captura dados do formulário
        produto_id = request.form.get('produto_id')
        quantity = int(request.form.get('quantity', 1))  # Garante que a quantidade seja pelo menos 1
        colors = request.form.get('colors')

        # Busca o produto no banco de dados
        produto = AddProduto.query.filter_by(id=produto_id).first()

        # Valida os dados do formulário e método
        if not (produto_id and colors and request.method == "POST"):
            flash("Dados inválidos. Tente novamente.", "danger")
            return redirect(request.referrer)

        # Cria o dicionário do produto
        dictProd = {
            produto_id: {
                'Nome': produto.name,
                'Preco': produto.price,
                'Desconto': produto.discount,
                'Cor': colors,
                'Quantidade': quantity,
                'Imagem': produto.image_1,
                'Descricao': produto.description,
                'colors': produto.colors
            }
        }

        # Lógica de sessão para o carrinho
        if 'LojainCarrinho' in session:
            carrinho = session['LojainCarrinho']
            if produto_id in carrinho:
                # Incrementa a quantidade do produto existente
                session.modified = True
                carrinho[produto_id]['Quantidade'] = int(carrinho[produto_id]['Quantidade']) + quantity
                flash("Produto adicionado novamente!", "info")
            else:
                # Adiciona um novo produto ao carrinho
                carrinho.update(dictProd)
                session['LojainCarrinho'] = carrinho
                flash("Produto adicionado ao carrinho!", "success")
        else:
            # Cria o carrinho e adiciona o primeiro produto
            session['LojainCarrinho'] = dictProd
            flash("Produto adicionado ao carrinho!", "success")

    except Exception as e:
        current_app.logger.error(f"Erro ao adicionar ao carrinho: {e}")
        flash("Ocorreu um erro ao adicionar o produto ao carrinho.", "danger")
    finally:
        # Sempre retorna o usuário para a página anterior
        return redirect(request.referrer)


@app.route("/carros")
def getCarro():
    if 'LojainCarrinho' not in session or len(session['LojainCarrinho'])<=0:
        return redirect(url_for('home'))
    subtotal = 0
    valor_pagar = 0

    for key, produto in session['LojainCarrinho'].items():
        discount = (produto['Desconto']/100) * float(produto['Preco'])
        subtotal += float(produto['Preco']) * int(produto['Quantidade'])
        subtotal -= discount
        imposto = (f"{.06 * float(subtotal):.2f}")
        valor_pagar = (f"{1.06 * float(subtotal):.2f}")
    return render_template('produtos/carros.html', title='Carrinho', subtotal=subtotal, imposto=imposto, valor_pagar=valor_pagar, marcas=marcasNav(), categorias=categoriasNav())


@app.route('/updateCarro/<int:code>', methods=['POST'])
def updateCarro(code):
    if 'LojainCarrinho' not in session or len(session['LojainCarrinho'])<=0:
        return redirect(url_for('home'))

    if request.method == 'POST':
        quantity = request.form.get('quantity')
        colors = request.form.get('colors')

        try:
            session.modified = True

            for key, item in session['LojainCarrinho'].items():
                if int(key) == code:
                    item['Quantidade'] = quantity
                    item['Cor'] = colors
                    flash("ITEM ATUALIZADO!", 'success')
                    return redirect(url_for('getCarro'))
        except Exception as e:
            print(e)
            return redirect(url_for('getCarro'))






@app.route('/excluirCar')
def excluirCar():
    try:
        session.modified = True
        del session['LojainCarrinho']
        return redirect(url_for('home'))
    except Exception as e:
        print(e)
        return redirect(url_for('home'))
    


@app.route("/deletarItem/<int:code>")
def deletarItem(code):
    try:
        if 'LojainCarrinho' not in session or len(session['LojainCarrinho'])<=0:
            return redirect(url_for('home'))
        
        session.modified = True
        if str(code) in session['LojainCarrinho']:
            session['LojainCarrinho'].pop(str(code))  # Remove diretamente pela chave
            flash("Produto deletado com sucesso!", "warning")

            # Remove o carrinho se ele ficar vazio
            if len(session['LojainCarrinho']) == 0:
                session.pop('LojainCarrinho', None)
                return redirect(url_for('home'))
            
            return redirect(url_for('getCarro'))

        else:
            flash("Item não encontrado no carrinho!", "danger")
            return redirect(url_for('getCarro'))

            
    except:
        flash("Não foi possível deletar o item", "danger")
        return redirect(url_for('getCarro'))
    

@app.route("/limparCarrinho")
def limparCarrinho():
    try:
        if 'LojainCarrinho' not in session or len(session['LojainCarrinho'])<=0:
            return redirect(url_for('home'))
        
        session.modified = True
        session.pop('LojainCarrinho', None)
        flash("Carrinho Limpo!", "warning")

            
        return redirect(url_for('home'))

            
    except:
        flash("Não foi possível deletar o item", "danger")
        return redirect(url_for('getCarro'))