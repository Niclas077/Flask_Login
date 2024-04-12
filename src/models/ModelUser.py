from .entities.User import User

class ModelUser():
    
    @classmethod
    def login(self,db,user): #el metodo login recibe el db que es la conexion a la base de datos y el user que es el usuario a logear
        try:
            cursor=db.connection.cursor()
            sql="""SELECT id, username, password, rol FROM USUARIOS 
            WHERE username= '{}'""".format(user.username) #valida que el usuario exista en la base de datos 
            cursor.execute(sql)
            row=cursor.fetchone() #guarda el dato de la consulta en la variable row
            if row != None:
                 user=User(row['id'], row['username'], User.check_password(row['password'], user.password), row['rol'])
                 return user
                #en el campo de la contraseña que refiere a row[password] se valida un booleano para saber si la contraseña es valida o no, despues de ir al 
                #metodo que genera el hash para la contraseña
                #cada posicion en la variable row hace referencia a cada columna de mi tabla: id, username, etc
            else:
                return None    
        except Exception as ex:
            raise Exception(ex)
    
    
    
    @classmethod
    def get_id(self,db,id): #el metodo get_id recibe el db que es la conexion a la base de datos y el id del usuario que se va a cargar para poder logear
        try:
            cursor=db.connection.cursor()
            sql='SELECT id, username FROM USUARIOS WHERE id={}'.format(id)
            cursor.execute(sql)
            row=cursor.fetchone() #guarda el dato de la consulta en la variable row
            if row != None:
                 return User(row['id'], row['username'], None, None)
            else:
                return None    
        except Exception as ex:
            raise Exception(ex)
        
        
        
    @classmethod
    def registroU(self,db,user):
        try:
            cursor = db.connection.cursor()
            sql = "INSERT INTO USUARIOS (username, password, rol) VALUES (%s, %s, %s)"
            cursor.execute(sql, (user.username, User.hash_password_generate(user.password), user.rol))
            db.connection.commit()
            row=cursor.fetchone()
            cursor.close()
            return True
                
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def registroUA(self,db,user):
        try:
            cursor = db.connection.cursor()
            sql = "INSERT INTO USUARIOS (id,username, password, rol) VALUES (%s,%s, %s, %s)"
            cursor.execute(sql, (user.id,user.username, User.hash_password_generate(user.password), user.rol))
            db.connection.commit()
            row=cursor.fetchone()
            cursor.close()
            return True
                
        except Exception as ex:
            raise Exception(ex)    
        
        
    @classmethod
    def eliminarU(self,db,user):
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT ID FROM USUARIOS WHERE ID=%s",(user.id,))
            id=cursor.fetchone()
            if id:
                cursor.execute("DELETE FROM USUARIOS WHERE ID=%s",(user.id,)) #Se pone una coma para especificar que se pasa el parametro como una tupla
                db.connection.commit()
                cursor.close()
                return True
            else:
                return False
            
        except Exception as ex:
            raise Exception(ex)          
        
        
    @classmethod
    def rectpassword(self,db,user):
        try:
            cursor=db.connection.cursor()
            cursor.execute("SELECT USERNAME, PASSWORD FROM USUARIOS WHERE USERNAME=%s",(user.username,))
            usuario=cursor.fetchone() #Guarda los datos de la consulta para ser verificados en el if 
            if usuario: #Si el usuario existe
                cursor.execute("UPDATE USUARIOS SET PASSWORD=%s WHERE USERNAME=%s",(User.hash_password_generate(user.password),user.username))
                db.connection.commit()
                cursor.close()
                return True
            else:
                return False
        except Exception as ex:
            raise Exception(ex)
    
    
    @classmethod
    def mostrarU(self,db):
        try:
            cursor=db.connection.cursor()
            cursor.execute("SELECT *FROM USUARIOS")
            usuarios = cursor.fetchall()
            cursor.close()
            return usuarios
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def actualizar(self,db,user):
        try:
            cursor=db.connection.cursor()
            cursor.execute("UPDATE USUARIOS SET USERNAME=%s,PASSWORD=%s,ROL=%s WHERE ID=%s", (user.username,User.hash_password_generate(user.password),user.rol,user.id))
            db.connection.commit()
            cursor.close()
            return True
        except Exception as ex:
            raise Exception(ex)
    
    