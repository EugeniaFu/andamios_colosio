import os

class Config:

    SECRET_KEY = 'clave_secreta' # tu clave secreta normal


    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '123456'  # Cambia aquí tu contraseña real
    MYSQL_DB = 'sistemarentas'
    SECRET_KEY = os.urandom(24)

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'alejandralopeez2003@gmail.com'    # Tu correo Gmail
    MAIL_PASSWORD = 'wyaj cxff hedi kvhy'   # Contraseña o contraseña de aplicación
