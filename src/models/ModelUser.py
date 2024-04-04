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
                #en el campo de la contraseña que refiere a row[2] se valida un booleano para saber si la contraseña es valida o no, despues de ir al 
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