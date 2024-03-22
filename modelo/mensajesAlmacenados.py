import config

idioma="es"

def ma_cambiar_idioma(cual): 
    global idioma
    if cual =="es":
        idioma = "es"
    else:
        idioma ="en" 

def ma_enviarmensaje_Nuevo():
    textos = {
        "es": f"""Hola!\nEste bot se creo con la finalidad de realizar tarea con las cuentas segundarias, programando un comando que puedad segir las demas por los que lo puedes ver como un autoclick mejorado para cuentas de tg.\n 

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
            """,
        "en": f"""Hello!\nThis bot was created with the purpose of performing tasks with secondary accounts, programming a command that can follow others so you can see it as an enhanced autoclick for tg accounts.\n 

But not all bots are used with autoclick, so you should know that I cannot do:\n
                *)  Read images from bots
                *)  Any other will be annotated.

@{config.arroba} is not responsible for:
                *) Lost account
                *) Account access 
                *) Account deletion 
                *) Lost balance due to loan, 
                    forgetfulness, transfer to third parties
                    (if activated) 
            """
    }
    return textos[idioma]

def ma_enviarmensaje_info(total,disponible,Tokes):
    texto={
        "es":f"""Informacion del @{config.arroba}\n
Actualmente contamos con {total} de cuentas unidad de las cuales disponibles para cualquiere tarea {disponible}

{config.nombre_mi_token}: {Tokes} totales
1000== 1 TRX (Aprox)

Ayuda? /ayuda""",
        "en":f"""Information about @{config.arroba}\n
Currently, we have {total} accounts, of which {disponible} are available for any task.

{config.nombre_mi_token}: {Tokes} total
1000 == 1 TRX (Approx)

Need help? /ayuda"""
    }
    return texto[idioma]

def ma_texto_de_apuesta(monto):
    textos = {
        "es": f"""Hola, El casino cuenta con estos juegos:
<pre>Dado_A  || x{config.dado["a"]}, si adivinas el número</pre>
    /dado_A #
            Apuestas por #: 5 
            Rst=5  <b>Ganas</b>: {(monto*2.2):.0f}
            Rst=6  <b>Ganas</b>: {(monto*0):.0f}
<pre>Dado_P  ||  x{config.dado["p"]} si sale Par</pre>
    /dado_P
           Si el dado sale 6, 4, 2
            Rst=6  <b>Ganas</b>: {(monto*1.3):.0f}
           Si el dado sale 5, 3, 1
            Rst=5  <b>Ganas</b>: {(monto*0):.0f}
<pre>Dado_I  ||  x{config.dado["i"]} si sale Impar</pre>
    /dado_I
           Si el dado sale 5, 3, 1
            Rst=5  <b>Ganas</b>: {(monto*1.3):.0f}
           Si el dado sale 6, 4, 2
            Rst=6  <b>Ganas</b>: {(monto*0):.0f}

Si el dado bota 0 <b>Ganas</b> $100 USDT
<pre>Por defecto, estás apostando [{monto}] Tokens</pre>""",

        "en": f"""Hello, The casino has these games:
<pre>Dice_A  || x{config.dado["a"]}, if you guess the number</pre>
    /dice_A #
            Bet on #: 5 
            Rst=5  <b>Wins</b>: {(monto*2.2):.0f}
            Rst=6  <b>Wins</b>: {(monto*0):.0f}
<pre>Dice_P  ||  x{config.dado["p"]} if it comes up Even</pre>
    /dice_P
           If the die comes up 6, 4, 2
            Rst=6  <b>Wins</b>: {(monto*1.3):.0f}
           If the die comes up 5, 3, 1
            Rst=5  <b>Wins</b>: {(monto*0):.0f}
<pre>Dice_I  ||  x{config.dado["i"]} if it comes up Odd</pre>
    /dice_I
           If the die comes up 5, 3, 1
            Rst=5  <b>Wins</b>: {(monto*1.3):.0f}
           If the die comes up 6, 4, 2
            Rst=6  <b>Wins</b>: {(monto*0):.0f}

If the die rolls 0, <b>you win</b> $100 USDT
<pre>By default, you are betting [{monto}] Tokens</pre>"""
    }

    return textos[idioma]

