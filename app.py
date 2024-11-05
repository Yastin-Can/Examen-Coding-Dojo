from flask import Flask, render_template, session, request, redirect, url_for
from models.user import User
from models.note import Note
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.secret_key = os.urandom(24) 
bcrypt = Bcrypt(app)

@app.route('/')
def main():
    notes = Note.get_all()
    return render_template('main.html', notas=notes)

@app.route('/addNote', methods=['GET', 'POST'])
def add_note():
    if 'id' not in session:
        return redirect(url_for('login_register'))
    
    if request.method == 'POST':
        contenido = request.form['contenido']
        Note.insert_one(contenido, session['id'])
        return redirect(url_for('main'))
    
    return render_template('addNote.html')

@app.route('/editNote/<int:note_id>', methods=['GET', 'POST'])
def editNote(note_id):
    if 'id' not in session:
        return redirect(url_for('login_register'))

    nota = Note.get_by_id(note_id)

    if not nota or nota['user_id'] != session['id']:
        return redirect(url_for('main'))

    if request.method == 'POST':
        nuevo_contenido = request.form['contenido']
        Note.update_one(note_id, nuevo_contenido)
        return redirect(url_for('main'))

    return render_template('editNote.html', nota=nota)


@app.route('/deleteNote/<int:note_id>', methods=['GET', 'POST'])
def deleteNote(note_id):
    if 'id' not in session:
        return redirect(url_for('login_register'))
    
    note = Note.get_by_id(note_id)
    if note and note['user_id'] == session['id']:
        Note.delete_one(note_id)
    
    return redirect(url_for('main'))



@app.route('/loginRegister')
def login_register():
    return render_template('loginRegister.html',  login_errors=[], register_errors=[])

@app.route('/register', methods=['POST'])
def register():
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    email = request.form["email"]
    password = request.form["password"]
    password2 = request.form["confirm_password"]

    errors = []

    if not nombre or len(nombre) < 3:
        errors.append("Nombre inválido")

    if not apellido or len(apellido) < 3:
        errors.append("Apellido inválido")

    if not email or len(email) < 3:
        errors.append("Email inválido")

    if password != password2:
        errors.append("Las contraseñas no coinciden")

    if len(password) < 6:  
        errors.append("La contraseña debe tener al menos 6 caracteres")


    existing_user = User.get_by_email(email)
    if existing_user:
        errors.append("El usuario ya está registrado")

    if errors:
        return render_template("loginRegister.html", register_errors=errors, login_errors=[])

    session['nombre'] = nombre
    session['apellido'] = apellido
    session['email'] = email
    
    password = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User.insert_one(nombre, apellido, email, password)
    users = User.get_by_email(email)
    
    session['id'] = users.id

    return redirect(url_for('main', user = user))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = User.get_by_email(email)

    if not user or not bcrypt.check_password_hash(user.password, password):
        return render_template("loginRegister.html", login_errors=["Email o contraseña incorrectos"], register_errors = [])

    session['id'] = user.id
    session['nombre'] = user.nombre

    return redirect(url_for('main'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(debug=True)
