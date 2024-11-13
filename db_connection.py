import mysql.connector # type: ignore
from mysql.connector import Error # type: ignore

def conectar():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='123456',  # Cambia esto por la contraseña de tu base de datos
            database='face_rec'  # Cambia esto por el nombre de tu base de datos
        )

        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")  # Depuración
            return conexion
        else:
            print("Error: No se pudo conectar a la base de datos")  # Depuración
            return None

    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
