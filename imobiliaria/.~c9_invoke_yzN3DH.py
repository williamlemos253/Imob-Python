# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm 
from wtforms import StringField, SelectField, IntegerField, TextAreaField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Regexp, Length, Required
from app import app, db
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from models import Cidades, Bairros


#consulta no banco de dados para o queryselectfield
def busca_cidades():
    return Cidades.query.all()
    
def busca_bairros():
        return Bairros.query
        return Bairros.query.filter(Baicidade==filtro)

    

class ImovelForm(FlaskForm):
    codigoimovel = StringField('C&oacute;d.:', validators=[DataRequired()])
    tiponegocio = SelectField('Tipo de Neg&oacute;cio', choices=[('venda', 'Venda'), ('aluguel', 'Aluguel')])
    tipoimovel = SelectField('Tipo de Im&oacute;vel', choices=[('apartamento', 'Apartamento'), ('casa', 'Casa'), ('cobertura', 'Cobertura')])
    cidade = QuerySelectField(query_factory=busca_cidades, allow_blank=True, get_label='cidade', get_pk=id)
    bairro = QuerySelectField(query_factory=busca_bairros, allow_blank=True, get_label='bairro'+, get_pk=id)
    descricao = TextAreaField('Cidade', validators=[DataRequired()])
    ndormitorios = IntegerField('Nº de Dormit&oacute;rio', validators=[DataRequired()])
    nsuites =  IntegerField('Nº de Su&iacute;tes', validators=[DataRequired()])
    ngaragem = IntegerField('Nº de Su&iacute;tes', validators=[DataRequired()])
    valor = DecimalField('Valor')
    
class CidadeForm(FlaskForm):
    cidade = StringField('Cidade', validators=[Required()])
    adicionar = SubmitField('Adicionar')
    
class BairroForm(FlaskForm):
    bairro = StringField('Bairro', validators=[Required()])
    adicionar = SubmitField('Adicionar')