from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import (DecimalField, Form, IntegerField, PasswordField,
                     StringField, SubmitField, TextAreaField, ValidationError,
                     validators)

from .models import Cadastro


class CadastroClienteForm(FlaskForm):
    name = StringField('Nome : ')
    username = StringField('Usuário : ', [validators.data_required()])
    email = StringField('E-mail : ', [validators.data_required()])
    password = PasswordField('Senha : ', [
        validators.data_required(), 
        validators.EqualTo("password_confirm", message="Senhas devem ser iguais.")
        ])
    password_confirm = PasswordField("Confirmar Senha : ")
    country = StringField('País : ', [validators.data_required()])
    state = StringField('Estado : ', [validators.data_required()])
    city = StringField('City : ', [validators.data_required()])
    contact = StringField('Contato : ', [validators.data_required()])
    address = StringField('Endereço : ', [validators.data_required()])
    zipcode = StringField('Caixa Postal : ', [validators.data_required()])
    profile = FileField('Foto de Perfil : ', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Apenas Fotos')])
    submit = SubmitField('Cadastrar')


    def validate_username(self, username):
        if Cadastro.query.filter_by(username=username.data).first():
            raise ValidationError("Este username já existe no site!")
    def validate_email(self, email):
        if Cadastro.query.filter_by(email=email.data).first():
            raise ValidationError("Este e-mail já existe no site!")
        


class LoginClienteForm(FlaskForm):
    email = StringField('E-mail : ', [validators.data_required()])
    password = PasswordField('Senha : ', {validators.data_required()})
    submit = SubmitField('Login')