import mysql.connector # type: ignore
from mysql.connector import Error # type: ignore

#conexion a la base de datos
def conectar():
    try:
        conexion = mysql.connector.connect(
            host='appdata.mysql.database.azure.com',  # El nombre del servidor de tu base de datos en Azure
            port=3306,
            user='cloudteam',  # El usuario que has creado y utilizado para conectarte
            password='Vision2024$',  # Contraseña de tu base de datos en Azure
            database='face_rec',  # Nombre de la base de datos que acabas de crear
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