def ma_falta_hash():
    texto = {
    "es": f"""Para agregar tus cuentas necesitamos que agregues un Hash propio para la seguridad de tu cuentas

Para ello dirígete a [Api Telegram](https://my.telegram.org/auth) 
Una vez registrado, [registra tu hash](https://my.telegram.org/apps) 

copiando el "*App api_id*" & "*App api_hash*" para agregarlo aquí.""",
    "en": f"""To add your accounts, we need you to add your own hash for the security of your accounts.

To do this, go to [Telegram API](https://my.telegram.org/auth) 
Once registered, [register your hash](https://my.telegram.org/apps) 

by copying the "*App api_id*" & "*App api_hash*" to add them here."""
}
    return texto[idioma]

def ma_no_falta_hash(api_id, api_has, grupo, disponible):
    if disponible == "" or not disponible:
        disponible = "No"
    else:
        disponible = "Si"
    if grupo == "":
        grupo = "Chat individuales"

    texto = {
        "es": f"""La información almacenada de tu 
        <a href="https://my.telegram.org/auth">Api Telegram</a>

        <b>App api_id</b>: {api_id}
        <b>App api_hash</b>: <pre>**{api_has[2:-2]}**</pre>
        <b>Grupo Principal</b>: {grupo}
        <b>Disponibilidad para tarea</b>: {disponible}
        """,
        "en": f"""Stored information from your 
        <a href="https://my.telegram.org/auth">Api Telegram</a>

        <b>App api_id</b>: {api_id}
        <b>App api_hash</b>: <pre>**{api_has[2:-2]}**</pre>
        <b>Main Group</b>: {grupo}
        <b>Task Availability</b>: {disponible}
        """
    }

    return texto[idioma]

def ma_envia_hash_id():
    texto = {
        "es": f"""El *Api_Id* es un numero 
        *Ingreselo ahora*:""",
        "en": f"""The *Api_Id* is a number 
        *Enter it now*:"""
    }
    return texto[idioma]

def ma_envia_hash():
    texto = {
        "es": f"""El *Api_Hash* Ingreselo ahora:""",
        "en": f"""The *Api_Hash* Enter it now:"""
    }
    return texto[idioma]

def ma_envia_grupo():
    texto = {
        "es": f"""El *Grupo* debe ser público, y la cuenta no debe estar BAN por escritura, o con permiso especial para poder escribir en el grupo. 
            Recuerda solo poner el @grupo y que este sea público
            Ingréselo ahora:""",
        "en": f"""The *Group* must be public, and the account must not be BAN for writing, or have special permission to write in the group. 
            Remember to only enter the @group, and it must be public.
            Enter it now:"""
    }
    return texto[idioma]
def ma_verSaldo(saldo, quien):
    texto = {
        "es": f"""@{quien}
Su saldo es de <b>{saldo}</b> {config.nombre_mi_token}

<pre>Equivalente a {(saldo*0.00095):.3f} TRX</pre>
Para retirar, presione aquí!""",
        "en": f"""@{quien}
Your balance is <b>{saldo}</b> {config.nombre_mi_token}

<pre>Equivalent to {(saldo*0.00095):.3f} TRX</pre>
To withdraw, click here!"""
    }
    return texto[idioma]
def ma_cancelar():
    texto = {
        "es": "Cancelar",
        "en": "Cancel"
    }
    return texto[idioma]

def ma_msj_retirar():
    texto = {
        "es":f"""
Hola, para retirar ten encuenta que te descontaremos el 5%
se te cancelara en {config.grupoPago} 

procede a escribir el monto de {config.nombre_mi_token} a retirar, o {ma_cancelar()}
""",
        "en": f"""
Hi, to withdraw, keep in mind that we will deduct 5%
it will be canceled in {config.grupoPago} 

proceed to write the amount of {config.nombre_mi_token} to withdraw, or {ma_cancelar()}
"""
    }
    return texto[idioma]
def ma_pasar_yo():
    texto = {
        "es": "No puede enviarte a ti mismo",
        "en": "You cannot send to yourself"
    }
    return texto[idioma]

def ma_tepaso_saldo(quien, para, cuanto):
    texto = {
        "es": f"@{quien} te envió {cuanto} {config.nombre_mi_token} a ti @{para}",
        "en": f"@{quien} sent you {cuanto} {config.nombre_mi_token} to @{para}"
    }
    return texto[idioma]

def ma_sinfondo(saldo):
    texto = {
        "es": f"Actualmente no tenemos fondo para este retiro, pruebe más tarde.\n\nSaldo actual para retiros {saldo} TRX",
        "en": f"Currently, we don't have funds for this withdrawal, please try again later.\n\nCurrent balance for withdrawals {saldo} TRX"
    }
    return texto[idioma]

