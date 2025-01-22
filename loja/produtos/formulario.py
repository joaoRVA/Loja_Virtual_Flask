from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import (DecimalField, Form, IntegerField, PasswordField,
                     StringField, TextAreaField, validators)


class AddProdutos(Form):
    name = StringField('nome :', [validators.DataRequired()])
    price = DecimalField('Preço :', [validators.DataRequired()])
    discount = IntegerField('Desconto :', [validators.DataRequired()])
    stock = IntegerField('Estoque :', [validators.DataRequired()])
    description = TextAreaField('Descrição :', [validators.DataRequired()])
    colors = TextAreaField('Cor :', [validators.DataRequired()])
    
    image_1 = FileField('image 1 :', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    image_2 = FileField('image 2 :', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    image_3 = FileField('image 3 :', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])