# -*- coding: utf-8 -*-
from flask import Flask
from werkzeug.serving import run_simple
from imobiliaria.app import app




if __name__ == '__main__':
    run_simple('0.0.0.0', 8080, app,
               use_reloader=True, use_debugger=True, use_evalex=True)