from flask import Flask
from flask_mysqldb import MySQL
from flask_cors import CORS
from flask_mail import Mail  # <- Aquí ya lo importaste

app = Flask(__name__)
app.config.from_object('config.Config')

CORS(app)
mysql = MySQL(app)

mail = Mail(app)  # <- ESTA LÍNEA NUEVA inicializa Flask-Mail

from app import routes
