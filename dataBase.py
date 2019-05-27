import random
import pymysql
import operaciones

#Conexion a la base de datos
def abrirConexion():
    cnx = pymysql.connect(
        host="104.198.31.228", port=3306, user="lsmupiita",
        passwd="lsmupiita", db="lsmupiita"
    )
    return cnx
##############################################################
##############################################################
###############APIS FUNCIONALIDAD#############################
##############################################################
##############################################################

def comprobarExistencia(codigo):
    respuesta=""
    cnx =abrirConexion()
    cursor = cnx.cursor()
    query=("select correo from usuario where codigo = %s")
    cursor.execute(query,(codigo,))
    results = cursor.fetchall()
    for row in results:
        respuesta = row[0]
    if len(respuesta)!=0:
        respuesta = "Correcto"
    else:
        respuesta = "Incorrecto"
    cursor.close()
    cnx.commit()
    cnx.close()
    return respuesta

def generarCodigo(correo):
    respuesta=""
    cnx =abrirConexion()

    cursor = cnx.cursor()
    query=("select codigo from usuario where correo = %s")
    cursor.execute(query,correo)
    results = cursor.fetchall()
    for row in results:
        respuesta = row[0]
        
    if len(respuesta)!=0:
        respuesta = respuesta
    else:
        respuesta = "No existe el correo solicitado"
    cursor.close()
    cnx.commit()
    cnx.close()
    return respuesta


def nuevoregistro(correo):
    respuesta=""
    if len(generarCodigo(correo))!=8:
        cnx =abrirConexion()
        cursor = cnx.cursor()
        query=("insert into usuario values(%s,%s)")
        cursor.execute(query,(correo, operaciones.crearCodigo(correo)))
        respuesta = "Registro exitoso"
        cursor.close()
        cnx.commit()
        cnx.close()
    else:
        respuesta = "El correo ya existe"

    return respuesta

##############################################################
##############################################################
####################     #LSM    #############################
##############################################################
##############################################################

# Para buscar una palabra (actualmente solo busca por LEMMA)
def buscarPalabra(tupla):
    resultado = []

    cnx = abrirConexion()
    cursor = cnx.cursor()

    lemma = tupla[0]
    etiqueta = tupla[1]
    colocacion = tupla[2]

    print ('Entra a consulta: ', lemma)

    if colocacion == -1:
        query = ("SELECT palabra, sprite FROM general WHERE lemma LIKE %s COLLATE utf8_bin AND etiqueta LIKE %s LIMIT 1")
        cursor.execute(query, (lemma,etiqueta[0]+'%'))

        # Llena una lista con el resultado de la busqueda
        for (palabra, sprite) in cursor:
            print("{}, {}".format(palabra.encode('utf-8'), sprite.encode('utf-8')))
            resultado.append((palabra.encode('utf-8'), sprite.encode('utf-8')))

        # Si no encontro nada
        if len(resultado) == 0:
            # Revisa la tabla de sinonimos lsm
            query = ("SELECT id_general FROM sinonimoslsm WHERE lemma LIKE %s COLLATE utf8_bin AND etiqueta LIKE %s LIMIT 1")
            cursor.execute(query, (lemma,etiqueta[0]+'%'))
            id_general = cursor.fetchone()
            if id_general: # Si encontro algo en la tabla de sinonimoslsm
                query = ("SELECT palabra, sprite FROM general WHERE id = %s LIMIT 1")
                cursor.execute(query, id_general)   
                for (palabra, sprite) in cursor:
                    print("{}, {}".format(palabra.encode('utf-8'), sprite.encode('utf-8')))
                    resultado.append((palabra.encode('utf-8'), sprite.encode('utf-8')))
            else:  # Si no encotro nada en sinonimos lsm
                # Revisa la tabla de sinonimos en espanol
                query = ("SELECT id_general FROM sinonimosespanol WHERE lemma LIKE %s COLLATE utf8_bin AND etiqueta LIKE %s LIMIT 1")
                cursor.execute(query, (lemma,etiqueta[0]+'%'))
                id_general = cursor.fetchone()
                if id_general:
                    query = ("SELECT palabra, sprite FROM general WHERE id = %s LIMIT 1")
                    cursor.execute(query, id_general)   
                    for (palabra, sprite) in cursor:
                        print("{}, {}".format(palabra.encode('utf-8'), sprite.encode('utf-8')))
                        resultado.append((palabra.encode('utf-8'), sprite.encode('utf-8')))
                # Si no hubo coincidencia en sinonimos lo deletrea
                else:
                    for letra in lemma:
                        query = ("SELECT palabra, sprite FROM general WHERE lemma LIKE %s COLLATE utf8_bin LIMIT 1")
                        print ('BUSCAR: ',letra)
                        cursor.execute(query, (letra,))
                        for (palabra, sprite) in cursor:
                            print("{}, {}".format(palabra.encode('utf-8'), sprite.encode('utf-8')))
                            resultado.append((palabra.encode('utf-8'), sprite.encode('utf-8')))
    else:
        # Revisa la tabla de colocaciones
        query = ("SELECT id_general FROM colocaciones WHERE id = %s LIMIT 1")
        cursor.execute(query, (colocacion,))
        id_general = cursor.fetchone()
        if id_general: # Si encontro algo en la tabla de colocaciones
            query = ("SELECT palabra, sprite FROM general WHERE id = %s LIMIT 1")
            cursor.execute(query, id_general)   
            for (palabra, sprite) in cursor:
                print("{}, {}".format(palabra.encode('utf-8'), sprite.encode('utf-8')))
                resultado.append((palabra.encode('utf-8'), sprite.encode('utf-8')))
        else:
            print ('Error buscando la colocacion')

    cursor.close()
    cnx.commit()
    cnx.close()

    return resultado


