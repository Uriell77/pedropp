#! usr\bin\env python
# _*_ coding: utf-8 _*_
#Author Luis Hermoso
# GP System C.A.
#fecha 07/01/2021 11:07 PM



from flask import Flask, escape, request, render_template, url_for, redirect, flash
import flask_wtf as wtf
from flask_sqlalchemy import SQLAlchemy
import bd
import sqlite3

app = Flask(__name__)
app.secret_key="secretoenlamontana"

@app.route('/')
def hello():
    #enrutado a pagina inicial
    return render_template('index.html')



@app.route('/layout')
def lay():
    return render_template('layout.html')


@app.route('/login', methods=['GET', 'POST'])
def log():
    #enrutado a login
    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']
        if nombre =="" or password =="":
            flash("No hay datos")
            return render_template('login.html')
        else:
            datos = (nombre, password)
            try:
                if bd.existe(datos):
                    flash("te haz logeado correctamente")
                    return redirect(url_for('dash', user=nombre))
                else:
                    flash("Datos Incorrectos")
                    return redirect(url_for('log'))
            except ValueError:
                return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/registro', methods=['GET', 'POST'])
def reg():
    #enrutado a registro
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        password = request.form['password']
        if nombre =="" or correo=="" or password =="":
            flash("No hay datos")
            return render_template('registro.html')
        else:
            datos = (nombre, correo, password)
            try:
                bd.crear(datos)
                flash("registro realizado")
                return redirect(url_for('log'))
            except ValueError:
                return render_template('registro.html')
            except sqlite3.IntegrityError:
                flash("Datos ya existen")
                return render_template('registro.html')
    else:
        return render_template('registro.html')


@app.route('/dashboard/<user>',  methods=['GET', 'POST'])
def dash(user):
    #enrutado a dashboard
    flash('Bienvenido')
    return render_template('dashboard.html', user=user)



@app.route('/recargas', methods=['GET', 'POST'])
def rec():
    return render_template('recargas.html')


@app.route('/documentacion', methods=['GET', 'POST'])
def doc():
    return render_template('documentacion.html')

