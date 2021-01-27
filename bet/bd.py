import sqlite3


base = sqlite3.connect('user.db', check_same_thread=False)

cursor = base.cursor()



def crear(datos):
    #ingresa un usuario a la bd parametro datos es tupla en el orden de campos en bd`
    cursor.execute("INSERT INTO usuarios(nombre, correo, password) VALUES ('{0}', '{1}', '{2}')".format(datos[0], datos[1], datos[2]))
    base.commit()


def leer(dato):
    #busca registro por nombre o id 
    cursor.execute("SELECT * FROM usuarios WHERE id = ? OR nombre = ?", (dato, dato))
    respuesta = cursor.fetchone()
    return respuesta


def leertodo():
    #returna toda la bd
    cursor.execute("SELECT * FROM usuarios")
    respuesta = cursor.fetchall()
    return respuesta



def editar(id, datos):
    cursor.execute("UPDATE usuarios SET (nombre, correo, password) = (?,?,?) WHERE id = ?",(datos[0],datos[1],datos[2], id))
    base.commit()


def borrar(id):
    cursor.execute("DELETE FROM usuarios WHERE id = ?",(id))
    base.commit()


def existe(datos):
    cursor.execute("SELECT * FROM usuarios WHERE (nombre = ? OR correo = ?) AND password = ?", (datos[0], datos[0], datos[1]))
    if cursor.fetchall():
        return True
    else:
        return False


