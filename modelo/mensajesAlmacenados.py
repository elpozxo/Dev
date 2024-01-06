import config
def ma_enviarmensaje_Nuevo():
    return f"""Hola!\nEste bot se creo con la finalidad de realizar tarea con las cuentas segundarias, programando un comando que puedad segir las demas por los que lo puedes ver como un autoclick mejorado para cuentas de tg.\n 

Pero no todo los bot's son utilizaado con autoclick asi que debes saber que no puedo hacer:\n
                *)  Leer las imagenes de los bots
                *)  Cualquier otro sera anotado.

@{config.arroba} No se hace responsable de:
                *) Perdida de cuenta
                *) Acceso a cuenta 
                *) Eliminancion de cuenta 
                *) Saldo perdido por prestamo, 
                    olvido, de cuenta a terceros
                    (si lo activa) 
            """

def ma_enviarmensaje_info(total,disponible,Tokes):
    return f"""Informacion del @{config.arroba}\n
Actualmente contamos con {total} de cuentas unidad de las cuales disponibles para cualquiere tarea {disponible}

Token: {Tokes} totales
100 == 1 TRX (Aprox)"""

def ma_texto_de_apuesta(monto):
    return f"""Hola, El casino cuenta con esto juegos:
*) Dado_A:
    X3, si adivinas el numero
    /dado_A
    
*) Dado_p
    x1.5 si sale Par/Impar
    /dado_P
    
*)Pronto agregamos MAS.

Por defecto estas apostando [{monto}]Token"""

def ma_falta_hash():
    return """Para agregar tus cuentas necesitamos que agregues un Hash propio para la seguridad de tu cuentas

Para ello dirígete a [Api Telegram](https://my.telegram.org/auth) 
Una vez registrado, [registra tu hash](https://my.telegram.org/apps) 

copiando el "*App api_id*" & "*App api_hash*" para agregarlo aquí.
"""

def ma_no_falta_hash(api_id,api_has,grupo,disponible):
    if disponible=="" or not disponible:
        disponible="No"
    else:
        disponible="Si"
    if grupo=="":
        grupo="Chat individuales"
    return f"""La información almacenada de tu 
<a href="https://my.telegram.org/auth">Api Telegram</a>

<b>App api_id</b>: {api_id}
<b>App api_hash</b>: {api_has}
<b>Grupo Principal</b>: {grupo}
<b>Disponibilidad para tarea</b>: {disponible}
"""

def ma_envia_hash_id():
    return """El *Api_Id* es un numero 
*Ingreselo ahora*:"""

def ma_envia_hash():
    return """El *Api_Hash* Ingreselo ahora:"""

def ma_envia_grupo():
    return """El *Grupo* debe ser publico, y las cuenta no debe estar BAN por escritura, o con permiso especial para poder escribir en el grupo. 
    Recuerda solo poner el @grupo y que este sea publico
    Ingreselo ahora:"""

def ma_botones(cual):
    if(cual=="Info"):
        return "Info"
    if(cual=="Casino"):
        return "Casino"
    if(cual=="add_cuenta"):
        return "Agregar Cuenta"
    if(cual=="lista_cuanta"):
        return "Listar Cuenta"
    return "._."