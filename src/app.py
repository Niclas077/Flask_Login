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

#Alerts.js

#from .static.js import NotificacionSawlf

app=Flask(__name__, template_folder='template',static_folder='static')

db=MySQL(app) #establece la conexion con la base de datos mediante la implementacion de un cursor
login_manager_app=LoginManager(app)

@login_manager_app.user_loader #Metodo que carga al usuario
def load_user(id):
    return ModelUser.get_id(db,id)
    


@app.route('/')
def index():
    return redirect(url_for('login')) #cuando se acceda a la ruta raiz esta se va a redirigir al metodo login


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user=User(0,request.form['txtemail'], request.form['txtpassword'],0) #Instancia del usuario que se va a logear
        logged_user=ModelUser.login(db,user)#Proceso de Login para validar los datos en la DB
        if logged_user != None:
            if logged_user.password: # Si es True, si la contraseña es correcta
                login_user(logged_user) #crea la instancia para logear al usuario verificado
                if logged_user.rol == 1:
                   return redirect(url_for("home"))
                elif logged_user.rol == 2:
                    return redirect(url_for("HUsuario"))
            else:
                flash("Contraseña Incorrecta")
        else:
            flash("El usuario no existe...")      
        return render_template('./auth/login.html')
    else: #Metodo GET que representa el primer acceso a la vista
        return render_template('./auth/login.html')



@app.route('/crearUsuario', methods=['GET','POST'])
def crearusuario():
    if request.method=='POST':
        user=User(None,request.form['txtusuario'],request.form['txtcontraseña'],'2')
        createUser=ModelUser.registroU(db,user)
        if createUser != None:
            flash(f"Usuario Registrado exitosamente!, Bienvenmido {request.form['txtusuario']} ")
            return redirect(url_for('login'))
        else:
            return redirect(url_for('registro'))
  
  
@app.route('/restaurarP', methods=['GET','POST'] ) 
def restaurarP():
    if request.method == 'POST':
        user=User(None,request.form['txtusuario'],request.form['txtcontraseña'],None)
        restart=ModelUser.rectpassword(db,user)
        if restart == True:
            flash("Contraseña actualizada con exito")
            return redirect(url_for('login')) 
        else:
            flash("El usuario ingresado no coincide con los registros en la base de datos")
            return redirect(url_for('recuperar')) 
            
        
        
        
@app.route('/updateUser', methods=['GET','POST'])
def updateUser():
     if request.method == 'POST':
         id=request.form['txtid']
         user=User(request.form['txtid'],request.form['txtusuario'],request.form['txtcontraseña'],request.form['txtrol'])
         update=ModelUser.actualizar(db,user)
         if update == True:
             return redirect(url_for('AdminU',success_message=True,id=id))
         else:
             return redirect(url_for('AdminU',success_message=False,id=id))
             
@app.route('/addUser', methods=['GET','POST'])
def addUser():
    if request.method=='POST':
        user=User(request.form['txtid'],request.form['txtusuario'],request.form['txtcontraseña'],request.form['txtrol'])
        createUser= ModelUser.registroUA(db,user) 
        if createUser == True:
            return redirect(url_for('AdminU'))
        else:
            flash("El usuario no ha podido ser añadido")
            return redirect(url_for('Añadir'))
           
@app.route('/deleteUser', methods=['GET','POST'])
def deleteUser():
    if request.method == 'POST':
        user = User(request.form['txtid'],0,0,0)
        id=request.form['txtid']
        deleteUser=ModelUser.eliminarU(db,user)
        if deleteUser == True:
          return redirect(url_for('AdminU'))
        else:
            flash("El usuario no se ha podido eliminar")
            return redirect(url_for('ElimU',id=id))
    
 
   
@app.route('/AdminU')
@login_required
def AdminU():
    success_message = request.args.get('success_message')
    id= request.args.get('id')
    usuarios = ModelUser.mostrarU(db)
    return render_template('./administradores/AdministrarU.html',usuarios=usuarios,success_message=success_message, id=id)   
       

@app.route('/ElimU/<int:id>')
@login_required  
def ElimU(id):
    return render_template('./administradores/EliminarU.html',id=id)
  
@app.route('/ActU/<int:id>')
@login_required
def ActU(id):
    return render_template('./administradores/ActualizarU.html',id=id)
    
    
@app.route('/Añadir') 
def Añadir():
    return render_template('./administradores/AñadirU.html')        
  
@app.route('/recuperar') 
def recuperar():
    return render_template('./auth/rectpass.html')   


#Vistas del usuario
@app.route('/HUsuario')
@login_required
def HUsuario():
    return render_template('./usuarios/index.html')

@app.route('/about')
@login_required
def about():
    return render_template('./usuarios/about.html')

@app.route('/contact')
@login_required
def contact():
    return render_template('./usuarios/contact.html')


@app.route('/gallery')
@login_required
def gallery():
    return render_template('./usuarios/gallery.html')


@app.route('/service')
@login_required
def services():
    return render_template('./usuarios/service.html')


@app.route('/testimonial')
@login_required
def testimonial():
    return render_template('./usuarios/testimonial.html')


@app.route('/registro')
def registro():
    return render_template('./Rest/registro.html')


@app.route('/logout') #Metodo para cerrar la sesion con flask
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
@login_required #Vista Protegida solo para usuarios autenticados
def home():
    return render_template('./administradores/home.html')

if __name__ == "__main__":
    app.config.from_object(config['development']) #establece la configuracion a partir de un objeto, el ob ubicado en el archivo config.py
    app.run()
    
