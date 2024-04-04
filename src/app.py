from flask import Flask, render_template, url_for, request, redirect, flash
from config import config #importamos el diccionario de nuestro archivo de configuracion inicial
from flask_mysqldb import MySQL
from flask_login import LoginManager,login_user,logout_user,login_required
#login_required controla laas vistas a las que el usuario ingresa solo si esta logeado
from flask_wtf.csrf import CSRFProtect

#Modelos

from models.ModelUser import ModelUser

#Entidades

from models.entities.User import User

app=Flask(__name__, template_folder='template',static_folder='static')

db=MySQL(app) #establece la conexion con la base de datos mediante la implementacion de un cursor
csrf=CSRFProtect() #variable que guarda el objeto CSRFProtect para generar el token de autenticacion al inicial
login_manager_app=LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_id(db,id)
    


@app.route('/')
def index():
    return redirect(url_for('login')) #cuando se acceda a la ruta raiz esta se va a redirigir al metodo login


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user=User(0,request.form['txtemail'], request.form['txtpassword'],0)
        logged_user=ModelUser.login(db,user)#Proceso de Login para validar los datos en la DB
        if logged_user != None:
            if logged_user.password: # Si es True, si la contraseña es correcta
                login_user(logged_user) #crea la instancia para logear al usuario verificado
                return redirect(url_for('home'))
            else:
                flash("Contraseña Incorrecta")
        else:
            flash("El usuario no existe...")      
        return render_template('./auth/login.html')
    else: #Metodo GET que representa el primer acceso a la vista
        return render_template('./auth/login.html')



@app.route('/logout') #Metodo para cerrar la sesion con flask
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
@login_required #Vista Protegida solo para usuarios autenticados
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.config.from_object(config['development']) #establece la configuracion a partir de un objeto, el ob ubicado en el archivo config.py
    csrf.init_app(app) #genera un token al iniciar mi aplicacion
    app.run()
    
