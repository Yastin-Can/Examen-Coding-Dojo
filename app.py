# app.py
from flask import Flask, render_template, session, request, redirect, url_for
from models.user import User
from models.note import Note
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

@app.route('/login-register')
def cuenta():
    return render_template('login-register.html')

@app.route('/register', methods=['POST'])
def register():
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    email = request.form["email"]
    password = request.form["pswd"]
    password2 = request.form["pswd2"]

    errors = []
    if not nombre or len(nombre) < 3:
        errors.append("Nombre inválido")
    if not apellido or len(apellido) < 3:
        errors.append("Apellido inválido")
    if not email or len(email) < 3:
        errors.append("Email inválido")
    if password != password2:
        errors.append("Las contraseñas no coinciden")
    if len(password) < 6:  # Puedes ajustar la longitud mínima de la contraseña
        errors.append("La contraseña debe tener al menos 6 caracteres")

    existing_user = User.get_by_email(email)
    if existing_user:
        errors.append("El usuario ya está registrado")

    if errors:
        return render_template("login-register.html", register_errors=errors)

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    User.insert_one(nombre, apellido, email, hashed_password)

    return redirect(url_for('main'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['pswd']
    user = User.get_by_email(email)

    if not user or not bcrypt.check_password_hash(user.password, password):
        return render_template("login-register.html", login_errors=["Email o contraseña incorrectos"])

    session['id'] = user.id
    session['nombre'] = user.nombre

    return redirect(url_for('main'))

@app.route('/')
def main():
    if 'id' in session:
        notes = Note.get_by_user_id(session['id'])
    else:
        notes = Note.get_all()

    return render_template('main.html', notes=notes)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(debug=True)