def buscarColocacion(tuplaDeTuplas):
    # ( (pal1, tag1), (pal2, tag2) )
    cnx = abrirConexion()
    cursor = cnx.cursor()
    resultado = -1
    reglaFinal = -1
    # Buscar en la tabla de colocaciones
    if len(tuplaDeTuplas) == 3:
        query = ("SELECT id, etiqueta_1, etiqueta_2, etiqueta_3, regla FROM colocaciones WHERE palabra_1 LIKE %s AND palabra_2 LIKE %s AND palabra_3 LIKE %s")
        cursor.execute(query, ( tuplaDeTuplas[0][0] , tuplaDeTuplas[1][0], tuplaDeTuplas[2][0],))
        # Iterar resutlados
        for (id, etiqueta1, etiqueta2, etiqueta3, regla) in cursor:
            if regla == "1":
                if etiqueta1 == tuplaDeTuplas[0][1]:
                    reglaFinal = regla
                    resultado = id
            elif regla == "2":
                if etiqueta2 == tuplaDeTuplas[1][1]:
                    reglaFinal = regla
                    resultado = id
            elif regla == "3":
                if etiqueta3 == tuplaDeTuplas[2][1]:
                    reglaFinal = regla
                    resultado = id
    else:
        query = ("SELECT id, etiqueta_1, etiqueta_2, etiqueta_3, regla FROM colocaciones WHERE palabra_1 LIKE %s AND palabra_2 LIKE %s")
        cursor.execute(query, ( tuplaDeTuplas[0][0] , tuplaDeTuplas[1][0],))
        # Iterar resutlados
        for (id, etiqueta1, etiqueta2, etiqueta3, regla) in cursor:
            if regla == "1":
                if etiqueta1 == tuplaDeTuplas[0][1]:
                    reglaFinal = regla
                    resultado = id
            elif regla == "2":
                if etiqueta2 == tuplaDeTuplas[1][1]:
                    reglaFinal = regla
                    resultado = id

    # id, palabra1, palabra2, palabra3, etiqueta1, etiqueta2, etiqueta3, regla
    cursor.close()
    cnx.commit()
    cnx.close()
    return (resultado, int(reglaFinal))


    
