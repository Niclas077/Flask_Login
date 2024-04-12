from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id,username,password,rol) -> None:
        self.id= id
        self.username= username
        self.password= password
        self.rol= rol
    #Esta clase es un reflejo de la tabla de usuarios de mi base de datos
    #Mediante esta clase se podran manipular las entidades de tipo usuario y realizar una autenticacion
    @classmethod
    def check_password(self,hashed_password,password): #Metodo que verifica el password junto a su respectivo hash
        return check_password_hash(hashed_password,password)
    
    @staticmethod 
    def hash_password_generate(password):
        return generate_password_hash(password)
    
    
    
