import random
import pymysql
import operaciones


def generarCodigo(correo):
    respuesta=""
    conn = pymysql.connect(
        host="104.198.31.228", port=3306, user="lsmupiita",
        passwd="lsmupiita", db="lsmupiita"
    )

    cursor = conn.cursor()
    cursor.execute(
        "SELECT codigo FROM usuario where correo = '" + correo + "'"
    )
    results = cursor.fetchall()
    for row in results:
        respuesta = row[0]
    
    print(len(respuesta))
    if len(respuesta)!=0:
        respuesta = respuesta
    else:
        respuesta = "No existe el correo solicitado"

    conn.commit()
    conn.close()

    return respuesta


def nuevoregistro(correo):
    conn = pymysql.connect(
        host="104.198.31.228", port=3306, user="lsmupiita",
        passwd="lsmupiita", db="lsmupiita"
    )

    cursor = conn.cursor()
    cursor.execute(
        "SELECT codigo FROM usuario where correo = '" + correo + "'"
    )

    respuesta = cursor.fetchone()
    print(respuesta)
    if respuesta == None:
        cursor.execute(
            "insert into usuario values ('" + correo + "','" + operaciones.crearCodigo(correo) + "')"
        )
        respuesta = "Registro exitoso"
    else:
        respuesta = "El correo ya existe"

    conn.commit()
    conn.close()

    return respuesta
