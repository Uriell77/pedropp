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



def editar(idu, datos):
    print(datos[1])
    cursor.execute('''UPDATE usuarios SET (nombre,
    correo,
    password,
    log,
    status,
    saldo) = ({0},
    {1},
    {2},
    {3},
    {4},
    {5}) WHERE id = {7}''',(datos[1],
                datos[2],
                datos[3],
                datos[4],
                datos[5],
                datos[6],idu))
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

def log(dato):
    #parametro dato es el nombre
    datos = leer(dato)
    datos = list(datos)
    #print(datos)
    datos[4] = 'Conectado'
    #print(datos)
    datos = tuple(datos)
    print(datos)
    print(datos[0])
    editar(datos[0], datos)
    return True


def logout(dato):
    #parametro dato es el nombre
    datos = leer(dato)
    datos = list(datos)
    #print(datos)
    datos[4] = 'Desconectado'
    #print(datos)
    datos = tuple(datos)
    #print(datos)
    editar(datos[0], datos)
    return True
    
    
def counteo():
    plantilla = leertodo()[1:]
    cusuarios = len(plantilla)
    cconect = [i for i in plantilla if i[4]=='Conectado']
    cdesconect = cusuarios - (len(cconect))
    cactiv = [i for i in plantilla if i[5] =='Activo']
    cinactiv = cusuarios - (len(cactiv))
    aldia = [i for i in plantilla if i[6]>= 0.0]
    morosos = [i for i in plantilla if i[6]< 0.0]

    res =  (cusuarios, len(cconect), cdesconect, len(cactiv), cinactiv, len(aldia), len(morosos))
    return res


