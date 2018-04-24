# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm 
from wtforms import StringField, SelectField, IntegerField, TextAreaField, DecimalField, SubmitField, HiddenField, PasswordField, DateField, BooleanField
from wtforms.fields.html5 import IntegerRangeField, EmailField
from wtforms.validators import DataRequired, Regexp, Length, Required, EqualTo
from flask_wtf.file import FileField, FileRequired, FileAllowed
from app import app, db
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from models import Cidades




class ImovelForm(FlaskForm):
    codigoimovel = StringField('', validators=[DataRequired(message="Este campo é obrigatório")])
    tiponegocio = SelectField('', choices=[('Venda', 'Venda'), ('Aluguel', 'Aluguel')])
    tipoimovel = SelectField('', choices=[('Apartamento', 'Apartamento'), ('Casa', 'Casa'), ('Cobertura', 'Cobertura')], validators=[DataRequired()])
    cidade = StringField('', validators=[DataRequired(message="Este campo é obrigatório")])
    bairro = StringField('', validators=[DataRequired(message="Este campo é obrigatório")])
    descricao = TextAreaField('Descrição')
    ndormitorios = IntegerField('', validators=[DataRequired(message="Este campo é obrigatório")])
    nbanheiros = IntegerField('', validators=[DataRequired(message="Este campo é obrigatório")])
    nsuites =  IntegerField('', validators=[DataRequired(message="Este campo é obrigatório")])
    ngaragem = IntegerField('', validators=[DataRequired(message="Este campo é obrigatório")])
    valor = DecimalField('', validators=[DataRequired(message="Este campo é obrigatório")])
    foto = FileField('',validators=[FileRequired(),FileAllowed(['jpg', 'png','jpeg'], 'Somente imagens podem enviadas!')])
    endereco = StringField('', render_kw={"class":"validate"})
    
    
class EditaImovelForm(FlaskForm):
    codigoimovel = StringField('', validators=[DataRequired(message="Este campo é obrigatório")])
    tiponegocio = SelectField('', choices=[('Venda', 'Venda'), ('Aluguel', 'Aluguel')])
    tipoimovel = SelectField('', choices=[('Apartamento', 'Apartamento'), ('Casa', 'Casa'), ('Cobertura', 'Cobertura')], validators=[DataRequired()])
    cidade = StringField('', validators=[DataRequired(message="Este campo é obrigatório")])
    bairro = StringField('')
    descricao = TextAreaField('Descrição')
    ndormitorios = IntegerField('', validators=[DataRequired(message="Este campo é obrigatório")])
    nbanheiros = IntegerField('', validators=[DataRequired(message="Este campo é obrigatório")])
    nsuites =  IntegerField('', validators=[DataRequired(message="Este campo é obrigatório")])
    ngaragem = IntegerField('', validators=[DataRequired(message="Este campo é obrigatório")])
    valor = DecimalField('', validators=[DataRequired(message="Este campo é obrigatório")])
    fotoedicao = FileField('',validators=[FileAllowed(['jpg', 'png','jpeg'], 'Somente imagens podem enviadas!')])
    endereco = StringField('', render_kw={"class":"validate"})
    

class CidadeForm(FlaskForm):
    cidade = StringField('Cidade', validators=[Required()])
    adicionar = SubmitField('Adicionar')

    
class BairroForm(FlaskForm):
    cidade = StringField('', validators=[DataRequired(message="Este campo é obrigatório")])
    bairro = StringField('Bairro', validators=[Required()])
    adicionar = SubmitField('Adicionar')
    
    
class BuscaForm(FlaskForm):
    busca = StringField('Busca')
    enviar = SubmitField('Pesquisar')
    
    
