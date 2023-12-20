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

def ma_no_falta_hash(api_id,api_has):
    return f"""La información almacenada de tu [Api Telegram](https://my.telegram.org/auth) 

*App api_id*={api_id}
*App api_hash*={api_has}
"""

def ma_envia_hash_id():
    return """El *Api_Id* es un numero 
*Ingreselo ahora*:"""

def ma_botones(cual):
    if(cual=="Info"):
        return "Info"
    if(cual=="Casino"):
        return "Casino"
    if(cual=="add_cuenta"):
        return "Agregar Cuenta"
    return "._."