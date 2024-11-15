import mysql.connector # type: ignore
from mysql.connector import Error # type: ignore

def conectar():
    try:
        conexion = mysql.connector.connect(
            host='visiontech-mysql.mysql.database.azure.com',
            port=3306,
            user='admin_db',
            password='Vision2024$',  # Cambia esto por la contraseña de tu base de datos en Azure
            database='face_rec',  # Cambia esto por el nombre de tu base de datos
            ssl_ca='DigiCertGlobalRootCA.crt.pem'  # Archivo SSL necesario para la conexión segura
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
