# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect
from app import app, db
from models import Imoveis, Bairros, Fotos, Cidades, Banners
from forms import IndexForm, ContatoForm
import urllib



@app.route('/', defaults={'pagina': 1 })
@app.route('/<int:pagina>', methods = ['GET','POST'])
def index(pagina):
    
    buscacidades = Cidades.query.order_by(Cidades.cidade).all()
    buscabanner = Banners.query.all()
    
 
    form = IndexForm()

 
    imoveis = funcbuscaimoveis()
    if request.method == 'POST':
        if form.cidade.data:
            imoveis = imoveis.filter(Imoveis.cidade==form.cidade.data)
        if form.bairro.data:
            imoveis = imoveis.filter(Imoveis.bairro==form.bairro.data)
        if form.tiponegocio.data:
            imoveis = imoveis.filter(Imoveis.tiponegocio==form.tiponegocio.data)
        if form.tipoimovel.data:
            imoveis = imoveis.filter(Imoveis.tipoimovel==form.tipoimovel.data)
        if form.valorminimo.data:
            imoveis = imoveis.filter(Imoveis.valor>=form.valorminimo.data)
        if form.valormaximo.data:
            imoveis = imoveis.filter(Imoveis.valor<=form.valormaximo.data)
        if form.nbanheiros.data:
            imoveis = imoveis.filter(Imoveis.nbanheiros==form.nbanheiros.data)
        if form.nbanheiros.data:
            imoveis = imoveis.filter(Imoveis.nbanheiros==form.nbanheiros.data)
        if form.nsuites.data:
            imoveis = imoveis.filter(Imoveis.nsuites==form.nsuites.data)
        if form.ngaragem.data:
            imoveis = imoveis.filter(Imoveis.ngaragem==form.ngaragem.data)
        if form.busca.data:
            imoveis = imoveis.filter(Imoveis.codigoimovel.ilike("%"+form.busca.data+"%"))
            


    novapagina = (pagina-1) * 12
    contador = imoveis.count()
    imoveis = imoveis.limit(12).offset(novapagina).all()
    
    

    
    
    #logica da paginacao
    npaginas = 1
    while(contador>=1):
        contador = contador - 12
        npaginas = npaginas + 1

    paginacao = []
    paginacao = range(1,npaginas)
  
    
    return render_template('index.html', imoveis=imoveis, form=form, paginaatual=pagina, npaginas=npaginas, paginacao=paginacao, buscacidades=buscacidades, buscabanner=buscabanner)
    
    
@app.route('/imovel/<int:id>')
def imovel(id):
    fotos = Fotos.query.filter(Fotos.imovelid==id).all()
    form =ContatoForm()
    buscaimovel = Imoveis.query.filter(Imoveis.id==id).first()
    return render_template('imovel.html', imovel=buscaimovel, form=form, fotos=fotos, id=id)

    
def funcbuscaimoveis():
    imoveis = Imoveis.query
    return imoveis
    
    
@app.route('/apibairros/', methods =['GET'])
def apibairros():
    cidade = request.args.get('cidade')
    bairros = Bairros.query.filter(Bairros.cidade==cidade).all()
    
    return render_template('api/apibairros.html', bairros=bairros)
    
    
@app.route('/apicidades/<int:id>')
def apicidades(id):
    cidade = Imoveis.query.filter(Imoveis.id==id).first()
    cidades = Cidades.query.all()
    
    return render_template('api/apicidades.html', cidades=cidades, cidade=cidade)