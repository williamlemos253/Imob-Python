#coding: UTF-8
from app import app, db
from models import User, UserRoles, Role
from flask import render_template, redirect, url_for, request, flash
from flask_user import login_required
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from forms import Formcadastropaciente, Formcadastrofuncionario
import bcrypt
import re

validausernameregex = re.compile("^[a-z0-9_-]{3,20}$")
validadataregex = re.compile("^([0]?[1-9]|[1|2][0-9]|[3][0|1])[./-]([0]?[1-9]|[1][0-2])[./-]([0-9]{4}|[0-9]{2})$")

@app.route('/funcionarios')
@login_required
def funcionarios():
    usuarios = User.query.filter(User.corretor==True)
    return render_template('usuarios/funcionarios.html', usuarios=usuarios)



@app.route('/cadastropaciente', methods=('GET', 'POST'))
@login_required
def cadastropaciente():
    form = Formcadastropaciente()
    
    formusuario = form.username.data
    formemail = form.email.data
    formcpf = form.cpf.data
    validausername = User.query.filter(User.username==formusuario).first()
    validaemail = User.query.filter(User.email==formemail).first()
    validacpf = User.query.filter(User.cpf==formcpf).first()
    
    if not form.username.data is None:
        if not form.email.data is None:
            if not form.cpf.data is None:
                if not validausername is None:
                   if validausername.username == form.username.data:
                        flash('Esse nome de usuário já está em uso', 'danger')
                        return render_template('cadastropaciente.html', Formcadastropaciente=form)
                elif not validaemail is None:
                    if validaemail.email == form.email.data:
                        flash('Esse endereço de e-mail já está em uso', 'danger')
                        return render_template('cadastropaciente.html', Formcadastropaciente=form)
                elif not validausernameregex.match(str(formusuario)):
                    flash('O nome de usuário não pode conter caracteres especiais e espaços', 'danger')
                    return render_template('cadastropaciente.html', Formcadastropaciente=form)
                elif not form.password.data == form.confirm.data:
                    flash('As senhas não são iguais', 'danger')
                    return render_template('cadastropaciente.html', Formcadastropaciente=form)
                elif not validacpf is None:
                    if validacpf.cpf == form.cpf.data:
                        flash('Esse CPF já foi cadastrado', 'danger')
                        return render_template('cadastropaciente.html', Formcadastrofuncionario=form)
                else:    
                    if form.validate_on_submit():
                        password2 = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())
                        cadastro = User(username=form.username.data, password=password2, email=form.email.data, active=form.active.data,
                        first_name=form.first_name.data, last_name=form.last_name.data, sexo=form.sexo.data, datanasc=form.datanasc.data, paciente=True, cpf=form.cpf.data)
                        db.session.add(cadastro)
                        db.session.commit()
                        flash('Paciente cadastrado com sucesso', 'success')
                        return redirect("/")
    return render_template('cadastropaciente.html', Formcadastropaciente=form)
    
@app.route('/editapaciente/')
@app.route('/editapaciente/<int:id>', methods=('GET', 'POST'))
@login_required
def editapaciente(id):
    form = Formcadastropaciente()
    usuarios = User.query.filter(User.paciente==True, User.id==id).first()
    datanasc = str(usuarios.datanasc.strftime("%d/%m/%Y"))
    
    validauser = User.query.filter(User.username==form.username.data).first()
    validaemail = User.query.filter(User.email==form.email.data).first()
    validacpf = User.query.filter(User.cpf==form.cpf.data).first()
    
    if request.method == 'GET':
        form.sexo.data = usuarios.sexo
    
    "valida nome de usuário se já não existe na base de dados"
    if request.method == 'POST':
        if validauser is None:
            usuarios.username = form.username.data
        elif validauser.id == id:
            usuarios.username = form.username.data
        else:
            flash("O nome de usuário já está em uso", "danger")
            return redirect("/editapaciente/"+str(id))
            
        "valida data de nascimento"
        if validadataregex.match(str(form.datanasc.data)):
            flash("A data de nascimento precisa estar em um formato válido ex: 01/01/1991", "danger")
            return redirect("/editapaciente/"+str(id))
            
        "valida email se já não existe na base de dados"
        if validaemail is None:
            usuarios.email = form.email.data
        elif validaemail.id == id:
            usuarios.email = form.email.data
        else:
            flash("O email informado já está em uso por outro usuário", "danger")
            return redirect("/editapaciente/"+str(id))
            
        "valida cpf se já não existe na base de dados"
        if validacpf is None:
            usuarios.cpf = form.cpf.data
        elif validacpf.id == id:
            usuarios.cpf = form.cpf.data
        else:
            flash("O cpf informado já está em uso por outro usuário", "danger")
            return redirect("/editapaciente/"+str(id))
            
        
        usuarios.email = form.email.data
        usuarios.first_name = form.first_name.data
        usuarios.last_name = form.last_name.data
        usuarios.sexo = form.sexo.data
        usuarios.datanasc = form.datanasc.data
        usuarios.active = form.active.data
        usuarios.cpf= form.cpf.data
        db.session.commit()
        print("dados atualizados")
        flash("Registro atualizado com sucesso", "success")
        return redirect("/pacientesbusca")
    
    return render_template('editapaciente.html', usuarios=usuarios, Formcadastropaciente = form, datanasc=datanasc)


