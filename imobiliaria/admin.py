# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, flash, redirect
from app import app, db
from models import Imoveis, Bairros, Fotos, Cidades, Banners
from forms import ImovelForm, BairroForm, BuscaForm, GaleriaForm, EditaImovelForm, CidadeForm, BannerForm
from werkzeug.utils import secure_filename
import os
import time
from PIL import Image, ImageDraw
from sqlalchemy import exc
import shutil




ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


@app.route('/admin')
def admin():
    
    return render_template('admin/admin.html')


@app.route('/cadastro', methods = ['POST', 'GET'])
def cadastro():
    buscabairro = Bairros.query.order_by(Bairros.cidade,Bairros.bairro).all()
    buscacidades = Cidades.query.order_by(Cidades.cidade).all()
    form = ImovelForm()

    buscabairro = Bairros.query.order_by(Bairros.cidade,Bairros.bairro).all()
    if request.method == 'POST':
        if form.validate_on_submit():
            codigoimovel = form.codigoimovel.data
            #valida se o código do imóvel não está em uso
            validacodigo = Imoveis.query.filter(Imoveis.codigoimovel==codigoimovel).first()
            if validacodigo:
                flash('O código do imóvel já está em uso')
                return render_template('admin/cadastro.html', form=form, buscabairro=buscabairro)
            tiponegocio = form.tiponegocio.data
            tipoimovel = form.tipoimovel.data
            cidade =  form.cidade.data
            bairro = form.bairro.data
            descricao = form.descricao.data
            ndormitorios = form.ndormitorios.data
            nsuites =  form.nsuites.data
            nbanheiros = form.nbanheiros.data
            ngaragem = form.ngaragem.data
            valor = form.valor.data
            endereco = form.endereco.data
            
            # check if the post request has the file part
            if 'foto' not in request.files:
                flash('Houve um erro durante o upload da imagem, por favor tente novamente')
                return redirect(request.url)
            foto = request.files['foto']
            # if user does not select file, browser also
            # submit a empty part without filename
            if foto.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(foto.filename):
                print 'chegamos no salvamento do arquivo'
                #chega se o nome é seguro a adiciona data e hora para evitar nomes repetidos de foto
                filename = secure_filename(codigoimovel+"-"+ time.strftime('%Y-%m-%d %H:%M:%S') + foto.filename)
                #salva todos os dados no banco
                dados = Imoveis(codigoimovel=codigoimovel, tiponegocio=tiponegocio, tipoimovel=tipoimovel,
                                cidade=cidade, bairro=bairro, descricao=descricao, ndormitorios=ndormitorios, 
                                nsuite=nsuites, ngaragem=ngaragem, valor=valor, nomefoto=str(foto.filename),
                                nbanheiros=nbanheiros, nomesegurofoto=str(filename), endereco=endereco)
                                
                try:    
                    db.session.add(dados)
                except:
                    flash("Ocorreu um erro ao cadastrar o imóvel")
        
                
                
                #salva a foto na pasta    
                foto.save(os.path.join(app.config['UPLOAD_FOLDER']+"/destaque/", filename))
                
   
                 #adiciona  marca da água
                photo = Image.open(app.config['UPLOAD_FOLDER']+"/destaque/"+filename)
                width, height = photo.size
                watermark = Image.open('./imobiliaria/static/uploads/watermark/watermark.png')
                photo.paste(watermark, (int(width/3.5), int(height/2.1)), watermark)
                photo.save(os.path.join(app.config['UPLOAD_FOLDER']+"/destaque/", filename))
                
                #compacta a foto 
                img = Image.open(app.config['UPLOAD_FOLDER']+"/destaque/"+filename)
                new_img = img.resize((1500,900))
                new_img.save(app.config['UPLOAD_FOLDER']+"/destaque/"+filename, "JPEG", optimize=True)
                
           
                #cria o thumbnail
                thumbnail = img.resize((320,190))
                thumbnail.save(app.config['UPLOAD_FOLDER']+"/thumb/"+filename, "JPEG", optimize=True)
             
                
                db.session.commit()
                
                return redirect('/buscaimoveis')
                
        else:
            flash('Por favor verifique se preencheu todos os campos corretamente')
              

    return render_template('admin/cadastro.html', form=form, buscabairro=buscabairro, buscacidades=buscacidades)
    
    
    