def ma_no_tienestanto():
    texto = {
        "es": "No cuentas con saldo, por favor recarga!",
        "en": "You don't have enough balance, please top up!"
    }
    return texto[idioma]

def ma_msj_recarga():
    texto = {
        "es": f"""
Hola, para recargar enviale en {config.grupoPago} trx a @vuejSon
ejemplo `cc 1 trx @vuejSon`
""",
        "en": f"""
Hello, to top up, send trx to @vuejSon in {config.grupoPago}
example `cc 1 trx @vuejSon`
"""
    }
    return texto[idioma]

def ma_recarga():
    texto = {
        "es": "Recarga!",
        "en": "Reload!"
    }
    return texto[idioma]
def ma_msj_ref(id_user, l):
    texto = {
        "es": f"""
Tu enlace de referencia es:
https://t.me/{config.arroba}?start={id_user}

Gana el 1% de depósito y tareas de tus referidos :D

{l}
""",
        "en": f"""
Your referral link is:
https://t.me/{config.arroba}?start={id_user}

Earn 1% of deposit and tasks from your referrals :D

{l}
"""
    }
    return texto[idioma]
def ma_pagado():
    texto = {
        "es": "Pagado!",
        "en": "Paid!"
    }
    return texto[idioma]
def ma_norelacion():
    texto = {
        "es": f"Los retiros se procesan solamente en {config.grupoPago}.\nÚnase y retire de nuevo",
        "en": f"Withdrawals are processed only in {config.grupoPago}.\nJoin and withdraw again"
    }
    return texto[idioma]
def ma_procesando_retiro(monto):
    texto = {
        "es": f"Procesando retiro. {monto} {config.nombre_mi_token}",
        "en": f"Processing withdrawal. {monto} {config.nombre_mi_token}"
    }
    return texto[idioma]
def ma_error_mensaje():
    texto = {
        "es": "Error desconocido al enviar mensaje a usuario",
        "en": "Unknown error while sending message to user"
    }
    return texto[idioma]

def ma_mira_menu():
    texto = {
        "es": "Mira Nuestro Menú",
        "en": "Check Our Menu"
    }
    return texto[idioma]
def ma_inStaking(staking):
    texto = {
        "es": f"\n\n<b>Tienes en Staking</b>: [{staking.monto}]\n<b>Iniciado</b>:{staking.fecha_inicio}",
        "en": f"\n\n<b>You have in Staking</b>: [{staking.monto}]\n<b>Started</b>:{staking.fecha_inicio}"
    }
    return texto[idioma]
def ma_staking():
    texto = {
        "es": "Para estar al tanto de bots y demás para ganar gratis, únete a @BotColombia",
        "en": "To stay informed about bots and other ways to earn for free, join @BotColombia"
    }
    return texto[idioma]
def ma_newstaking():
    texto = {
        "es": "¡Tu Staking comenzó ahora!",
        "en": "Your Staking has started now!"
    }
    return texto[idioma]
def ma_error_flotante():
    texto = {
        "es": "Error al manejar la acción del botón flotante.",
        "en": "Error handling the floating button action."
    }
    return texto[idioma]
def ma_msj_api_staking():
    texto = {
        "es": "Api de {config.apiStaking}%\nDebe permanecer al menos 5 días para desbloquear\nsolo cuenta día pasado. *Envíe la cantidad entera a bloquear*",
        "en": "Api of {config.apiStaking}%\nMust stay at least 5 days to unlock\nonly counts past day. *Send the whole amount to lock*"
    }
    return texto[idioma]
def ma_unStaking():
    texto = {
        "es": "¡Staking retirado!",
        "en": "Staking withdrawn!"
    }
    return texto[idioma]
def ma_espere():
    texto = {
        "es": "::[Espere por favor]",
        "en": "::[Please wait]"
    }
    return texto[idioma]
def ma_espere_staking():
    texto = {
        "es": "Debe esperar al menos 5 días",
        "en": "You must wait at least 5 days"
    }
    return texto[idioma]
def ma_no_staking():
    texto = {
        "es": "No tienes saldo en Staking",
        "en": "You don't have Staking balance"
    }
    return texto[idioma]