@app.route('/cadastrodefuncionario', methods=('GET', 'POST'))
def cadastrodefuncionario():
    form = Formcadastrofuncionario()
    
    formusuario = form.username.data
    formemail = form.email.data
    formcpf = form.cpf.data
    validausername = User.query.filter(User.username==formusuario).first()
    validaemail = User.query.filter(User.email==formemail).first()
    validacpf = User.query.filter(User.cpf==formcpf).first()
    
    if not form.username.data is None:
        if not form.email.data is None:
            if not form.cpf.data is None:
                if not validausername is None:
                    if validausername.username == form.username.data:
                        flash('Esse nome de usuário já está em uso', 'danger')
                        return render_template('usuarios/cadastrodefuncionario.html', Formcadastrofuncionario=form)
                elif not validaemail is None:
                    if validaemail.email == form.email.data:
                        flash('Esse endereço de e-mail já está em uso', 'danger')
                        return render_template('usuarios/cadastrodefuncionario.html', Formcadastrofuncionario=form)
                elif not validausernameregex.match(str(formusuario)):
                    flash('O nome de usuário não pode conter caracteres especiais e espaços', 'danger')
                    return render_template('usuarios/cadastrodefuncionario.html', Formcadastrofuncionario=form)
                elif not form.password.data == form.confirm.data:
                    flash('As senhas não são iguais', 'danger')
                    return render_template('usuarios/cadastrodefuncionario.html', Formcadastrofuncionario=form)
                elif not validacpf is None:
                    if validacpf.cpf == form.cpf.data:
                        flash('Esse CPF já foi cadastrado', 'danger')
                        return render_template('usuarios/cadastrodefuncionario.html', Formcadastrofuncionario=form)
                else:    
                    if form.validate_on_submit():
                        password2 = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())
                        cadastro = User(username=form.username.data, password=password2, email=form.email.data, active=form.active.data,
                        first_name=form.first_name.data, last_name=form.last_name.data, sexo=form.sexo.data, datanasc=form.datanasc.data, corretor=True, cpf=form.cpf.data)
                        
                        db.session.add(cadastro)
                        db.session.commit()
                        userobj = User.query.filter(User.username==formusuario).first()
                        roleobj = Role.query.filter(Role.name=="corretor").first()
                
                        if not roleobj is None:
                            funcao = UserRoles(userobj.id, roleobj.id)
                            db.session.add(funcao)
                            db.session.commit()
                            flash('Funcionário cadastrado com sucesso', 'success')
                            return redirect("/funcionarios")
    return render_template('usuarios/cadastrodefuncionario.html', Formcadastrofuncionario=form)
    
    
    
    
@app.route('/editafuncionario/')
@app.route('/editafuncionario/<int:id>', methods=('GET', 'POST'))
#@login_required
def editafuncionario(id):
    form = Formcadastrofuncionario()
    usuarios = User.query.filter(User.corretor==True, User.id==id).first()
    datanasc = str(usuarios.datanasc.strftime("%d/%m/%Y"))
    
    validauser = User.query.filter(User.username==form.username.data).first()
    validaemail = User.query.filter(User.email==form.email.data).first()
    validacpf = User.query.filter(User.cpf==form.cpf.data).first()
    
    if request.method == 'GET':
        form.sexo.data = usuarios.sexo
    
    "valida nome de usuário se já não existe na base de dados"
    if request.method == 'POST':
        if validauser is None:
            usuarios.username = form.username.data
        elif validauser.id == id:
            usuarios.username = form.username.data
        else:
            flash("O nome de usuário já está em uso", "danger")
            return redirect("usuarios/editafuncionario/"+str(id))
            
        "valida data de nascimento"
        if validadataregex.match(str(form.datanasc.data)):
            flash("A data de nascimento precisa estar em um formato válido ex: 01/01/1991", "danger")
            return redirect("usuarios/editafuncionario/"+str(id))
            
        "valida email se já não existe na base de dados"
        if validaemail is None:
            usuarios.email = form.email.data
        elif validaemail.id == id:
            usuarios.email = form.email.data
        else:
            flash("O email informado já está em uso por outro usuário", "danger")
            return redirect("usuarios/editafuncionario/"+str(id))
            
        "valida cpf se já não existe na base de dados"
        if validacpf is None:
            usuarios.cpf = form.cpf.data
        elif validacpf.id == id:
            usuarios.cpf = form.cpf.data
        else:
            flash("O cpf informado já está em uso por outro usuário", "danger")
            return redirect("usuarios/editafuncionario/"+str(id))
            
        
        usuarios.email = form.email.data
        usuarios.first_name = form.first_name.data
        usuarios.last_name = form.last_name.data
        usuarios.sexo = form.sexo.data
        usuarios.datanasc = form.datanasc.data
        usuarios.active = form.active.data
        usuarios.cpf= form.cpf.data
        db.session.commit()
        flash("Registro atualizado com sucesso", "success")
        return redirect("/funcionarios")
    
    return render_template('usuarios/editafuncionario.html', usuarios=usuarios, Formcadastrofuncionario = form, datanasc=datanasc)




'''    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('erros/404.html'), 404
    
@app.errorhandler(403)
def page_forbidden(e):
    return render_template('erros/403.html'), 403
    
@app.errorhandler(410)
def Internal_Server_Error(e):
    return render_template('erros/410.html'), 410
    
@app.errorhandler(500)
def Internal_Server_Error(e):
    return render_template('erros/500.html'), 500
    
@app.errorhandler(Exception)
def unhandled_exception(e):
    return render_template('erros/500.html'), 500
'''