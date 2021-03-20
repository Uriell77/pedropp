import mysql.connector as mycon
from mysql.connector import Error


try:
    connection = mycon.connect(host='localhost', database='user', user='root', password='')


    if connection.is_connected():
        print('conectado')
        cursor = connection.cursor()


        def crear(datos):
            'Ingresa un usuario a la bd parametro datos es una tupla en el orden de campos en bd'
            cursor.execute("INSERT INTO usuarios (nombre, correo, password) VALUES ('{0}', '{1}', '{2}')".format(datos[0], datos[1], datos[2]))
            connection.commit()
            print('registro correcto')
            cursor.close()

except Error as e:
    print('no se pudo conectar a la base de datos')


'''
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print('la conexion esta cerrada')

'''
