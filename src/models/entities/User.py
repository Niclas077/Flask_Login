from werkzeug.security import check_password_hash, generate_password_hash


class User():
    def __init__(self, id,username,password,rol) -> None:
        self.id= id
        self.username= username
        self.password= password
        self.rol= rol
    #Esta clase es un reflejo de la tabla de usuarios de mi base de datos
    #Mediante esta clase se podran manipular las entidades de tipo usuario y realizar una autenticacion
    @classmethod
    def check_password(self,hashed_password,password):
        return check_password_hash(hashed_password,password)
    
    
