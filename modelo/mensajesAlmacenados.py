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

{config.nombre_mi_token}: {Tokes} totales
1000== 1 TRX (Aprox)"""

def ma_texto_de_apuesta(monto):
    return f"""Hola, El casino cuenta con esto juegos:
<pre>Dado_A  || x{config.dado["a"]}, si adivinas el #</pre>
    /dado_A #
            Apuestas por #=5 
            Rst=5  <b>Gana</b>:{(monto*2.2):.0f}
            Rst=6  <b>Gana</b>:{(monto*0):.0f}
<pre>Dado_P  ||  x{config.dado["p"]} si sale Par</pre>
    /dado_P
           Si el dado Sale 6,4,2
            Rst=6  <b>Gana</b>:{(monto*1.3):.0f}
           Si el dado Sale 5,3,1
            Rst=5  <b>Gana</b>:{(monto*0):.0f}
<pre>Dado_I  ||  x{config.dado["i"]} si sale Impar</pre>
    /dado_I
           Si el dado Sale 5,3,1
            Rst=5  <b>Gana</b>:{(monto*1.3):.0f}
           Si el dado Sale 6,4,2
            Rst=6  <b>Gana</b>:{(monto*0):.0f}

si el dado bota 0 <b>ganas</b> $100 usdt
<pre>Por defecto estas apostando [{monto}]Token</pre>"""

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
<b>App api_hash</b>: <pre>**{api_has[2:-2]}**</pre>
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

def ma_verSaldo(saldo,quien):
    return f"""@{quien}
Su saldo es de <b>{saldo}</b> {config.nombre_mi_token}

<pre>Equivalente a {(saldo*0.00095):.3f} TRX</pre>
para retirar presione aqui!
    """

def ma_cancelar():
    return "Cancelar"
def ma_msj_retirar():
    return f"""
Hola, para retirar ten encuenta que te descontaremos el 5%
se te cancelara en Cualquier grupo que tenga en comun con @VueJson
si no estas en ninguno te recomendamos el grupo vinculado a @BotColombia

procede a escribir el monto de {config.nombre_mi_token} a retirar, o {ma_cancelar()}
"""

def ma_msj_recarga():
    return f"""
Hola, para recargar enviale en un grupo que tenga en comun con @VueJson
si no estas en ninguno te recomendamos el grupo vinculado a @BotColombia 
"""
def ma_msj_ref(id_user,l):
    print(l)
    return f"""
Tu link de referido es:
https://t.me/{config.arroba}?start={id_user}

Gana el 1% de deposito y tarea de tu referidos :D

{l}
"""
 

def ma_procesando_retiro(monto,id_user):
    return f"""procesando retiro  <a href="tg://user?id={id_user}">Usuario!!</a>
    <b>De:</b> {monto} {config.nombre_mi_token}
    <b>Manera:</b> Manual
    <pre>Equivalente a {(monto*0.00095):.3f} TRX</pre>
    
    <i>Pronto renviamos el mensaje de @cctip_bot como evidencia</i>
    """
def ma_pasar_sobre():
    return """
Para pasar saldo a otro usuario seleccionandolo
+pasar [cantidad]
                <b>Ejemplo:</b> +pasar 100
"""
def ma_pasar_user():
    return """
Para Pasar saldo a otro usuario por username
+pasar [cantidad] [@username]
                <b>Ejemplo:</b> +pasar 100 @VueJson
"""
def ma_botones(cual):
    if(cual=="Info"):
        return "Info"
    if(cual=="Casino"):
        return "Casino"
    if(cual=="add_cuenta"):
        return "Agregar Cuenta"
    if(cual=="lista_cuanta"):
        return "Listar Cuenta"
    if(cual=="Saldo"):
        return "Saldo"
    if(cual=="ref"):
        return "Referidos"
    if(cual=="pasar"):
        return "+pasar"
    if(cual=="recargar"):
        return "+add"
    return "._."