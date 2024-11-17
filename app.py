from flask import Flask, render_template, request, redirect, url_for, flash, session # type: ignore
from auth_logic import registrar_usuario, validar_credenciales
import os
import base64

app = Flask(__name__)
app.secret_key = "supersecretkey"

@app.route('/')
def home():
    success = session.pop('success', None)
    return render_template('register_login.html', success=success)

@app.route('/registro', methods=['POST'])
def registro():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    contrasena = request.form['contrasena']
    usuario = f"{nombre[0].upper()}{apellido.split()[0].capitalize()}"
    imagen_data = request.form['imagen']

    if not nombre or not apellido or not contrasena or not imagen_data:
        flash("Todos los campos son obligatorios")
        return redirect(url_for('home'))

    img_ruta = f'img_registradas/{usuario}.jpg'

    # Guardar la imagen base64 en un archivo
    try:
        with open(img_ruta, 'wb') as img_file:
            import base64
            img_file.write(base64.b64decode(imagen_data.split(',')[1]))
    except Exception as e:
        flash(f"Error al guardar la imagen: {e}")
        return redirect(url_for('home'))

    try:
        registrar_usuario(nombre, apellido, usuario, contrasena, img_ruta)
        flash(f"Registro completado exitosamente para {nombre} {apellido}")
    except Exception as e:
        flash(f"Error al registrar el usuario: {e}")
    return redirect(url_for('home'))

# Ruta para iniciar sesión
@app.route('/login', methods=['POST'])
def login():
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']
    imagen_data = request.form['imagen']

    if not usuario or not contrasena or not imagen_data:
        flash("Por favor, completa todos los campos requeridos.")
        return redirect(url_for('home'))

    img_ruta_captura = 'temp_captura.jpg'

    try:
        # Guardar la imagen capturada para la comparación
        with open(img_ruta_captura, 'wb') as img_file:
            img_file.write(base64.b64decode(imagen_data.split(',')[1]))

        # Validar credenciales e imagen
        nombre, apellido = validar_credenciales(usuario, contrasena, img_ruta_captura)
        flash(f"Inicio de sesión exitoso. Bienvenido {nombre} {apellido}")
        session['success'] = True
        session['nombre'] = nombre
        session['apellido'] = apellido
        return redirect(url_for('menu_principal'))

    except ValueError as ve:
        flash(str(ve))
    except Exception as e:
        flash(f"Error al iniciar sesión: {e}")
    finally:
        # Eliminar la imagen temporal después de la comparación
        if os.path.exists(img_ruta_captura):
            os.remove(img_ruta_captura)

    return redirect(url_for('home'))

@app.route('/menu')
def menu_principal():
    nombre = session.get('nombre')
    apellido = session.get('apellido')
    if not nombre or not apellido:
        return redirect(url_for('home'))
    return render_template('menuPrincipal.html', nombre=nombre, apellido=apellido)

if __name__ == "__main__":
    app.run(debug=True)