def ma_ejp_num_celular():
    texto = {
        "es": "Ejemplo de número celular +573001112233\nDonde +57 es el *indicativo* del país\n*Envíe el número*",
        "en": "Example of phone number +573001112233\nWhere +57 is the *country code*\n*Send the number*"
    }
    return texto[idioma]
def ma_validando_api():
    texto = {
        "es": "_Validando Api_",
        "en": "_Validating Api_"
    }
    return texto[idioma]
def ma_validando_apihast(api, has):
    texto = {
        "es": f"Validando Tu Api Tg <pre>[{api}]</pre>:<pre>[{has}]</pre>",
        "en": f"Validating Your Tg Api <pre>[{api}]</pre>:<pre>[{has}]</pre>"
    }
    return texto[idioma]
def ma_envie_celular():
    texto = {
        "es": "Envie numero celular",
        "en": "Send cellphone number"
    }
    return texto[idioma]
def ma_cerrar():
    texto = {
        "es": "Cerrar",
        "en": "Close"
    }
    return texto[idioma]
def ma_agregar():
    texto = {
        "es": "Agregar",
        "en": "Add"
    }
    return texto[idioma]
def ma_grupo():
    texto = {
        "es": "Grupo",
        "en": "Group"
    }
    return texto[idioma]
def ma_disponible():
    texto = {
        "es": "Disponible",
        "en": "Available"
    }
    return texto[idioma]
def ma_numero():
    texto = {
        "es": "Número",
        "en": "Number"
    }
    return texto[idioma]
def ma_numerok():
    texto = {
        "es": "Número Ok!",
        "en": "Number Ok!"
    }
    return texto[idioma]
def ma_validando_numero():
    texto = {
        "es": "Validando Número",
        "en": "Validating Number"
    }
    return texto[idioma]
def ma_validando_codigo():
    texto = {
        "es": "Validando Código",
        "en": "Validating Code"
    }
    return texto[idioma]
def ma_nose_valido_numrro():
    texto = {
        "es": "No se pudo validar el número",
        "en": "Failed to validate the number"
    }
    return texto[idioma]
def ma_numero_entero():
    texto = {
        "es": "Debe ser un número entero",
        "en": "It must be an integer"
    }
    return texto[idioma]
def ma_numero_sesion_borrada(numero):
    texto = {
        "es": f"Esta cuenta [{numero}] borró la *Sesión* del bot, ¿quieres volver a registrar?",
        "en": f"This account [{numero}] deleted the bot's *Session*, do you want to re-register?"
    }
    return texto[idioma]
def ma_elimino_numero(numero):
    texto = {
        "es": f"Cuenta {numero} se eliminó",
        "en": f"Account {numero} was deleted"
    }
    return texto[idioma]
def ma_codigoa():
    texto = {
        "es": "Se envió un código a:",
        "en": "A code was sent to:"
    }
    return texto[idioma]
def ma_numero_noescribe():
    texto = {
        "es": "Se valida la cuenta, pero no sirve para escribir en grupos. ¿Quieres eliminarla?",
        "en": "The account is validated but cannot write in groups. Do you want to delete it?"
    }
    return texto[idioma]
def ma_recuperar():
    texto = {
        "es": "Recuperar",
        "en": "Recover"
    }
    return texto[idioma]
def ma_no_sevalido_numero():
    texto = {
        "es": "No se pudo validar el número\nVerifique que tenga el código de seguridad desactivado mientras te registra.",
        "en": "Could not validate the number\nMake sure you have security code disabled while registering."
    }
    return texto[idioma]
def ma_numero_errado():
    texto = {
        "es": "Este número está errado, se procede a *ELIMINARLO AUTOMÁTICAMENTE*.",
        "en": "This number is incorrect, it will be *AUTOMATICALLY REMOVED*."
    }
    return texto[idioma]
def ma_numero_nogrupos():
    texto = {
        "es": "Se valida la cuenta, pero no sirve para unirse a canales.\nSe procede a *ELIMINARLO AUTOMÁTICAMENTE*.",
        "en": "The account is validated but cannot join channels.\nIt will be *AUTOMATICALLY REMOVED*."
    }
    return texto[idioma]
def ma_ganaste(cuanto):
    texto = {
        "es": f"Ganaste!\nTu saldo es {cuanto} {config.nombre_mi_token}",
        "en": f"You won!\nYour balance is {cuanto} {config.nombre_mi_token}"
    }
    return texto[idioma]