@app.route('/criabairro', methods = ['POST', 'GET'])
def criabairro():
    form = BairroForm()
    buscabairros  = Bairros.query.order_by(Bairros.cidade).all()
    buscacidades = Cidades.query.order_by(Cidades.cidade).all()
    if request.method == 'POST':
        if form.validate_on_submit():
            bairro = form.bairro.data
            cidade = form.cidade.data
            novobairro = Bairros(bairro=bairro, cidade=cidade)
            db.session.add(novobairro)
            db.session.commit()
            return redirect('/criabairro')
            flash('Bairro cadastrado com sucesso')
        else:
            flash('Por favor certifique-se de ter preenchido todos os campos corretamente')
    return render_template('admin/criabairro.html', form=form, buscabairros=buscabairros, buscacidades=buscacidades)
    



@app.route('/deletabairro/<int:id>', methods = ['POST', 'GET'])
def deletabairro(id):
    buscabairros = Bairros.query.filter(Bairros.id==id).first()
    db.session.delete(buscabairros)
    db.session.commit()
    flash('Bairro apagado com sucesso')
    return redirect('/criabairro')
    
    
@app.route('/criacidade', methods = ['POST', 'GET'])
def criacidade():
    form = CidadeForm()
    buscacidades  = Cidades.query.all()
    if request.method == 'POST':
        if form.validate_on_submit():
            cidade = form.cidade.data
            novacidade = Cidades(cidade=cidade)
            db.session.add(novacidade)
            db.session.commit()
            buscacidades = Cidades.query.order_by(Cidades.id.desc()).limit(1).all()
            return redirect('/criabairro')
            flash('Cidade cadastrada com sucesso')
        else:
            flash('Por favor certifique-se de ter preenchido todos os campos corretamente')
            
    return render_template('admin/criacidade.html', form=form, buscacidades=buscacidades)
    


