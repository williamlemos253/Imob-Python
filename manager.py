# -*- coding: utf-8 -*-
from flask import Flask
from werkzeug.serving import run_simple
from imobiliaria.app import app, manager
from flask_script import Manager





if __name__ == '__main__':
    manager.run()