def ma_buscando_numero(numero):
    texto = {
        "es": f"Buscando la información de [{numero}]",
        "en": f"Searching for information of [{numero}]"
    }
    return texto[idioma]
def ma_perdiste(cuanto):
    texto = {
        "es": f"Perdiste!\nTu saldo es {cuanto} {config.nombre_mi_token}",
        "en": f"You lost!\nYour balance is {cuanto} {config.nombre_mi_token}"
    }
    return texto[idioma]
def ma_borrar():
    texto = {
        "es": "Borrar",
        "en": "Delete"
    }
    return texto[idioma]
def ma_teInvito(quien):
    texto = {
        "es": f"¡Hola!\nInvitado por [{quien}](tg://user?id={quien}).",
        "en": f"Hello!\nInvited by [{quien}](tg://user?id={quien})."
    }
    return texto[idioma]
def ma_hola():
    texto = {
        "es": "¡Hola!",
        "en": "Hello!"
    }
    return texto[idioma]
def ma_monto_apuesta():
    texto = {
        "es": "Envie monto de apuesta",
        "en": "Send bet amount"
    }
    return texto[idioma]
def ma_monto_apuesta_nuevo(monto):
    texto = {
        "es": f"Su nuevo monto de apuesta es de {monto}\n¡Vuelve a jugar de nuevo!",
        "en": f"Your new bet amount is {monto}\nPlay again!"
    }
    return texto[idioma]
def ma_monto_apuesta_cambiar():
    texto = {
        "es": "Cambiar Monto Apuesta",
        "en": "Change Bet Amount"
    }
    return texto[idioma]
def ma_espere_juego_anterior():
    texto = {
        "es": "Espera que termine el anterior Juego",
        "en": "Wait for the previous game to finish"
    }
    return texto[idioma]
def ma_Invitaste(username):
    texto = {
        "es": f"Invitaste a @{username}",
        "en": f"You invited @{username}"
    }
    return texto[idioma]
def ma_procesando_retiro(monto, id_user):
    texto = {
        "es": f"""procesando retiro <a href="tg://user?id={id_user}">Usuario!!</a>
    <b>De:</b> {monto} {config.nombre_mi_token}
    <b>Manera:</b> Automático
    <pre>Equivalente a {(monto*0.00095):.3f} TRX</pre>

    <i>Pronto reenviamos el mensaje de @cctip_bot como evidencia</i>
    """,
        "en": f"""Processing withdrawal <a href="tg://user?id={id_user}">User!!</a>
    <b>From:</b> {monto} {config.nombre_mi_token}
    <b>Method:</b> Automatic
    <pre>Equivalent to {(monto*0.00095):.3f} TRX</pre>

    <i>We will soon forward the message from @cctip_bot as evidence</i>
    """
    }
    return texto[idioma]
def ma_pasar_sobre():
    texto = {
        "es": f"""
Para pasar saldo a otro usuario seleccionándolo
+pasar [cantidad]
                <b>Ejemplo:</b> +pasar 100
""",
        "en": f"""
To transfer balance to another user, select them
+transfer [amount]
                <b>Example:</b> +transfer 100
"""
    }
    return texto[idioma]
def ma_pasar_user():
    texto = {
        "es": f"""
Para pasar saldo a otro usuario por nombre de usuario
+pasar [cantidad] [@username]
                <b>Ejemplo:</b> +pasar 100 @VueJson
""",
        "en": f"""
To transfer balance to another user by username
+transfer [amount] [@username]
                <b>Example:</b> +transfer 100 @VueJson
"""
    }
    return texto[idioma]
