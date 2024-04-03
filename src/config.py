class Config:
    SECRET_KEY ='eu2j4ifi3%&sj!dghVs' #maneja datos de sesion y envio de mensajes con flash



class DevelopmentConfig(Config): #debe ser heredada de la clase Config
    DEBUG=True; #Activa la depuracion automatica de nuestro proyecto, necesario que debug edte escrito en mayuscula
    MYSQL_HOST='localhost'
    MYSQL_USER='root'
    MYSQL_PASSWORD='2304'
    MYSQL_DB='login_flask'
    MYSQL_CURSORCLASS='DictCursor'
    
#Diccionario de datos    
config = { 
    'development' : DevelopmentConfig
}