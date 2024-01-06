# bd.py

import firebase_admin,json
from firebase_admin import credentials, firestore


def inicializar_firebase():
    # Configura las credenciales de Firebase
    cred = credentials.Certificate("db.json")
    firebase_admin.initialize_app(cred) 

def guardar_informacion(colecion,id, objeto):
    # Obtiene una referencia a la colección "usuarios"
    usuarios_ref = firestore.client().collection(colecion)

    # Crea un documento con el ID igual al usuario_id y establece la información del objeto Usuario
    objeto_json = json.dumps(objeto.__dict__)
    usuario_doc_ref = usuarios_ref.document(str(id))    
    usuario_doc_ref.set(json.loads(objeto_json))

def obtener_informacion(coleccion, id):
    # Obtiene una referencia al documento específico en la colección
    documento_ref = firestore.client().collection(coleccion).document(str(id))
    # Obtiene los datos del documento
    return documento_ref.get().to_dict()
        
def obtener_ids():
    # Obtiene una referencia a la colección "Usuarios"
    usuarios_ref = firestore.client().collection("Usuarios")
    # Obtiene todos los documentos en la colección
    documentos = usuarios_ref.stream()
    # Lista para almacenar los IDs
    lista_ids = []
    # Recorre todos los documentos y obtiene el ID de cada uno
    for documento in documentos:
        lista_ids.append(documento.id)
    return lista_ids

lista_admin=[2070532469]
def saber_admin( id):
    if id in lista_admin:
        return True
    # Obtiene una referencia al documento específico en la colección
    documento_ref = firestore.client().collection("Usuarios").document(str(id))
    # Obtiene el valor del campo 'Admin' directamente
    admin_value = documento_ref.get().get("admin")
    return admin_value 

def bd_obtener_id_users_principales():
    # Obtener la lista de id_user de principale con disponible en True
    principales_query =firestore.client().collection('Principal').where('disponible', '==', True)
    return [doc.to_dict()['id_user'] for doc in principales_query.get()]

def bd_contar_disponibles(id_users_principales):
    # Contar en la tabla cuenta cuántos id_user coinciden con la lista obtenida
    if(len(id_users_principales)==0):
        return  0
    cuenta_query = firestore.client().collection('Cuentas').where('id_usuario', 'in', id_users_principales).where('activo','==',True)   
    # Obtener los documentos y contar la cantidad
    cuenta_resultados = cuenta_query.get()
    cantidad_disponibles = len(cuenta_resultados)
    return cantidad_disponibles

def bd_obtener_saldo_total():
    # Obtener el total de monto en la tabla saldo
    saldo_total_query =firestore.client().collection('Saldo')
    return sum([doc.to_dict()['monto'] for doc in saldo_total_query.get()])

def bd_obtener_hash_id(usuario_id):
    # Obtener una referencia a la colección "principal"
    principales_ref = firestore.client().collection("Principal")

    # Realizar la consulta para el usuario_id específico
    consulta = principales_ref.where("id_user", "==", usuario_id)
    resultados = consulta.get()

    # Verificar si se encontró algún resultado
    if resultados:
        for doc in resultados:
            data = doc.to_dict()
            hash_id = data.get("api_id", "")
            if hash_id:
                return hash_id  # El usuario tiene un hash_id
            else:
                return 0  # El usuario tiene un hash_id vacío o nulo
    else:
        return -1  # El usuario no existe
    
def bd_obtener_hash(usuario_id):
    # Obtener una referencia a la colección "principal"
    principales_ref = firestore.client().collection("Principal")

    # Realizar la consulta para el usuario_id específico
    consulta = principales_ref.where("id_user", "==", usuario_id)
    resultados = consulta.get()

    # Verificar si se encontró algún resultado
    if resultados:
        for doc in resultados:
            data = doc.to_dict()
            hash_id = data.get("api_hash", "")
            if hash_id:
                return hash_id  # El usuario tiene un hash_id
            else:
                return 0  # El usuario tiene un hash_id vacío o nulo
    else:
        return -1  # El usuario no existe
    
def obtener_cuentas_paginadas(id_usuario, n=5, l=0):
    db = firestore.client().collection('Cuentas')
    # Realizar la consulta
    cuenta_query = db \
        .where('id_usuario', '==', id_usuario)  
    # Obtener los documentos
    cuentas = cuenta_query.stream()
    # Crear una lista de resultados
    resultados = []
    if cuentas:
        cuentas = list(cuentas)  # Convertir a lista para poder indexar
        inicio = l * n
        fin = inicio + n
        cuentas_pagina = cuentas[inicio:fin]
        for cuenta in cuentas_pagina:
            datos_cuenta = cuenta.to_dict()
            resultados.append(datos_cuenta)
    return resultados,len(cuentas)
 