class IndexForm(FlaskForm):
    busca = StringField('')
    cidade = StringField('', validators=[DataRequired(message="Este campo é obrigatório")])
    bairro = StringField('')
    tipoimovel = SelectField('', choices=[('', 'Qualquer'),('Apartamento', 'Apartamento'), ('Casa', 'Casa'), ('Cobertura', 'Cobertura')])
    valorminimo = IntegerField('')
    valormaximo = IntegerField('')
    ndormitorios = IntegerField('')
    nbanheiros = IntegerField('')
    nsuites =  IntegerField('')
    ngaragem = IntegerField('')
    tiponegocio = SelectField('', choices=[('', 'Qualquer'),('Venda', 'Venda'), ('Aluguel', 'Aluguel')])
    enviar = SubmitField('Filtrar')
    
    
class GaleriaForm(FlaskForm):
    fotos = FileField('',validators=[FileRequired(),FileAllowed(['jpg', 'png','jpeg'], 'Somente imagens podem enviadas!')])
    enviar = SubmitField('Enviar')
    
class ContatoForm(FlaskForm):
    nome = StringField("Nome", validators=[Required()])
    email = StringField("E-mail", validators=[Required()])
    telefone = StringField("Telefone para contato", validators=[Required()])
    assunto = StringField("Dúvida", validators=[Required()])
    enviar = SubmitField('Enviar')

class BannerForm(FlaskForm):    
    banner = FileField('',validators=[FileRequired(),FileAllowed(['jpg', 'png','jpeg'], 'Somente imagens podem enviadas!')])
    link = StringField('')
    texto = TextAreaField('')
    posicaotexto = SelectField('', choices=[('caption',''), ('caption center-align', 'Centro' ), ('caption left-align','Esquerda'), 
    ('caption right-align','Direita')])
    

class Formcadastropaciente(FlaskForm):
    username = StringField('Nome de Usário', validators=[DataRequired(), Length(min=6, max=18, message='O nome de Usuário deve ter no mínimo 6 dígitos e no máximo 18'),
    Regexp('^[a-z0-9_-]{3,20}$', message="O nome de usuário não pode conter caracteres especiais, espaços e letras maiúsculas")])
    password = PasswordField('Senha', validators=[Required(), EqualTo('confirm', message='As senhas precisam ser iguais')])
    confirm = PasswordField('Repetir senha', validators=[Required(), EqualTo('password', message='As senhas precisam ser iguais')])
    email = EmailField('E-mail', validators=[Required(), Length(min=2, max=50)])
    datanasc = DateField('Data de nascimento', format="%d/%m/%Y" ,validators=[Required()])
    active = BooleanField('Ativo', default=True)
    first_name =  StringField('Nome', validators=[Required(), Length(min=2, max=50)])
    last_name = StringField('Sobrenome', validators=[Required(), Length(min=2, max=60)])
    sexo = SelectField('Sexo', choices=[('masculino', 'Masculino'), ('feminino', 'Feminino')])
    cpf = StringField('CPF', validators = [Length(min=6, max=16)])
    salvar = SubmitField('Salvar')
    
    
class Formcadastrofuncionario(FlaskForm):
    username = StringField('Nome de Usário', validators=[Required(), Length(min=6, max=18, message='O nome de Usuário deve ter no mínimo 6 dígitos e no máximo 18'),
    Regexp('^[a-z0-9_-]{3,20}$', message="O nome de usuário não pode conter caracteres especiais, espaços e deve ter no mínimo 6 digítos")])
    password = PasswordField('Senha', validators=[Required(), EqualTo('confirm', message='As senhas precisam ser iguais')])
    confirm = PasswordField('Repetir senha', validators=[Required(), EqualTo('password', message='As senhas precisam ser iguais')])
    email = EmailField('E-mail', validators=[Required(), Length(min=2, max=50)])
    datanasc = DateField('Data de nascimento', format='%d/%m/%Y')
    active = BooleanField('Ativo')
    first_name =  StringField('Nome', validators=[Required(), Length(min=2, max=50)])
    last_name = StringField('Sobrenome', validators=[Required(), Length(min=2, max=60)])
    sexo = SelectField('Sexo', choices=[('masculino', 'Masculino'), ('feminino', 'Feminino')])
    cpf = StringField('CPF', validators = [Length(min=6, max=16)])
    salvar = SubmitField('Salvar')