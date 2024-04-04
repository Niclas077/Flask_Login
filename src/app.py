from flask import Flask, render_template, url_for, request,redirect, flash
from config import config #importamos el diccionario de nuestro archivo de configuracion inicial
from flask_mysqldb import MySQL


#Modelos

from models.ModelUser import ModelUser

#Entidades

from models.entities.User import User

app=Flask(__name__, template_folder='template',static_folder='static')

db=MySQL(app) #establece la conexion con la base de datos mediante la implementacion de un cursor


@app.route('/')
def index():
    return redirect(url_for('login')) #cuando se acceda a la ruta raiz esta se va a redirigir al metodo login


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user=User(0,request.form['txtemail'], request.form['txtpassword'],2)
        logged_user=ModelUser.login(db,user)
        if logged_user != None:
            if logged_user.password:# Si es True, si la contraseña es correcta
                return redirect(url_for('home'))
            else:
                flash("Contraseña Incorrecta")
        else:
            flash("El usuario no existe...")      
        return render_template('./auth/login.html')
    else: #Metodo GET que representa el primer acceso a la vista
        return render_template('./auth/login.html')



@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.config.from_object(config['development']) #establece la configuracion a partir de un objeto, el ob ubicado en el archivo config.py
    app.run()
    
#asdfgdsafgkhkñljgdfasfjk
#asdfhgfdgstfghfdgsgfg