def ma_minExplicacion_tarea():
    texto = {
        "es": f"""
Aquí tienes una breve descripción de algunos de los comandos principales del bot.
Toda la información detallada y ejemplos se encuentran en el canal @multicuentabobot_ayuda.

<pre>Unirse a Canales/Grupos públicos</pre><b>#unirser</b> Ejemplo  <i>#uniser @botcolombiachat,@multicuentabobot_ayuda</i> 

<pre>Unirse a Canales/Grupos privados</pre><b>#Privunirser</b> Ejemplo  <i>#Privunirser hacsa+1233ko1,+23iojd8w8s-jw</i>

<pre>Unirse a Bots</pre><b>/botRef</b> Ejemplo  <i>#botRef https://t.me/mult1sbot?start=2070532469</i>
<b>#sbot</b> Ejemplo  <i>#sbot @mult1sbot</i>
<b>#ref</b> Ejemplo  <i>#Ref 2070532469</i>

<pre>Enviar mensaje</pre><b>#mensaje</b> Ejemplo  <i>#mensaje  ✅  check</i>

<pre>Esperar Segundos</pre><b>#espera</b> Ejemplo  <i>#espera 5</i>

<b>Ok</b>
Envía /tarea + la combinación que quieras que realicen tus cuentas.

El código se ejecutará con tu primera cuenta y luego preguntará si continúa con las demás.
""",
        "en": f"""
Here is a brief description of some of the main bot commands.
All detailed information and examples are available in the @multicuentabobot_ayuda channel.

<pre>Join public channels/groups</pre><b>#unirser</b> Example  <i>#unirser @botcolombiachat,@multicuentabobot_ayuda</i> 

<pre>Join private channels/groups</pre><b>#Privunirser</b> Example  <i>#Privunirser hacsa+1233ko1,+23iojd8w8s-jw</i>

<pre>Join Bots</pre><b>/botRef</b> Example  <i>#botRef https://t.me/mult1sbot?start=2070532469</i>
<b>#sbot</b> Example  <i>#sbot @mult1sbot</i>
<b>#ref</b> Example  <i>#Ref 2070532469</i>

<pre>Send a message</pre><b>#mensaje</b> Example  <i>#mensaje  ✅  check</i>

<pre>Wait for Seconds</pre><b>#esperar</b> Example  <i>#esperar 5</i>

<b>Ok</b>
Send /task + the combination you want your accounts to perform.

The code will run with your first account and then ask if it continues with the others.
"""
    }
    return texto[idioma]
def ma_maxExplicacion_tarea():
    texto = {
        "es": f"""<b>Description of bot commands</b>
<pre>Join public channels/groups</pre><b>#join</b> 
Example  
<i>#join @botcolombiachat,@multicuentabobot_ayuda</i> 
<i>#join https://t.me/botcolombiachat,https://t.me/multicuentabobot_ayuda</i> 

Remember <b>not to use spaces</b> to separate the channels you want to join, only <b>","</b>.
You are charged every 9 links.

<pre>Join private channels/groups</pre><b>#joinPrivate</b> 
Example  
<i>#joinPrivate @+23thsGo2VEhiYTBh</i> 
<i>#joinPrivate https://t.me/+23thsGo2VEhiYTBh</i> 

Remember <b>not to use spaces</b> to separate the channels you want to join, only <b>","</b>.
You are charged every 9 links.

<pre>Join Bots</pre><b>#botRef</b> 
Example  <i>#botRef https://t.me/mult1sbot?start=2070532469</i>
If you have the complete link.
<b>#sbot</b> Example  <i>#sbot @mult1sbot</i>
If it has the "@" symbol.
<b>#ref</b> Example  <i>#Ref 2070532469</i>
And the reference parameter.

<pre>Send message</pre><b>#message</b> Example  <i>#message ✅ check</i>

This message is sent to the @bot parameter.

We can also send an extra message like #extraMessage @botcolombiachat ✅ check
where @botcolobiachat is the username to whom the message will be sent.

We can also send a random one like #randomMessage message 1;;message 2;;message 3
where we randomly select 1 and send it.

<pre>Utilities</pre>

We can also wait like #wait 5
where 5 means 5 seconds of waiting before performing the next action.

We can also create a text or number chain of x length
#number 5  or #letter 5
where 5 is the length of the text to create.

We can also search for your wallet address for a token on @cctit_bot
#wallet bttnew
where it returns a trc20 address
#wallet2 trx 0
where it returns an address of a network option number 0.
""",

        "en": f"""<b>Descripcion de los comando bot</b>
<pre>Uniserce a Canales/Grupos publicos</pre><b>#uniser</b> 
Ejp  
<i>#unirser @botcolombiachat,@multicuentabobot_ayuda</i> 
<i>#unirser https://t.me/botcolombiachat,https://t.me/multicuentabobot_ayuda</i> 

recuerda <b>no usar espacio</b> para separar los canales a unirte, solo <b>","</b>
se cobra cada 9 link

<pre>Uniserce a Canales/Grupos privado</pre><b>#Privunirser</b> 
Ejp  
<i>#Privunirser @+23thsGo2VEhiYTBh</i> 
<i>#Privunirser https://t.me/+23thsGo2VEhiYTBh</i> 

recuerda <b>no usar espacio</b> para separar los canales a unirte, solo <b>","</b>
se cobra cada 9 link

<pre>Uniserce a Bot</pre><b>#botRef</b> Ejp  <i>#botRef https://t.me/mult1sbot?start=2070532469</i>
por si tienes el link completo
<b>#sbot</b> Ejp  <i>#sbot @mult1sbot</i>
por si tiene el arroba de bor
<b>#ref</b> Ejp  <i>#Ref 2070532469</i>
y el parametro de referencia

<pre>Enviar mensaje</pre><b>#mensaje</b> Ejp  <i>#mensaje ✅ check</i>

este mensaje se envia a el parametro de @bot

Tambien podemos enviar mensaje extra asi #mensajextra @botcolombiachat ✅ check
donde @botcolobiachat es username a quien le enviara el mensaje

Tambien  podemos enviar un rando asi #mensajedom mensaje 1;;mensaje 2;;mensaje 3
donde aleatoriamente selecionamos 1 y se envia

<pre>Utilez</pre>

Tambien  podemos esperar asi #esperar 5
donde 5 sig 5seg de espera para realizar la sig accion

Tambien podemos crear cadena texto o numero de x largo
#numero 5  ó #letra 5
donde 5 es el largo del texto a crear

tambien podemos buscar tu dirrecion wallet de una token en @cctit_bot
#wallet bttnew
donde regresa una direcion trc20
#wallet2 trx 0
donde regresa una direcion de una opciones de red la numero 0
"""
    }
    return texto[idioma]
