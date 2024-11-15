from db_connection import conectar
from mysql.connector import Error # type: ignore
import os
import face_recognition # type: ignore

def registrar_usuario(nombre, apellido, usuario, contrasena, img_ruta):
    if not usuario or not contrasena:
        raise ValueError("Usuario y contraseña no pueden estar vacíos")

    if not os.path.exists(img_ruta):
        raise ValueError("La imagen no se encuentra en la ruta especificada")

    conexion = conectar()
    if conexion:
        try:
            # Leer la imagen para almacenar en la base de datos
            with open(img_ruta, 'rb') as f:
                imagen_blob = f.read()

            cursor = conexion.cursor()
            query = "INSERT INTO usuarios (nombre, apellido, usuario, contrasena, imagen) VALUES (%s, %s, %s, %s, %s)"
            valores = (nombre, apellido, usuario, contrasena, imagen_blob)
            cursor.execute(query, valores)
            
            # Confirmar la transacción
            conexion.commit()

            print(f"Usuario '{usuario}' registrado exitosamente.")

        except Error as e:
            print(f"No se pudo registrar el usuario: {e}")
            raise e
        finally:
            cursor.close()
            conexion.close()

def validar_credenciales(usuario, contrasena, img_ruta_captura):
    if not usuario or not contrasena:
        raise ValueError("Usuario y contraseña no pueden estar vacíos.")

    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "SELECT nombre, apellido, imagen FROM usuarios WHERE usuario = %s AND contrasena = %s"
            valores = (usuario, contrasena)
            cursor.execute(query, valores)
            resultado = cursor.fetchone()

            if resultado is None:
                raise ValueError("Usuario o contraseña incorrectos.")

            # Asignar los valores devueltos por la consulta
            nombre, apellido, imagen_blob = resultado

            # Guardar la imagen registrada temporalmente para comparación
            img_ruta_db = 'temp_registrada.jpg'
            with open(img_ruta_db, 'wb') as img_file:
                img_file.write(imagen_blob)

            # Comparar las imágenes con face_recognition
            imagen_registrada = face_recognition.load_image_file(img_ruta_db)
            imagen_capturada = face_recognition.load_image_file(img_ruta_captura)

            # Verificar si hay encodings en ambas imágenes
            encoding_registrada = face_recognition.face_encodings(imagen_registrada)
            encoding_capturada = face_recognition.face_encodings(imagen_capturada)

            if not encoding_registrada or not encoding_capturada:
                raise ValueError("Error: No se detectó un rostro en una de las imágenes.")

            # Realizar la comparación
            resultados = face_recognition.compare_faces([encoding_registrada[0]], encoding_capturada[0])

            if not resultados[0]:
                raise ValueError("El rostro no coincide con el usuario registrado.")

            return nombre, apellido

        except Error as e:
            raise Exception(f"Error al validar las credenciales: {e}")
        finally:
            cursor.close()
            conexion.close()
            # Eliminar las imágenes temporales
            if os.path.exists(img_ruta_db):
                os.remove(img_ruta_db)
