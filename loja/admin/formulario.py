from wtforms import BooleanField, Form, PasswordField, StringField, validators


class Registro(Form):
    name = StringField('Nome', [validators.Length(min=6, max=30)])
    username = StringField('Usuário', [validators.Length(min=6, max=30)])
    email = StringField('E-mail', [validators.Length(min=6, max=40)])
    password = PasswordField('Senha', [
        validators.data_required(), 
        validators.EqualTo("password_confirm", message="Senhas devem ser iguais.")
        ])
    password_confirm = PasswordField("Confirmar Senha")

class Login(Form):
    email = StringField('E-mail', [validators.length(min=6, max=40)])
    password = PasswordField('Senha', [validators.data_required()])