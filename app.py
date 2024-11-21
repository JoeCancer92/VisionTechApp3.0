from binascii import Error
from db_connection import conectar
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify  # type: ignore
from auth_logic import registrar_usuario, validar_credenciales
import os
import base64

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Ruta para la página principal (login y registro)
@app.route('/')
def home():
    success = session.pop('success', None)
    return render_template('register_login.html', success=success)

# Ruta para registrar un usuario
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

# Ruta para el menú principal
@app.route('/menu')
def menu_principal():
    nombre = session.get('nombre')
    apellido = session.get('apellido')
    if not nombre or not apellido:
        return redirect(url_for('home'))
    return render_template('menuPrincipal.html', nombre=nombre, apellido=apellido)

# Ruta para gestionar usuarios (carga el archivo gestionarUsuarios.html)
@app.route('/gestionar_usuarios', methods=['GET'])
def gestionar_usuarios():
    return render_template('gestionarUsuarios.html')

# Ruta para listar usuarios
@app.route('/listar_usuarios', methods=['GET'])
def listar_usuarios():
    try:
        # Conectar a la base de datos
        conexion = conectar()  
        if not conexion:
            print("Error: No se pudo conectar a la base de datos")
            return {"error": "No se pudo conectar a la base de datos"}, 500

        cursor = conexion.cursor()
        cursor.callproc('listarusuarios')  # Ejecutar el procedimiento almacenado

        # Obtener todos los resultados
        usuarios = []
        for result in cursor.stored_results():
            usuarios = result.fetchall()
        
        cursor.close()
        conexion.close()  # Asegurarse de cerrar la conexión después de usarla

        # Convertir los resultados a un formato adecuado para el DataTable
        usuarios_data = [
            {
                "id": user[0],
                "nombre": user[1],
                "apellido": user[2],
                "usuario": user[3]
            }
            for user in usuarios
        ]

        return jsonify(usuarios_data)

    except Exception as e:
        print(f"Error al listar usuarios: {e}")
        return {"error": str(e)}, 500

# Ruta para ver un usuario específico
@app.route('/ver_usuario', methods=['GET'])
def ver_usuario():
    user_id = request.args.get('id')
    
    if not user_id:
        return jsonify({"error": "Se necesita el ID del usuario"}), 400

    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.callproc('verUsuario', [int(user_id)])
        result = cursor.stored_results()
        
        usuario = None
        for r in result:
            usuario = r.fetchone()

        if usuario:
            usuario_data = {
                "id": usuario[0],
                "nombre": usuario[1],
                "apellido": usuario[2],
                "usuario": usuario[3],
                "contrasena": usuario[4]
            }
            return jsonify(usuario_data)
        else:
            return jsonify({"error": "Usuario no encontrado"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conexion.close()

# Ruta para editar un usuario
@app.route('/editar_usuario', methods=['POST'])
def editar_usuario():
    data = request.json

    if 'id' not in data or 'nombre' not in data or 'apellido' not in data or 'usuario' not in data or 'contrasena' not in data:
        return jsonify({"error": "Faltan datos para editar el usuario"}), 400

    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.callproc('editarUsuario', [
            int(data['id']), data['nombre'], data['apellido'], data['usuario'], data['contrasena']
        ])
        conexion.commit()
        return jsonify({"message": "Usuario actualizado correctamente"})

    except Exception as e:
        conexion.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conexion.close()

# Ruta para eliminar un usuario
@app.route('/eliminar_usuario', methods=['POST'])
def eliminar_usuario():
    data = request.json

    if 'id' not in data:
        return jsonify({"error": "Faltan datos para eliminar el usuario"}), 400

    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.callproc('eliminarUsuario', [int(data['id'])])
        conexion.commit()
        return jsonify({"message": "Usuario eliminado correctamente"})

    except Exception as e:
        conexion.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conexion.close()

# Ruta para cerrar sesión
@app.route('/logout', methods=['GET'])
def logout():
    # Limpiar la sesión y redirigir a la página de registro/login
    session.clear()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
