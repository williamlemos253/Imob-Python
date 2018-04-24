# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db, app
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter


class Cidades(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cidade = db.Column(db.String(120), nullable=False, unique=True)
    


    
class Bairros(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cidade = db.Column(db.String(120), nullable=False)
    bairro = db.Column(db.String(120), nullable=False)
    
    
    

class Imoveis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigoimovel = db.Column(db.String(80), unique=True, nullable=False)
    tiponegocio = db.Column(db.String(120), nullable=False)
    tipoimovel = db.Column(db.String(120), nullable=False)
    cidade = db.Column(db.String(120), nullable=False)
    bairro = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.Text)
    ndormitorios = db.Column(db.SmallInteger)
    nsuite = db.Column(db.SmallInteger)
    nbanheiros = db.Column(db.SmallInteger)
    ngaragem = db.Column(db.SmallInteger)
    valor = db.Column(db.Numeric)
    datacadastro = db.Column(db.DateTime, default=datetime.now())
    nomefoto = db.Column(db.String(), nullable=False)
    nomesegurofoto = db.Column(db.String(), nullable=False)
    endereco = db.Column(db.String(), nullable=True)
    
class Fotos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imovelid = db.Column(db.Integer, db.ForeignKey('imoveis.id',  ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    nomefoto = db.Column(db.String(), nullable=False)
    nomesegurofoto = db.Column(db.String(), nullable=False)
    
    
class Banners(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nomebanner = db.Column(db.String(), nullable=False)
    nomesegurobanner = db.Column(db.String(), nullable=False)
    link = db.Column(db.String(), nullable=True)
    texto = db.Column(db.String(120), nullable=True)
    posicaotexto = db.Column(db.String(50), nullable=True)
    
    
# Define the User data model. Make sure to add flask_user UserMixin!!
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    # User authentication information
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')

    # User email information
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())

    # User information
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')
    
    
    #campos extras dos usuarios
    sexo = db.Column(db.String(15), nullable=False)
    datanasc = db.Column(db.DateTime, nullable=False)
    corretor = db.Column(db.Boolean(), nullable=False, server_default='0')
    cpf = db.Column(db.String(15), nullable=True, unique=True)

    # Relationships
    roles = db.relationship('Role', secondary='user_roles',
            backref=db.backref('users', lazy='dynamic'))

# Define the Role data model
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    
    def init_db():
        if db.session.query(Role).count() == 0:
            admin = Role("corretor")
            db.session.add(admin)
            db.session.commit()
    

# Define the UserRoles data model
class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))


# Setup Flask-User
db_adapter = SQLAlchemyAdapter(db,  User)
user_manager = UserManager(db_adapter, app)