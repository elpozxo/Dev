class Usuario:
    def __init__(self=None, nombre=None, apellidos=None, user=None, user_id=None, user_id2=None, fecha=None, fecha_ultima=None, ref_id=None, principal=None, disponible=None,montoApuesta=0):
        self.nombre = validate(nombre)
        self.apellidos = validate(apellidos)
        self.user = validate(user)
        self.user_id = validate(user_id)
        self.user_id2 = validate(user_id2)
        self.fecha = validate(fecha)
        self.fecha_ultima = validate(fecha_ultima)
        self.ref_id = validate(ref_id)
        self.principal = validate(principal)
        self.disponible = validate(disponible)
        self.MontoApuesta=montoApuesta
        self.admin = False

    def __str__(self):
        return f"Usuario: {self.nombre} {self.apellidos}, User: {self.user}, ID: {self.user_id}"

class Principal:
    def __init__(self=None, grupo=None, id_user=None, api_id=None, api_hash=None, disponible=None):
        self.grupo = validate(grupo)
        self.id_user = validate(id_user)
        self.api_id = validate(api_id)
        self.api_hash = validate(api_hash)
        self.disponible = validate(disponible)

    def __str__(self):
        return f"Grupo: {self.grupo}, ID User: {self.id_user}, API ID: {self.api_id}, API Hash: {self.api_hash}, Disponible: {self.disponible}"

class Cuenta:
    def __init__(self=None, id_usuario=None, numero=None,activo=None,ultimo=None,fecha=None,ban=None,elid=None):
        self.id_usuario = id_usuario
        self.numero = numero
        self.activo = activo
        self.ultimo = ultimo
        self.fecha = fecha
        self.ban = ban
        self.elid =elid

    def __str__(self):
        return f'Cuenta(ID Usuario: {self.id_usuario}, Saldo: {self.ban}, #: {self.numero})'

class Saldo:
    def __init__(self=None,id_usuario=None, saldo=None, fecha_actualizacion=None,motivo=None):
        self.id_usuario = id_usuario
        self.saldo = saldo
        self.fecha_actualizacion = fecha_actualizacion
        self.motivo = motivo
 
    @classmethod
    def from_dict(cls, data):
        # Crea una instancia del objeto desde un diccionario
        return cls(
            id_usuario=data['id_usuario'],
            saldo_actual=data['saldo_actual'],
            fecha_actualizacion=data['fecha_actualizacion']
        )


def validate(texto):
    if texto is None :
        return ""
    return texto
# Ejemplo de uso
# usuario1 = Usuario(nombre=None, apellidos="", user="johndoe", user_id="123", user_id2="456",fecha="2023-01-01", fecha_ultima="2023-12-31", ref_id="ref123", principal=True, disponible=True)
