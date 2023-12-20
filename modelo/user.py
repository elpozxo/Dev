class Usuario:
    def __init__(self=None, nombre=None, apellidos=None, user=None, user_id=None, user_id2=None, fecha=None, fecha_ultima=None, ref_id=None, principal=None, disponible=None):
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

    # Puedes agregar más métodos según las operaciones que necesites realizar con instancias de esta clase


def validate(texto):
    if texto is None :
        return ""
    return texto
# Ejemplo de uso
# usuario1 = Usuario(nombre=None, apellidos="", user="johndoe", user_id="123", user_id2="456",fecha="2023-01-01", fecha_ultima="2023-12-31", ref_id="ref123", principal=True, disponible=True)
