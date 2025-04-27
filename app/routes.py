from flask import render_template, request, redirect, url_for, session, flash
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from app import app, mysql, mail


def generar_token(correo):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(correo, salt='recuperar-contrasena')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        contrasena = request.form["contrasena"]

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuario WHERE u_correo = %s", (correo,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[5], contrasena):
            session["usuario_id"] = user[0]  # id_usuario
            session["correo"] = user[4]      # u_correo
            session["rol"] = user[6]          # rol
            flash("¡Bienvenido!", "success")
            return redirect(url_for("index"))  # Cambiar luego a tu dashboard real
        else:
            flash("Correo o contraseña incorrectos", "danger")
            return render_template("login.html")

    return render_template("login.html")







@app.route("/recuperar", methods=["GET", "POST"])
def recuperar():
    if request.method == "POST":
        correo = request.form["correo"]

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuario WHERE u_correo = %s", (correo,))
        user = cur.fetchone()
        cur.close()

        if user:
            # 1. Generar token seguro
            token = generar_token(correo)

            # 2. Crear enlace de recuperación
            link = url_for('resetear', token=token, _external=True)

            # 3. Crear mensaje de correo
            mensaje = Message(
                subject='Recuperación de Contraseña - Andamios Colosio',
                sender=app.config['MAIL_USERNAME'],
                recipients=[correo]
            )

            # 4. Contenido HTML del correo
            mensaje.html = f'''
            <div style="text-align: center; font-family: Arial, sans-serif; padding: 20px;">
                <img src="app/static/img/logo.png" alt="Logo Empresa" style="width: 150px; margin-bottom: 20px;">
                <h2 style="color: #333;">Recuperación de Contraseña</h2>
                <p style="font-size: 16px; color: #555;">Recibimos una solicitud para restablecer tu contraseña.</p>
                <a href="{link}" style="display: inline-block; padding: 10px 20px; margin-top: 20px; background-color: #d9534f; color: white; text-decoration: none; border-radius: 5px; font-size: 16px;">Restablecer Contraseña</a>
                <p style="font-size: 14px; color: #999; margin-top: 30px;">Si no realizaste esta solicitud, puedes ignorar este correo.</p>
            </div>
            '''

            # 5. Enviar correo
            mail.send(mensaje)

            flash("Te enviamos un correo con instrucciones para recuperar tu contraseña.", "success")
            return redirect(url_for('login'))
        else:
            flash("El correo ingresado no existe.", "danger")
            return render_template("recuperar/recuperar.html")

    return render_template("recuperar/recuperar.html")








@app.route("/resetear/<token>", methods=["GET", "POST"])
def resetear(token):
    try:
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        correo = serializer.loads(token, salt='recuperar-contrasena', max_age=3600)  # Token válido 1 hora
    except (SignatureExpired, BadSignature):
        flash("El enlace ya expiró o no es válido.", "danger")
        return redirect(url_for('login'))

    if request.method == "POST":
        nueva_contrasena = request.form["nueva_contrasena"]
        confirmar_contrasena = request.form["confirmar_contrasena"]

        if nueva_contrasena != confirmar_contrasena:
            flash("Las contraseñas no coinciden.", "danger")
            return render_template("recuperar/resetear.html")

        hash_contrasena = generate_password_hash(nueva_contrasena)

        cur = mysql.connection.cursor()
        cur.execute("UPDATE usuario SET u_contrasena = %s WHERE u_correo = %s", (hash_contrasena, correo))
        mysql.connection.commit()
        cur.close()

        flash("¡Contraseña actualizada exitosamente!", "success")
        return redirect(url_for('login'))

    return render_template("recuperar/resetear.html")







@app.route("/nueva_contrasena", methods=["GET", "POST"])
def nueva_contrasena():
    if "recuperar_correo" not in session:
        flash("Acceso no autorizado.", "danger")
        return redirect(url_for("login"))

    if request.method == "POST":
        nueva_contrasena = request.form["nueva_contrasena"]
        confirmar_contrasena = request.form["confirmar_contrasena"]

        if nueva_contrasena != confirmar_contrasena:
            flash("Las contraseñas no coinciden.", "danger")
            return render_template("recuperar/nueva_contrasena.html")

        hash_contrasena = generate_password_hash(nueva_contrasena)

        cur = mysql.connection.cursor()
        cur.execute("UPDATE usuario SET u_contrasena = %s WHERE u_correo = %s", (hash_contrasena, session["recuperar_correo"]))
        mysql.connection.commit()
        cur.close()

        session.pop("recuperar_correo", None)
        flash("¡Contraseña actualizada exitosamente!", "success")
        return redirect(url_for("login"))

    return render_template("recuperar/nueva_contrasena.html")





#pendiente de terminar
@app.route("/nueva-renta")
def nueva_renta():
    return render_template("rentas/nueva_renta.html")







@app.route("/")
def index():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")


