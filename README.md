### Loja Virtual com Flask  

Este repositório contém o código de uma **loja virtual** desenvolvida com o framework Flask e Python. O projeto inclui funcionalidades completas para gerenciar produtos, realizar compras e gerar notas fiscais, proporcionando uma experiência prática e moderna tanto para administradores quanto para clientes.  

---

## 🛠️ Funcionalidades  

- **Autenticação**:  
  - Login e cadastro de clientes e administradores com níveis de acesso diferenciados.  
  - Segurança no armazenamento de senhas utilizando hashing.  

- **Gerenciamento de Produtos**:  
  - Admins podem adicionar, editar e excluir produtos.  
  - Gerenciamento de informações como nome, preço, descrição e imagem.  

- **Processo de Compra**:  
  - Integração com o **Stripe** para pagamento seguro e eficiente.  

- **Geração de Notas Fiscais**:  
  - Após a compra, o cliente recebe automaticamente uma nota fiscal em PDF gerada com o **pdfkit** e o **wkhtmltopdf**.  
 

---

## 🛠️ Tecnologias Utilizadas  

- **Backend**: Flask (Python)  
- **Banco de Dados**: SQLAlchemy  
- **Pagamento Online**: Stripe API  
- **Geração de PDFs**: pdfkit e wkhtmltopdf  
- **Frontend**: HTML, CSS, Bootstrap  

---

## 🚀 Como Executar o Projeto  

1. **Clone o Repositório**  
   ```bash
   git clone https://github.com/joaoRVA/Loja_Virtual_Flask.git
   ```  

2. **Crie e Ative um Ambiente Virtual**  
   ```bash
   python -m venv venv
   source venv/bin/activate   # No Windows: venv\Scripts\activate
   ```  

3. **Instale as Dependências**  
   ```bash
   pip install -r requirements.txt
   ```  

4. **Configure as suas keys do Stripe**
   Para saber a sua key, crie uma conta em: https://dashboard.stripe.com
   Modifique essas variáveis pelas suas keys em `clientes/rotas.py`
   ```bash
   publishable_key = sua_chave_publica_do_stripe
   stripe.api_key = sua_chave_secreta_do_stripe
   ```

5. **Inicialize o Banco de Dados**  
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```  

 

---

## 📄 Requisitos  

- Python 3.8+  
- Flask 2.0+  
- wkhtmltopdf instalado e configurado no sistema  

---

## 📷 Demonstração  

- **Cadastro de Produtos (Admin)**:  
  ![Cadastro de Produtos](https://imgur.com/L0EJ6CL)  

- **Tela de Gerenciamento de Produtos (Admin)**:  
  ![Tela de Gerenciamento](https://imgur.com/axwhfJi)
  
- **Tela de Compra**:  
  ![Tela de Compra](https://imgur.com/h3WdJ0o)

- **Tela de Carrinho**:  
  ![Tela de Carrinho](https://imgur.com/nhLdmGL)
  
- **Nota Fiscal Gerada**:  
  ![Nota Fiscal](https://imgur.com/h5DJ7TA)  

---

## 🤝 Contribuições  

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma **issue** ou enviar um **pull request**.  

---

## 📧 Contato  

Em caso de dúvidas ou sugestões, entre em contato:  
- **Email**: joaovitordeaquino20@gmail.com
- **LinkedIn**: [Seu Perfil](linkedin.com/in/joão-vítor-rodrigues-8a6320242/)  

---  

### 🌟 Não se esqueça de deixar uma ⭐ se este projeto foi útil para você!  
