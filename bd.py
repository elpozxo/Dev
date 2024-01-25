# bd.py

import firebase_admin,json
from firebase_admin import credentials, firestore
import warnings 

def inicializar_firebase():
    # Configura las credenciales de Firebase
    
    warnings.simplefilter("ignore", category=UserWarning)
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

def cambiar_estado_cuenta(colecion,id,nombre_dato,dato):
    # Referencia a la colección "Cuentas" en Firestore
    coleccion_cuentas = firestore.client().collection(colecion)
    cuenta_ref = coleccion_cuentas.document(id)
    # Actualizar el campo "estado" con el nuevo valor
    cuenta_ref.update({nombre_dato: dato})    
    return cuenta_ref.get().to_dict()
        
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
    principales_query =firestore.client().collection('Principal').where(field_path='disponible', op_string='==', value=True)
    return [doc.to_dict()['id_user'] for doc in principales_query.get()]

def bd_contar_disponibles(id_users_principales):
    # Contar en la tabla cuenta cuántos id_user coinciden con la lista obtenida
    if(len(id_users_principales)==0):
        return  0
    cuenta_query = firestore.client().collection('Cuentas')\
        .where(field_path='id_usuario',op_string= 'in',value= id_users_principales)\
        .where(field_path='activo',op_string='==',value=True)   
    # Obtener los documentos y contar la cantidad
    cuenta_resultados = cuenta_query.get()
    cantidad_disponibles = len(cuenta_resultados)
    return cantidad_disponibles

def bd_obtener_saldo_total():
    # Obtener el total de monto en la tabla saldo
    saldo_total_query =firestore.client().collection('Saldo')
    return sum([doc.to_dict()['saldo'] for doc in saldo_total_query.get()])

def bd_obtener_saldo_total_user(id_user):
    # Obtener el total de monto en la tabla saldo
    saldo_total_query =firestore.client().collection('Saldo')\
        .where(field_path='id_usuario',op_string= '==', value=id_user)    
    return sum([doc.to_dict()['saldo'] for doc in saldo_total_query.get()])

def bd_obtener_hash_id(usuario_id):
    # Obtener una referencia a la colección "principal"
    principales_ref = firestore.client().collection("Principal")
    # Realizar la consulta para el usuario_id específico
    consulta = principales_ref.where(field_path="id_user", op_string="==", value=usuario_id)
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
    consulta = principales_ref.where(field_path="id_user",op_string="==", value=usuario_id)
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
    cuenta_query = db.where(field_path='id_usuario',op_string='==',value= id_usuario)  
    # Obtener los documentos
    cuentas = cuenta_query.stream() 
    # Crear una lista de resultados
    resultados = []
    resultados2 = []
    if cuentas: 
        cuentas = list(cuentas)  # Convertir a lista para poder indexar
        for cuenta in cuentas:
            datos_cuenta = cuenta.to_dict() 
            if(datos_cuenta.get("ban")!=True):
                resultados2.append(datos_cuenta) 
        cuentas=resultados2
         
        inicio = l * n
        fin = inicio + n
        cuentas_pagina = cuentas[inicio:fin]
        for cuenta in cuentas_pagina: 
            resultados.append(cuenta)
    return resultados,len(cuentas)
 
def obtener_referidos(id_usuario):    
    principales_ref = firestore.client().collection("Usuarios")
    # Realizar la consulta para el usuario_id específico
    consulta = principales_ref.where(field_path='ref_id',op_string= '==',value= str(id_usuario))
    return consulta.stream() 

def obtener_iduser(arroba): 
    principales_ref = firestore.client().collection("Usuarios")
    # Realizar la consulta para el usuario específico
    consulta = principales_ref.where('user','==', arroba).limit(1).stream()
    # Verificar si se encontró algún resultado
    for usuario in consulta:
        datos_usuario = usuario.to_dict() 
        # Verificar si el resultado tiene la clave 'user_id'
        if 'user_id' in datos_usuario:
            return datos_usuario['user_id']
    return None
        
def obtener_arroba(iduser): 
    principales_ref = firestore.client().collection("Usuarios")
    # Realizar la consulta para el usuario específico
    consulta = principales_ref.where(field_path='user_id', op_string='==',value= iduser).limit(1).stream()
    # Verificar si se encontró algún resultado
    for usuario in consulta:
        datos_usuario = usuario.to_dict()
        # Verificar si el resultado tiene la clave 'user_id'
        if 'user' in datos_usuario:
            return datos_usuario['user']

def obtener_saldos_agrupados():
    # Obtén una referencia a la colección Saldo
    saldo_ref = firestore.client().collection('Saldo')
    # Obtén todos los documentos de la colección Saldo
    documentos_saldo = saldo_ref.stream()
    # Crear un diccionario para almacenar las sumas por id
    sumas_por_id = {}
    # Iterar sobre los documentos de Saldo
    for doc in documentos_saldo:
        # Obtener datos del documento Saldo
        datos_saldo = doc.to_dict()
        id_usuario = datos_saldo.get('id_usuario')
        monto = int(datos_saldo.get('saldo', 0))
        # Sumar el monto al total para el id de usuario correspondiente
        sumas_por_id[id_usuario] = sumas_por_id.get(id_usuario, 0) + monto
    return sumas_por_id
    
def obtener_saldos_id_agrupados(id):
    # Obtén una referencia a la colección Saldo
    saldo_ref = firestore.client().collection('Saldo')
    # Obtén todos los documentos de la colección Saldo
    saldo_ref=saldo_ref.where(field_path="id_usuario",op_string="==",value=(id))
    documentos_saldo = saldo_ref.stream()
    # Crear un diccionario para almacenar las sumas por id
    sumas_por_id = {}
    # Iterar sobre los documentos de Saldo
    for doc in documentos_saldo:
        # Obtener datos del documento Saldo
        datos_saldo = doc.to_dict()  
        monto = int(datos_saldo.get('saldo', 0))
        motivo = (datos_saldo.get('motivo', "??"))
        # Sumar el monto al total para el id de usuario correspondiente
        sumas_por_id[motivo] = sumas_por_id.get(motivo, 0) + monto
    return sumas_por_id

def bd_obtener_staking(id_user):
    # Obtener el staking con estado True en la tabla Staking
    saldo_total_query = firestore.client().collection('Staking')\
        .where(field_path='id_user',op_string= '==',value= id_user)\
        .where(field_path='estado',op_string= '==',value= True).limit(1).get()
    if saldo_total_query:    
        return saldo_total_query[0].to_dict()     
    return None

def bd_obtener_saldo_staking_user(id_user):
    # Obtener el total de monto en la tabla saldo
    saldo_total_query =firestore.client().collection('Staking')\
        .where(field_path='id_user',op_string= '==',value= id_user)\
        .where(field_path='estado',op_string= '==',value= True)    
    return sum([doc.to_dict()['monto'] for doc in saldo_total_query.get()])

def xxx(): 
    consulta =firestore.client().collection('Usuarios').stream()
    for documento in consulta:
        # Obtener el valor actual del campo 'user'
        user_actual = documento.get('user')
        # Convertir el valor a minúsculas y actualizar en la base de datos
        user_minusculas = user_actual.lower() 
        documento.reference.update({'user': user_minusculas})