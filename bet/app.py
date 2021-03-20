#! usr\bin\env python
# _*_ coding: utf-8 _*_
#Author Luis Hermoso
# GP System C.A.
#fecha 07/01/2021 11:07 PM



from flask import Flask, escape, request, render_template, url_for, redirect, flash, session, jsonify
import flask_wtf as wtf
from flask_sqlalchemy import SQLAlchemy
import bd
import sqlite3
import flask_socketio as soc
import json as j
import time
from gevent import monkey

monkey.patch_all()

app = Flask(__name__)
app.secret_key="secretoenlamontana"
app.config.update(SESSION_COOKIE_SAMESITE="lax")
socket = soc.SocketIO(app)

fallas = {'nolog':'Usuario no esta Logueado', 'noacces':'Usuario sin acceso a esta area'}

@app.before_request
def session_manager():
    session.permanent = True


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

        session.clear()
        session['name'] = nombre
        session['auth'] = 0
        
        if nombre =="" or password =="":
            flash("No hay datos")
            return render_template('login.html')
        else:
            datos = (nombre, password)
            try:
                if bd.existe(datos):
                    plantilla = bd.leertodo()
                    if nombre== str(plantilla[0][1]) and password == str(plantilla[0][3]):
                        session['auth'] = 1
                        flash('Bienvenido')
                        return redirect(url_for('layad', user=nombre))
                    else:
                        session['auth'] = 1
                        #flash("te haz logeado correctamente")
                        bd.log(str(nombre))
                        flash('Bienvenido')
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
    plantilla = bd.leertodo()
    if user == plantilla[0][1]:
        return render_template('fail.html', error=fallas['noacces'])
    else:
        if session['auth'] == 1 and session['name'] == user:
            #enrutado a dashboard
            #flash('Bienvenido')

            return render_template('dashboard.html', user=user)
        else:
            return render_template('fail.html', error = fallas['nolog'])


@app.route('/recargas/<user>', methods=['GET', 'POST'])
@app.route('/recargas', methods=['GET', 'POST'])
def rec(user):
    if session['auth'] == 1 and  session['name'] == user:
        return render_template('recargas.html', user=user)
    else:
        return render_template('fail.html', error=fallas['nolog'])



@app.route('/documentacion', methods=['GET', 'POST'])
def doc():
    return render_template('documentacion.html')



@app.route('/dashboard1/<user>', methods=['GET', 'POST'])
def layad(user):
    cuenta = bd.counteo()
    plantilla = bd.leertodo()
    if user != plantilla[0][1]:
        return render_template('fail.html', error=fallas['noacces'])
    else:
        if session['auth'] == 1 and session['name'] == str(plantilla[0][1]):
            #flash('Bienvvenido')

            return render_template('dashboard1.html', user=user, plantilla=plantilla, cuenta=cuenta)
        else:
            return render_template('fail.html', error=fallas['noacces'])



@app.route('/logout')
def logout():
    print(session['name'])
    bd.logout(session['name'])
    session.clear()
    session['name'] = 'unknown'
    session['auth'] = 0
    cuenta = bd.counteo()
    return redirect(url_for('hello'))


@app.route('/fail')
def fail(fail):
    return render_template('fail.html', error=fail)



@socket.on('message')#inicio la escucha
def sockete(msg): #funcion recibe el dato que sera el mensaje
    time.sleep(2)
    if msg== 'hola server':
        cuenta = bd.counteo()
        plantilla = bd.leertodo()
        plantilla.append(cuenta)
        plantilla = tuple(plantilla)
        socket.send('hola cliente') #envio respuesta
        cuenta = j.dumps(plantilla) #convierto a json
        #print(cuenta)
        socket.send(cuenta) #envio


@socket.on_error_default
def error(e):
    print("este es el error: " + str(e))


if __name__ == '__main__':
    socket.run(app, host='0.0.0.0', debug=1)
