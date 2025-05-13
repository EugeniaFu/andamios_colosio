import os

class Config:

    SECRET_KEY = 'clave_secreta' # tu clave secreta normal


    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'luna18rz'  # Cambia aquí tu contraseña real// contraseña de quien lo corra 
    MYSQL_DB = 'SistemaRentas'
    SECRET_KEY = 'clave-segura-y-constante'  # o carga desde una variable de entorno

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'alejandralopeez2003@gmail.com'    # Tu correo Gmail
    MAIL_PASSWORD = 'wyaj cxff hedi kvhy'   # Contraseña o contraseña de aplicación