@app.route('/galeria/<int:id>', methods = ['POST', 'GET'])
def galeria(id):
    buscafotos = Fotos.query.filter(Fotos.imovelid==id).all()
  
    
    #cria pasta com id do imovel
    try:
        os.stat(app.config['UPLOAD_FOLDER']+"/album/"+str(id))
    except:
        os.mkdir(app.config['UPLOAD_FOLDER']+"/album/"+str(id))
    
    
    
    if request.method == 'POST':
        for f in request.files.getlist('file'):
            if allowed_file(f.filename):
                nomefoto = str(f.filename)
                filename = secure_filename(str(id)+"-"+ time.strftime('%Y-%m-%d %H:%M:%S') + f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER']+"/album/"+str(id)+"/", filename))
                
                #adiciona  marca da água
                photo = Image.open(app.config['UPLOAD_FOLDER']+"/album/"+str(id)+"/"+filename)
                width, height = photo.size
                watermark = Image.open('./imobiliaria/static/uploads/watermark/watermark.png')
                photo.paste(watermark, (int(width/3.5), int(height/2.1)), watermark)
                photo.save(os.path.join(app.config['UPLOAD_FOLDER']+"/album/"+str(id)+"/", filename))
                
                #compacta a foto 
                img = Image.open(app.config['UPLOAD_FOLDER']+"/album/"+str(id)+"/"+filename)
                new_img = img.resize((1500,900))
                new_img.save(app.config['UPLOAD_FOLDER']+"/album/"+str(id)+"/"+filename, "JPEG", optimize=True)
                
                
                
                db.session.add(Fotos(imovelid=id, nomefoto=nomefoto, nomesegurofoto=filename))
                db.session.commit()
            else:
                flash("A foto não está em um formatado permitido")
            
        return redirect('/galeria/'+str(id))    
            
    
    
    return render_template('admin/galeria.html', fotos=buscafotos, id=id)
    
    
    
@app.route('/deletafoto/<int:id>')
def deletafoto(id):
    buscafoto = Fotos.query.filter(Fotos.id==id).first()
    
    try:
         os.remove(app.config['UPLOAD_FOLDER']+"/album/"+str(buscafoto.imovelid)+"/"+buscafoto.nomesegurofoto)
    except:
        pass
    
    db.session.delete(buscafoto)
    db.session.commit()
    flash('Foto deletada com sucesso')
    
    return redirect('/galeria/'+str(buscafoto.imovelid))
    
    
@app.route('/deletaimovel/<int:id>')
def deletaimovel(id):
    buscaimovel = Imoveis.query.filter(Imoveis.id==id).first()
    
    try:
        #shutil remove pastas inteiras e os.remove apenas arquivos
        shutil.rmtree(app.config['UPLOAD_FOLDER']+"/album/"+str(buscaimovel.id)+"/")
        os.remove(app.config['UPLOAD_FOLDER']+"/destaque/"+buscaimovel.nomesegurofoto)
        os.remove(app.config['UPLOAD_FOLDER']+"/thumb/"+buscaimovel.nomesegurofoto)

    except:
        db.session.rollback()
        flash('Occoreu um erro ao remover o imóvel')
    
    db.session.delete(buscaimovel)
    db.session.commit()
    
    return redirect('/buscaimoveis/')
    
    
    

    
@app.route('/buscaimoveis/', defaults={'pagina' : 1})
@app.route('/buscaimoveis/<int:pagina>', methods =['POST','GET'])
def buscaimoveis(pagina):
    form = BuscaForm()
    novapagina = (pagina-1) * 12
    if request.method == 'POST':
        if form.validate_on_submit():
            pesquisa = form.busca.data
            imoveis = Imoveis.query.filter((Imoveis.descricao.like('%'+pesquisa+'%')) | (Imoveis.codigoimovel.ilike('%'+pesquisa+'%')) 
                                             | (Imoveis.cidade.ilike('%'+pesquisa+'%'))  | (Imoveis.bairro.ilike('%'+pesquisa+'%'))  
                                             | (Imoveis.tiponegocio.ilike('%'+pesquisa+'%')) | (Imoveis.tipoimovel.ilike('%'+pesquisa+'%')))
            contador = imoveis.count()
    else:
        imoveis = Imoveis.query.order_by(Imoveis.datacadastro).limit(12)
        contador = Imoveis.query.count()
    
    
   
    #logica da paginacao
    npaginas = 1
    while(contador>=1):
        contador = contador - 12
        npaginas = npaginas + 1
    
    paginacao = []
    paginacao = range(1,npaginas)
    
    return render_template('admin/buscaimoveis.html', buscaimoveis=imoveis, paginaatual=pagina, npaginas=npaginas, paginacao=paginacao, form=form)
    
    
    
@app.route('/editaimovel/<int:id>', methods = ['POST', 'GET'])
def editarimovel(id):
    buscaimovel = Imoveis.query.filter(Imoveis.id==id).first()
    form = EditaImovelForm()
    
   
 
    buscabairro = Bairros.query.order_by(Bairros.cidade,Bairros.bairro).all()
    buscacidades = Cidades.query.order_by(Cidades.cidade).all()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            #valida se o código do imóvel não está em uso
            validacodigo = Imoveis.query.filter(Imoveis.codigoimovel==form.codigoimovel.data).first()
            if validacodigo.codigoimovel is not buscaimovel.codigoimovel:
                flash('O código do imóvel já está em uso')
                return redirect('editaimovel/'+str(id))
                
            buscaimovel.codigoimovel = form.codigoimovel.data
            buscaimovel.tiponegocio = form.tiponegocio.data
            buscaimovel.tipoimovel = form.tipoimovel.data
            buscaimovel.cidade =  form.cidade.data
            buscaimovel.bairro = form.bairro.data
            buscaimovel.descricao = form.descricao.data
            buscaimovel.ndormitorios = form.ndormitorios.data
            buscaimovel.nsuites =  form.nsuites.data
            buscaimovel.nbanheiros = form.nbanheiros.data
            buscaimovel.ngaragem = form.ngaragem.data
            buscaimovel.valor = form.valor.data
            buscaimovel.endereco = form.endereco.data
            
            # check if the post request has the file part
            if 'fotoedicao' not in request.files:
                nomeseguro = buscaimovel.nomesegurofoto
                nomefoto = buscaimovel.nomefoto
            
            try:  
                foto = request.files['fotoedicao']
            except:
                nomeseguro = buscaimovel.nomesegurofoto
                nomefoto = buscaimovel.nomefoto
                foto = None
            
            # if user does not select file, browser also
            # submit a empty part without filename
            if foto:
                if file and allowed_file(foto.filename):
                    #remove a foto antigo
                    nomeseguro = buscaimovel.nomesegurofoto
                    nomefoto = buscaimovel.nomefoto
                    try:
                        os.remove(app.config['UPLOAD_FOLDER']+"/destaque/"+nomeseguro)
                        os.remove(app.config['UPLOAD_FOLDER']+"/thumb/"+nomeseguro)
                    except Exception as error:
                        app.logger.error("Por favor coloque uma foto de destaque", error)
                    
                    
                    nomefoto = foto.filename
        
                    #checa se o nome é seguro a adiciona data e hora para evitar nomes repetidos de foto
                    filename = secure_filename(buscaimovel.codigoimovel+"-"+ time.strftime('%Y-%m-%d %H:%M:%S') + foto.filename)
                    #salva todos os dados no banco
                    
                    nomeseguro = filename
                    
                    
               
                    #salva a foto na pasta    
                    foto.save(os.path.join(app.config['UPLOAD_FOLDER']+"/destaque/", filename))
                    
       
                     #adiciona  marca da água
                    photo = Image.open(app.config['UPLOAD_FOLDER']+"/destaque/"+filename)
                    width, height = photo.size
                    watermark = Image.open('./imobiliaria/static/uploads/watermark/watermark.png')
                    photo.paste(watermark, (int(width/3.5), int(height/2.1)), watermark)
                    photo.save(os.path.join(app.config['UPLOAD_FOLDER']+"/destaque/", filename))
                    
                    #compacta a foto 
                    img = Image.open(app.config['UPLOAD_FOLDER']+"/destaque/"+filename)
                    new_img = img.resize((1500,900))
                    new_img.save(app.config['UPLOAD_FOLDER']+"/destaque/"+filename, "JPEG", optimize=True)
                    
               
                    #cria o thumbnail
                    thumbnail = img.resize((320,190))
                    thumbnail.save(app.config['UPLOAD_FOLDER']+"/thumb/"+filename, "JPEG", optimize=True)
                 
                    buscaimovel.nomefoto = nomefoto
                    buscaimovel.nomesegurofoto = nomeseguro
           
            try:    
                db.session.commit()
                flash("Dados atualizados com sucesso")
                return redirect('/buscaimoveis')
            except exc.IntegrityError as e:
                db.session().rollback()
                flash('O código do imóvel já está em uso')
                
        else:
            flash('Por favor verifique se preencheu todos os campos do formulário corretamente')
            
            
            
    form.codigoimovel.data = buscaimovel.codigoimovel
    form.tiponegocio.data = buscaimovel.tiponegocio
    form.tipoimovel.data = buscaimovel.tipoimovel
    form.valor.data = buscaimovel.valor
    form.cidade.data = buscaimovel.cidade
    form.bairro.data = buscaimovel.bairro
    form.ndormitorios.data = buscaimovel.ndormitorios
    form.nsuites.data = buscaimovel.nsuite
    form.nbanheiros.data = buscaimovel.nbanheiros
    form.ngaragem.data = buscaimovel.ngaragem
    form.endereco.data = buscaimovel.endereco
    form.descricao.data = buscaimovel.descricao
    
    return render_template('admin/editaimovel.html', form=form, imovel=buscaimovel, id=id, buscacidades=buscacidades)    
    


@app.route('/criabanner', methods = ['POST', 'GET'])
def banner():
    buscabanner = Banners.query.all()
    form = BannerForm()
    link = form.link.data
    texto = form.texto.data
    posicaotexto = form.posicaotexto.data
    
    if request.method == 'POST':
        # check if the post request has the file part
        if 'banner' not in request.files:
            flash('Houve um erro durante o upload do banner, por favor tente novamente')
            return redirect(request.url)
        banner = request.files['banner']
        # if user does not select file, browser also
        # submit a empty part without filename
        if banner.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(banner.filename):
            print 'chegamos no salvamento do arquivo'
            #chega se o nome é seguro a adiciona data e hora para evitar nomes repetidos de foto
            filename = secure_filename("banner-"+ time.strftime('%Y-%m-%d %H:%M:%S') + banner.filename)
            banner.save(os.path.join(app.config['UPLOAD_FOLDER']+"/banner/", filename))
            
            banners = Banners(nomebanner = banner.filename, nomesegurobanner = filename, link = link, posicaotexto = posicaotexto, texto=texto )
            
            db.session.add(banners)
            
            db.session.commit()
            
            return redirect('/criabanner')

    
    return render_template('admin/criabanner.html', form=form, buscabanner=buscabanner)
    

@app.route('/removebanner/<int:id>')
def removebanner(id):
    buscabanner = Banners.query.filter(Banners.id==id).first()
    
    os.remove(app.config['UPLOAD_FOLDER']+"/banner/"+buscabanner.nomesegurobanner)
    
    db.session.delete(buscabanner)
    
    db.session.commit()
    
    return redirect('/criabanner')


#funcao para tipos de arquivos no upload    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    
