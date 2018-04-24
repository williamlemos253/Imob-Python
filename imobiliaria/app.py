# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_material import Material 
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail
from flask_script import Manager
from flask_user import login_required, SQLAlchemyAdapter
from flask_user import roles_required




import sys
reload(sys)
sys.setdefaultencoding('utf-8')


mail = Mail()


app = Flask(__name__)

app.debug = True
Material(app) 


#chama o arquivo com as configs dos plugins
app.config.from_pyfile('../config.cfg')

#conf do csrf do wtforms
csrf = CSRFProtect(app)
csrf.init_app(app)

#e-mail
mail.init_app(app)

db = SQLAlchemy(app)




migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)



import views
import admin
import userviews