def ma_dado_nok():
    texto = {
        "es": "No se pudo obtener el valor del dado.",
        "en": "Unable to retrieve the dice value."
    }
    return texto[idioma]
def ma_restaking():
    texto = {
        "es": "Tu Staking ReComienza ahora!",
        "en": "Your Staking Restarts now!"
    }
    return texto[idioma]
def ma_sincuentas():
    texto = {
        "es": "Debe registrar cuentas para poder usar el apartado tarea",
        "en": "You must register accounts to use the task section"
    }
    return texto[idioma]
def ma_error_numero(error, contador):
    texto = {
        "es": f"La cuenta {error} ha perdido el acceso, así que el sistema la eliminará.\n"
              "Recuerda borrar las cuentas a las que les hayas revocado el acceso al bot.\n"
              f"La tarea se detuvo en la cuenta número {contador}",
        "en": f"The account {error} has lost access, so the system will remove it.\n"
              "Remember to delete accounts that you have revoked access to the bot.\n"
              f"The task stopped at account number {contador}"
    }
    return texto[idioma]
def ma_tg_no_play():
    texto = {
        "es": "Lo sentimos, tu Telegram no soporta juegos",
        "en": "Sorry, your Telegram doesn't support games"
    }
    return texto[idioma]
def ma_botones(cual):
    texto = {
        "es": {
            "add_cuenta": "Agregar Cuenta",
            "agregar_staking": "🚀 Agregar Staking",
            "apartado": "🏗 Apartado de Tareas",
            "Casino": "🎉 Casino",
            "Ganar": "💸 Ganar",
            "Info": "🚏 Info",
            "lista_cuanta": "Listar Cuenta",
            "pasar": "+pasar",
            "recarga": "🧑‍🎤 Recargar",
            "ref": "🖇 Referidos",
            "reclamar_staking": "🍾 Reclamar",
            "retirar": "📤 Retirar",
            "sacar_staking": "🫀 Retirar Staking",
            "Saldo": "🗞 Saldo",
            "atras": "🔙 Atras"
        },
        "en": {
            "add_cuenta": "Add Account",
            "agregar_staking": "🚀 Add Staking",
            "apartado": "🏗 Task Section",
            "Casino": "🎉 Casino",
            "Ganar": "💸 Earn",
            "Info": "🚏 Info",
            "lista_cuanta": "List Accounts",
            "pasar": "+pasar",
            "recarga": "🧑‍🎤 Reload",
            "ref": "🖇 Referrals",
            "reclamar_staking": "🍾 Claim",
            "retirar": "📤 Withdraw",
            "sacar_staking": "🫀 Withdraw Staking",
            "Saldo": "🗞 Balance",
            "atras": "🔙 Back"
        }
    }
    return texto[idioma][cual] if idioma in texto and cual in texto[idioma] else "._."
