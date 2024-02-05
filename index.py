from decimal import Decimal
import config,re,logging, threading,requests,asyncio
from flask import Flask, request, abort
from time import sleep
from telebot import TeleBot, types, util
from telegram import KeyboardButton, ReplyKeyboardMarkup 
from datetime import datetime
from modelo.user import Cuenta, Principal, Saldo, Staking, Usuario
from modelo.mensajesAlmacenados import *
from codigo import EjecutarTaarea, Inicializar, Logear_a, Logear_ab, buscarRecarga, pagara, saldoAdmin, validarcuenta
from bd import *
from datetime import datetime, timedelta
import math 
# Inicializar Firebase
inicializar_firebase()


app = Flask(__name__)
main_bot = TeleBot(config.MAIN_BOT_TOKEN)
tokens = {config.MAIN_BOT_TOKEN: True}
lista_hashid_input=[]
lista_hash_input=[]
lista_grupo_input=[]
lista_disponible_input=[]
lista_addnumero_input=[] 
lista_addnumerocodigo_input=[] 
lista_addnumerocodigo_input2=[] 
lista_retiro_input=[] 
lista_montoApuesta_input=[]
lista_staking_input=[] 

lista_casino_espera=[]
# Configura el sistema de registros
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_hora():
    current_time = datetime.now().strftime("%H:%M:%S")
    return str(current_time)
def get_fecha():
    current_time = datetime.now().strftime("%Y-%m-%d")
    return str(current_time)
def horatodo():
    return get_fecha()+" "+get_hora()

def aplicar_estilo(texto, estilo):
    # Aplica el estilo si está definido
    if estilo == 't':
        return f"<i><b>{texto}</b></i>"
    elif estilo == 'c':
        return f"<code>{texto}</code>"
    elif estilo == 'ta':
        return f"<pre>{texto}</pre>"
    else:
        return texto

def es_admin(id):
    try:
        return saber_admin(id) 
    except:
        return False

def remplace_texto(texto,de,a):
    cadena_con_punto_y_coma = re.sub(de, a, texto)
    return (cadena_con_punto_y_coma)

def crear_linea_boton(texto):
    # Verificar si se proporciona una lista de textos
    if isinstance(texto, list):
        # Crear botones en línea para cada texto en la lista
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for linea_texto in texto:
            fila = [types.KeyboardButton(boton_texto.strip()) for boton_texto in linea_texto.split(';')]
            keyboard.add(*fila)
    else:
        # Crear botones en línea para el texto proporcionado
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        fila = [types.KeyboardButton(boton_texto.strip()) for boton_texto in texto.split(';')]
        keyboard.add(*fila)
    return keyboard

def crear_linea_fboton(texto): 
    if isinstance(texto, list):
        # Crear botones en línea para cada texto en la lista
        keyboard = types.InlineKeyboardMarkup()
        for linea_texto in texto:
            fila = [types.InlineKeyboardButton(text=boton_texto.strip(), callback_data=f'boton_{boton_texto.strip()}') for boton_texto in linea_texto.split(';')]
            keyboard.add(*fila)
    else:
        # Crear botones en línea para el texto proporcionado
        keyboard = types.InlineKeyboardMarkup()
        fila = [types.InlineKeyboardButton(text=boton_texto.strip(), callback_data=f'boton_{boton_texto.strip()}') for boton_texto in texto.split(';')]
        keyboard.add(*fila)
    return keyboard

def enviar_mensaje(lista_ids, mensaje): 
    mens=0
    for usuario_id in lista_ids:
        try:
            mens=main_bot.send_message(usuario_id, mensaje) 
        except Exception as e:
            # Manejar otras excepciones no previstas
            print(f"{ma_error_mensaje()} enviar_mensaje {usuario_id} ")
    return mens

def responder_mensaje(lista_ids, mensaje,a):
    for usuario_id in lista_ids:
        try:
            mens=main_bot.send_message(usuario_id, mensaje,reply_to_message_id=a)    
        except  : 
            print(f"{ma_error_mensaje()} responder_mensaje {usuario_id} ")
    return mens

def renviar_mensaje(a_id,de_id,mensaje_id):
    try:
        mens=main_bot.forward_message(a_id,de_id,mensaje_id.id)         
    except Exception as e:
        # Manejar otras excepciones no previstas
        print(f"{ma_error_mensaje()} renviar_mensaje {a_id}")
    return mens

def enviar_mensaje_parse(lista_ids, mensa,parse="Markdown"):
    mensaje=0
    for usuario_id in lista_ids:
        try:  
            mensaje=main_bot.send_message(usuario_id, mensa,parse_mode=parse) 
            mensaje=mensaje.message_id 
        except Exception as e:
            # Manejar otras excepciones no previstas
            print(f"{ma_error_mensaje} enviar_mensaje_parse {usuario_id}")
            print(mensa)
    return mensaje
    
def enviar_mensaje_flotante(lista_ids, mens,boton,parse="Markdown",responder=0): 
    for usuario_id in lista_ids:
        try:
            mensaje=0
            if(responder==0):
                mensaje=main_bot.send_message(usuario_id, mens,parse_mode=parse,reply_markup=boton) 
            else:
                mensaje=main_bot.send_message(usuario_id, mens,parse_mode=parse,reply_markup=boton,reply_to_message_id=responder)  
        except Exception as e:
            # Manejar otras excepciones no previstas
            print(f"{ma_error_mensaje()} enviar_mensaje_flotante {usuario_id} ")
            return False
    return mensaje

def enviar_alerta(usuario_id, mensaje,parse_mode="NO",minutos=3):
    # Crear un mensaje con teclado en línea vacío
    markup = types.InlineKeyboardMarkup()    
    # Crear un botón "Cerrar" que no realiza ninguna acción
    btn_cerrar = types.InlineKeyboardButton(f"{ma_cerrar()}", callback_data='cerrar_alerta')
    markup.add(btn_cerrar)
    # Enviar el mensaje con el teclado en línea
    if parse_mode=="NO":
        mensaje_enviado = main_bot.send_message(usuario_id, mensaje, reply_markup=markup)
    else:
        mensaje_enviado = main_bot.send_message(usuario_id, mensaje, reply_markup=markup,parse_mode=parse_mode)
    # Configurar el temporizador para cerrar el mensaje después de 3 minutos    
    threading.Timer(minutos*60, cerrar_alerta_auto, args=[mensaje_enviado.chat.id, mensaje_enviado.message_id]).start()

# Función para cerrar automáticamente el mensaje
def cerrar_alerta_auto(chat_id, message_id):
    try:
        main_bot.delete_message(chat_id, message_id)
    except:
        f=1
def borrarultimosmenaje( message_id,chat_id,c):
    for i in range(1,1+c):
        try:
            main_bot.delete_message(chat_id, message_id-i)
        except:
            f=1
def borrar_mensaje_en( minutos=3,id_user=0,mensaje=0):   
    threading.Timer(minutos*60, cerrar_alerta_auto, args=[id_user,mensaje]).start()
# Manejar la acción de cerrar alerta
@main_bot.callback_query_handler(func=lambda call: call.data == 'cerrar_alerta')
def cerrar_alerta_callback(query):
    # Eliminar el mensaje original con el teclado en línea
    try:
        main_bot.delete_message(query.message.chat.id, query.message.message_id)
    except:
        f=1

def botonesInicio(id):
    main_bot.send_message(id,f"{ma_mira_menu()}", 
        reply_markup=crear_linea_boton(
            [ 
                f"{ma_botones('apartado')}",
                f"{ma_botones('Saldo')};{ma_botones('ref')}",
                f"{ma_botones('Casino')};{ma_botones('Ganar')}",
                f"{ma_botones('Info')}"
            ] 
        )
    )
def botonesTarea(id):
    main_bot.send_message(id, f"{ma_mira_menu()}", 
        reply_markup=crear_linea_boton(
            [
                f"{ma_botones('add_cuenta')};{ma_botones('lista_cuanta')}",
                f"{ma_botones('atras')}"
            ] 
        )
    )
def botonesGana(id):    
    staking=bd_obtener_staking(id)  
    text_add=""  
    if(staking):        
        staking = cargarStaking(staking)
        text_add=f"{ma_inStaking(staking)}"
    main_bot.send_message(id, f"{ma_staking()} {text_add}",
        reply_markup=crear_linea_boton(
            [
                f"{ma_botones('agregar_staking')};{ma_botones('sacar_staking')}",
                f"{ma_botones('reclamar_staking')}",
                f"{ma_botones('atras')}"
            ] 
        ),parse_mode="HTML"
    )

# Manejar la acción del botón flotante
@main_bot.callback_query_handler(func=lambda call: 'DO_Agregar_Api_id' in call.data)
def handle_btf_apihash_nuevo(call):
    try:
        main_bot.delete_message(call.message.chat.id, call.message.message_id)
        # Obtener el id_user del callback_data
        id_user = int(call.data.split(":")[1])
        # Llamar a la función con el id_user
        DO_Agregar_Api_id(id_user)
    except:
        print(f"{ma_error_flotante('DO_Agregar_Api_id')}")

def DO_Agregar_Api_id(id_user):
    main_bot.send_message(id_user, ma_envia_hash_id(), parse_mode="Markdown") 
    lista_hashid_input.append(id_user)

# Manejar la acción del botón flotante
@main_bot.callback_query_handler(func=lambda call: 'DO_Agregar_Api' in call.data)
def handle_btf_apihash_nuevo(call):
    try:
        main_bot.delete_message(call.message.chat.id, call.message.message_id)
        # Obtener el id_user del callback_data
        id_user = int(call.data.split(":")[1])
        # Llamar a la función con el id_user
        DO_Agregar_Api(id_user)
    except   : 
        print(f"{ma_error_flotante('DO_Agregar_Api')}") 

def DO_Agregar_Api(id_user):
    main_bot.send_message(id_user, ma_envia_hash(), parse_mode="Markdown") 
    lista_hash_input.append(id_user)

# Manejar la acción del botón flotante
@main_bot.callback_query_handler(func=lambda call: 'DO_Agregar_grupo' in call.data)
def handle_btf_DO_Agregar_grupo(call):
    try:
        main_bot.delete_message(call.message.chat.id, call.message.message_id)
        # Obtener el id_user del callback_data
        id_user = int(call.data.split(":")[1])
        # Llamar a la función con el id_user
        DO_Agregar_grupo(id_user)
    except  :
        print(f"{ma_error_flotante('DO_Agregar_grupo')}") 

def DO_Agregar_grupo(id_user):
    main_bot.send_message(id_user, ma_envia_grupo(), parse_mode="Markdown") 
    lista_grupo_input.append(id_user)

# Manejar la acción del botón flotante
@main_bot.callback_query_handler(func=lambda call: 'DO_disponible' in call.data)
def handle_btf_DO_disponible(call):
    try:        
        id_user = int(call.data.split(":")[1])
        main_bot.delete_message(id_user, call.message.message_id)
        # Obtener el id_user del callback_data
        # Llamar a la función con el id_user
        p = Principal()
        p=cargarPrincipal(obtener_informacion("Principal", id_user)) 
        if p.disponible=="" or not p.disponible:
            p.disponible=True
        else:
            p.disponible=False 
        guardar_informacion("Principal",id_user,p)  
        AgregarAcc(id_user)
        logger.info(f"User {id_user} envió [disponible]  "+horatodo()) 
    except :
        print(f"{ma_error_flotante('DO_disponible')}")  

@main_bot.callback_query_handler(func=lambda call: 'DO_Agregar_Numero' in call.data)
def handle_btf_DO_Agregar_Numero(call):
    try:        
        id_user = int(call.data.split(":")[1])
        main_bot.delete_message(id_user, call.message.message_id)         
        mensaje_para_borrar=main_bot.send_message(
            id_user, 
            f"{ma_validando_api()}",
            reply_markup= crear_linea_fboton(f"{ma_espere()}"),
            parse_mode="Markdown"
        )
        main_bot.delete_message(id_user, mensaje_para_borrar.message_id)         
        mensaje_para_borrar=main_bot.send_message(
            id_user, 
            f"{ma_ejp_num_celular()}",
            reply_markup= crear_linea_fboton(f"{ma_envie_celular()}"),
            parse_mode="Markdown"
        )
        lista_addnumero_input.append(id_user)
        minutos=3
        threading.Timer(minutos*60, cerrar_alerta_auto, args=[id_user,mensaje_para_borrar]).start()
        logger.info(f"User {id_user} envió [DO_Agregar_Numero]  "+horatodo()) 
    except   :
        print(f"{ma_error_flotante('DO_Agregar_Numero')}")  

def btf_apihash_nuevo(id_user):  
    keyboard = types.InlineKeyboardMarkup() 
    fila = [
        types.InlineKeyboardButton(text=f"{ma_agregar()} Api_Id" , callback_data=f'DO_Agregar_Api_id:{id_user}'),
        types.InlineKeyboardButton(text=f"{ma_agregar()} Api_Hash" , callback_data=f'DO_Agregar_Api:{id_user}') ] 
    keyboard.add(*fila) 
    return keyboard

def btf_apihash(id_user):  
    keyboard = types.InlineKeyboardMarkup() 
    fila = [
        types.InlineKeyboardButton(text=f"{ma_agregar()} Api_Id" , callback_data=f'DO_Agregar_Api_id:{id_user}'),
        types.InlineKeyboardButton(text=f"{ma_agregar()} Api_Hash" , callback_data=f'DO_Agregar_Api:{id_user}') 
        ]     
    fila1 = [
        types.InlineKeyboardButton(text=f"{ma_agregar()} {ma_grupo()}" , callback_data=f'DO_Agregar_grupo:{id_user}'),
        types.InlineKeyboardButton(text=f"{ma_disponible()}" , callback_data=f'DO_disponible:{id_user}') 
        ] 
    fila2=[
         types.InlineKeyboardButton(text=f"{ma_agregar()} {ma_numero()}" , callback_data=f'DO_Agregar_Numero:{id_user}') 
    ]
    keyboard.add(*fila)     
    keyboard.add(*fila1)     
    keyboard.add(*fila2)     
    return keyboard

@main_bot.callback_query_handler(func=lambda call: 'DO_btf_sin_acceso_numero_Recuperar' in call.data)
def handle_DO_btf_sin_acceso_numero_Recuperar(call):
    # Obtener los parámetros de la callback data 
    datos_callback = call.data.split(':') 
    datos_tupla = eval(datos_callback[1])
    numero, id_user = datos_tupla 
    agrego_new_numero(numero,id_user)

@main_bot.callback_query_handler(func=lambda call: 'DO_btf_sin_acceso_numero_borrar' in call.data)
def handle_DO_btf_sin_acceso_numero_borrar(call):
    # Obtener los parámetros de la callback data 
    datos_callback = call.data.split(':') 
    datos_tupla = eval(datos_callback[1])
    numero, id_user = datos_tupla 
    x=(cambiar_estado_cuenta("Cuentas",f"{id_user}{numero}","ban",True))
    if(x!=None):
        enviar_mensaje([id_user],f"{ma_elimino_numero(numero)}")
        borrarultimosmenaje( call.message.message_id,id_user,5)        
        ListarCuenta(5,0,id_user)

def btf_sin_acceso_numero(id_user,numero):  
    keyboard = types.InlineKeyboardMarkup() 
    fila = [
        types.InlineKeyboardButton(text=f"{ma_recuperar()}" , callback_data=f'DO_btf_sin_acceso_numero_Recuperar:{numero,id_user}'),
        types.InlineKeyboardButton(text=f"{ma_borrar()}" , callback_data=f'DO_btf_sin_acceso_numero_borrar:{numero,id_user}')
        ]  
    keyboard.add(*fila)       
    return keyboard

def btf_numero_ban_grupo_borrar(id_user,numero):  
    keyboard = types.InlineKeyboardMarkup() 
    fila = [ 
        types.InlineKeyboardButton(text=f"{ma_borrar()}" , callback_data=f'DO_btf_sin_acceso_numero_borrar:{numero,id_user}')
        ]  
    keyboard.add(*fila)       
    return keyboard

@app.route(f"/{config.WEBHOOK_PATH}/<token>", methods=['POST']) #telegram_webhook
def webhook(token: str):
    if not tokens.get(token):
        return abort(404)
    if request.headers.get('content-type') != 'application/json':
        return abort(403)
    json_string = request.get_data().decode('utf-8')
    update = types.Update.de_json(json_string)
    if token == main_bot.token:
        main_bot.process_new_updates([update])
    else:
        from_update_bot = TeleBot(token)
        from_update_bot.process_new_updates([update])
    return ''

@main_bot.message_handler(commands=['start'] , func=lambda message: message.chat.type == 'private')
def handle_start(message: types.Message):
    ma_cambiar_idioma(message.from_user.language_code)
    user_id_referente = message.text.split(' ')[1] if len(message.text.split(' ')) > 1 else None
    user_info = message.from_user     
    logger.info(f"User {user_info.id} @{user_info.username} envió [start]  "+horatodo()) 
    us = Usuario(
        nombre=user_info.first_name,
        apellidos=user_info.last_name,
        user=user_info.username.lower(),
        user_id=user_info.id,
        user_id2=None,
        fecha=f"{get_fecha()} {get_hora()}",  # Combina fecha y hora
        fecha_ultima=None,  # Puedes ajustar esto según tus necesidades
        ref_id=None,  # Puedes ajustar esto según tus necesidades
        principal=None,  # Puedes ajustar esto según tus necesidades
        disponible=None  # Puedes ajustar esto según tus necesidades
    ) 
            ##BONO?
    if not obtener_informacion("Usuarios",user_info.id):  
        if(user_id_referente!=None):
            if(message.from_user.id!=user_id_referente ):
                us.ref_id=user_id_referente 
                enviar_mensaje([user_id_referente], f"{ma_Invitaste(user_info.username)}")  
            enviar_mensaje_parse([message.chat.id], {ma_teInvito(user_id_referente)},"Markdown") 
            logger.info(f"User {message.from_user.id} envió /hola "+user_id_referente+horatodo())        
        guardar_informacion("Usuarios",us.user_id,us)
        enviar_alerta(message.chat.id,ma_enviarmensaje_Nuevo())
    else:
        enviar_mensaje([message.chat.id], f"{ma_hola()}")  
        logger.info(f"User {message.from_user.id} envió /hola"+horatodo())
    botonesInicio(message.chat.id)

@main_bot.message_handler(commands=['hora'])
def handle_start(message: types.Message):    
    ma_cambiar_idioma(message.from_user.language_code)
    main_bot.send_message(message.chat.id, "¡Hora!:", reply_markup=crear_linea_fboton([remplace_texto(get_fecha(),"-",";"),remplace_texto(get_hora(),":",";")] ))
    logger.info(f"User {message.from_user.id} envió /hora"+horatodo())

@main_bot.message_handler(commands=['mensajem'])
def handle_mensaje(message: types.Message):  
    ma_cambiar_idioma(message.from_user.language_code)  
    if not  es_admin(message.chat.id): 
        main_bot.send_message(message.chat.id,"No Eres Admin!")
        return
    # Obtiene los argumentos del mensaje
    args = message.text.split(' ')[1:]     
    logger.info(f"User {message.from_user.id} envió [mensaje] {message.text}"+horatodo())
    # Verifica si se proporcionó un ID de usuario específico
    if len(args) >= 1:
        args_id = args[0].split(';@')
        if len(args_id) == 2:
            lista_ids = [int(id_) for id_ in args_id[0].split(',')]
            mensaje = {' '.join(map(str, args[1:]))}
            enviar_mensaje(lista_ids, mensaje)
            main_bot.send_message(message.chat.id, f"Mensaje enviado a usuarios con IDs {', '.join(map(str, lista_ids))}")
        else:
            enviar_mensaje(obtener_ids(),' '.join(map(str, args)))
            main_bot.send_message(message.chat.id, "Mensaje enviado a todos")
    else:
        main_bot.send_message(message.chat.id, f"Formato de comando no válido. Uso: `/mensajem id1,id2;@ mensaje alv`",parse_mode="Markdown")

@main_bot.message_handler(func=lambda message: message.text in ['/'+ma_botones("Info"),ma_botones("Info")])
def handle_Info(message: types.Message):  
    ma_cambiar_idioma(message.from_user.language_code)
    idl=bd_obtener_id_users_principales()
    enviar_alerta(message.chat.id,ma_enviarmensaje_info(len(idl),bd_contar_disponibles(idl),bd_obtener_saldo_total()))
    logger.info(f"User {message.from_user.id} envió /info "+horatodo())

@main_bot.callback_query_handler(func=lambda call: 'apuesta_cambiar_monto' in call.data)
def handle_btf_apihash_nuevo(call): 
    id_user=call.message.chat.id
    enviar_mensaje([id_user],f"{ma_monto_apuesta()}")
    lista_montoApuesta_input.append(id_user)

def btf_texto_dado():  
    keyboard = types.InlineKeyboardMarkup() 
    fila = [types.InlineKeyboardButton(text=f"{ma_monto_apuesta_cambiar()}"   
    , callback_data=f'apuesta_cambiar_monto') ]
    keyboard.add(*fila)     
    return keyboard

@main_bot.message_handler(func=lambda message: message.text.startswith('/dado_A') or  message.text.startswith('/dado_a'))
def handle_Info(message: types.Message): 
    ma_cambiar_idioma(message.from_user.language_code)   
    id_user=message.from_user.id     
    id_chat=message.chat.id 
    msn=message.message_id
    user_info=message.from_user
    if id_user in lista_casino_espera:
        return responder_mensaje([id_chat],f"{ma_espere_juego_anterior()}",msn) 
    lista_casino_espera.append(id_user) 
    user=cargarUsuarios(obtener_informacion("Usuarios",id_user))    
    numero=0
    try:
        numero = int(message.text.lower().split('/dado_a')[1].strip()) 
    except ValueError:
        lista_casino_espera.remove(id_user)
        return responder_mensaje([id_chat],f"{ma_numero_entero()}",msn)
    saldo=0
    try:
        saldo=int(bd_obtener_saldo_total_user(id_user) )
    except:
        f=1
    if saldo>0:
        if saldo>=user.MontoApuesta:
            if(user.MontoApuesta>0 ):
                dado=lanzar_dado(id_chat,message.message_id)
                monto=-user.MontoApuesta                
                sald=Saldo(id_user,monto,horatodo(),"dadoA")
                guardar_informacion("Saldo",remplace_texto(f"dadoA_i+{id_user}+"+horatodo()," ","="),sald)
                if dado==numero : 
                    montog=int(user.MontoApuesta*config.dado["a"])
                    sald=Saldo(id_user,montog,horatodo(),"dadoA")
                    guardar_informacion("Saldo",remplace_texto(f"dadoA_f+{id_user}+"+horatodo()," ","="),sald)
                    responder_mensaje([id_chat],f"{ma_ganaste(saldo+monto+montog)}",msn)
                else:
                    responder_mensaje([id_chat],f"{ma_perdiste(saldo+monto)}",msn)
            else:
                responder_mensaje([id_chat],f"{ma_monto_apuesta_nuevo(user.MontoApuesta)}",msn)
        else:
            cambiar_estado_cuenta("Usuarios",str(id_user),"MontoApuesta",saldo)
            responder_mensaje([id_chat],f"{ma_monto_apuesta_nuevo(saldo)}",msn)
    else:
        enviar_mensaje_flotante([id_chat],f"@{message.from_user.username} {ma_recarga()}",btf_depositar(id_user))
    try:
        lista_casino_espera.remove(id_user)
    except:
        f=1    
    logger.info(f"User {user_info.id} @{user_info.username} envió [dadoA] {saldo} "+horatodo()) 

@main_bot.message_handler(func=lambda message: message.text in  ['/dado_p','/dado_P','/dado_p@Mult1sbot'])
def handle_Info(message: types.Message):  
    ma_cambiar_idioma(message.from_user.language_code)  
    id_user=message.from_user.id     
    id_chat=message.chat.id    
    msn=message.message_id
    user_info=message.from_user
    if id_user in lista_casino_espera:
        return responder_mensaje([id_chat],f"{ma_espere_juego_anterior()}",message.message_id) 
    lista_casino_espera.append(id_user) 
    user=cargarUsuarios(obtener_informacion("Usuarios",id_user))    
    numero=[2,4,6]
    saldo=0
    try:
        saldo=int(bd_obtener_saldo_total_user(id_user) )
    except:
        f=1
    if saldo>0:
        if saldo>=user.MontoApuesta:
            if(user.MontoApuesta>0 ):                
                dado=lanzar_dado(id_chat,message.message_id)
                monto=-user.MontoApuesta                
                sald=Saldo(id_user,monto,horatodo(),"dadoP")
                guardar_informacion("Saldo",remplace_texto(f"dadoP_I+{id_user}+"+horatodo()," ","="),sald)
                if dado in numero : 
                    montog=int(user.MontoApuesta*config.dado["p"])
                    sald=Saldo(id_user,montog,horatodo(),"dadoP")
                    guardar_informacion("Saldo",remplace_texto(f"dadoP_f+{id_user}+"+horatodo()," ","="),sald)
                    responder_mensaje([id_chat],f"{ma_ganaste(saldo+monto+montog)}",msn)
                else:
                    responder_mensaje([id_chat],f"{ma_perdiste(saldo+monto)}",msn)
            else:
                responder_mensaje([id_chat],f"{ma_monto_apuesta_nuevo(user.MontoApuesta)}",msn)
        else:
            cambiar_estado_cuenta("Usuarios",str(id_user),"MontoApuesta",saldo)
            responder_mensaje([id_chat],f"{ma_monto_apuesta_nuevo(saldo)}",msn)
    else:
        enviar_mensaje_flotante([id_chat],f"@{message.from_user.username} {ma_recarga()}",btf_depositar(id_user))
    try:
        lista_casino_espera.remove(id_user)
    except:
        f=1
    logger.info(f"User {user_info.id} @{user_info.username} envió [dadoP] {saldo} "+horatodo()) 

@main_bot.message_handler(func=lambda message: message.text in  ['/dado_i','/dado_I','/dado_i@Mult1sbot'])
def handle_Info(message: types.Message):   
    ma_cambiar_idioma(message.from_user.language_code) 
    id_user=message.from_user.id     
    id_chat=message.chat.id     
    msn=message.message_id
    user_info=message.from_user  
    if id_user in lista_casino_espera:
        return responder_mensaje([id_chat],f"{ma_espere_juego_anterior()}",message.message_id) 
    lista_casino_espera.append(id_user) 
    user=cargarUsuarios(obtener_informacion("Usuarios",id_user))    
    numero=[1,3,5]
    saldo=0
    try:
        saldo=int(bd_obtener_saldo_total_user(id_user) )
    except:
        f=1
    if saldo>0:
        if saldo>=user.MontoApuesta:
            if(user.MontoApuesta>0 ):                
                dado=lanzar_dado(id_chat,message.message_id)
                monto=-user.MontoApuesta                
                sald=Saldo(id_user,monto,horatodo(),"dadoI")
                guardar_informacion("Saldo",remplace_texto(f"dadoP_i+{id_user}+"+horatodo()," ","="),sald)
                if dado in numero : 
                    montog=int(user.MontoApuesta*config.dado["p"])
                    sald=Saldo(id_user,montog,horatodo(),"dadoI")
                    guardar_informacion("Saldo",remplace_texto(f"dadoP_f+{id_user}+"+horatodo()," ","="),sald)
                    responder_mensaje([id_chat],f"{ma_ganaste(saldo+monto+montog)}",msn)
                else:
                    responder_mensaje([id_chat],f"{ma_perdiste(saldo+monto)}",msn)
            else:
                responder_mensaje([id_chat],f"{ma_monto_apuesta_nuevo(user.MontoApuesta)}",msn)
        else:
            cambiar_estado_cuenta("Usuarios",str(id_user),"MontoApuesta",saldo)
            responder_mensaje([id_chat],f"{ma_monto_apuesta_nuevo(saldo)}",msn)
    else:
        enviar_mensaje_flotante([id_chat],f"@{message.from_user.username} {ma_recarga()}",btf_depositar(id_user))
    try:
        lista_casino_espera.remove(id_user)
    except:
        f=1
    logger.info(f"User {user_info.id} @{user_info.username} envió [dadoI] {saldo} "+horatodo()) 

def lanzar_dado(chat_id,responder):
    url = f"https://api.telegram.org/bot{config.MAIN_BOT_TOKEN}/sendDice"
    params = {"chat_id": chat_id ,"reply_to_message_id": responder}
    response = requests.get(url, params=params)
    json_data = response.json()
    if 'ok' in json_data and json_data['ok']:  
        dice_value = json_data.get('result', {}).get('dice', {}).get('value')
        if dice_value:
            responder_mensaje([chat_id], dice_value,responder)
            return dice_value
        else:
            enviar_mensaje([chat_id], f"{ma_dado_nok()}")
    else:
        enviar_mensaje([chat_id], f"{ma_tg_no_play()}")
    return 0

@main_bot.message_handler(func=lambda message: message.text in ['/Casino','/casino','/casino@Mult1sbot',ma_botones("Casino")])#incompleto
def handle_Info(message: types.Message):    
    ma_cambiar_idioma(message.from_user.language_code)
    id_user=message.from_user.id     
    id_chat=message.chat.id  
    user=cargarUsuarios(obtener_informacion("Usuarios",id_user))    
    monto_user_id=user.MontoApuesta
    if message.chat.type == 'private':
        enviar_mensaje_flotante([id_chat], ma_texto_de_apuesta(monto_user_id),btf_texto_dado(),"HTML")
    else:
        enviar_mensaje_parse([id_chat], ma_texto_de_apuesta(monto_user_id),"HTML")
    logger.info(f"User {message.from_user.id} envió /casino "+horatodo())

def AgregarAcc(id_user):
    mensaje=0
    hash_id=bd_obtener_hash_id(id_user) 
    if(hash_id in [-1,0]):  
        mensaje=main_bot.send_message(id_user, ma_falta_hash(),parse_mode='Markdown',reply_markup=btf_apihash_nuevo(id_user))
    else:         
        p = Principal()
        p=cargarPrincipal(obtener_informacion("Principal", id_user))
        mensaje=main_bot.send_message(
            id_user,  
            ma_no_falta_hash(p.api_id,p.api_hash,p.grupo,p.disponible),
            parse_mode='HTML',
            reply_markup=btf_apihash(id_user)
        )
    minutos=5
    threading.Timer(minutos*60, cerrar_alerta_auto, args=[mensaje.chat.id,mensaje]).start()

@main_bot.message_handler(func=lambda message: message.text in ['/'+ma_botones("add_cuenta"),ma_botones("add_cuenta")]  and message.chat.type == 'private')
def handle_AgregarAcc(message: types.Message):   
    ma_cambiar_idioma(message.from_user.language_code)
    AgregarAcc(message.chat.id)
@main_bot.message_handler(func=lambda message: message.text in ['/idioma']  and message.chat.type == 'private')
def handle_AgregarAcc(message: types.Message):   
    ma_cambiar_idioma(message.from_user.language_code)
    enviar_mensaje([message.chat.id],message.from_user.language_code)

def cargarPrincipal(consulta):
    p = Principal()
    if consulta:
        # Crea una instancia de la clase Principal con los consulta obtenidos
        p = Principal(
            grupo=consulta.get("grupo"),
            id_user=consulta.get("id_user"),
            api_id=consulta.get("api_id"),
            api_hash=consulta.get("api_hash"),
            disponible=consulta.get("disponible")
        )
    return p
def cargarCuentas(consulta):
    p = Cuenta()
    if consulta: 
        p=Cuenta(
            id_usuario=consulta.get("id_usuario"),
            numero=consulta.get("numero"),
            activo=consulta.get("activo"),
            ultimo=consulta.get("ultimo"),
            fecha=consulta.get("fecha"),
            ban=consulta.get("ban")
        )
        try:
            p.elid=consulta.get("elid") 
        except:
            p.elid=0
    return p
def cargarUsuarios(consulta):
    p=Usuario()
    if consulta:
        p = Usuario( 
            ref_id=consulta.get('ref_id', '2070532469'),
            nombre=consulta.get('nombre', ''),
            apellidos=consulta.get('apellidos', ''),
            user=consulta.get('user', ''),
            user_id=consulta.get('user_id', ''),
            user_id2=consulta.get('user_id2', ''),
            fecha=consulta.get('fecha', ''),
            fecha_ultima=consulta.get('fecha_ultima', ''), 
            principal=consulta.get('principal', False),
            disponible=consulta.get('disponible', False)
            )
        try:            
            p.MontoApuesta=consulta.get('MontoApuesta', 0)
        except:
            p.MontoApuesta=0
    return p
def cargarStaking(consulta):
    staking = Staking(
        id_user=consulta.get('id_user'),  
        monto=consulta.get('monto', 0),
        fecha_inicio=consulta.get('fecha_inicio', datetime.now()),
        estado=consulta.get('estado', True)
    )
    return staking

def agrego_new_numero(nemeri_texto,id_user):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    x=0
    try:
        mensaje_para_borrar=main_bot.send_message(id_user, f"{ma_validando_numero()}",reply_markup=
        crear_linea_fboton(nemeri_texto),parse_mode="Markdown")
        p = Principal()
        p=cargarPrincipal(obtener_informacion("Principal",id_user))  
        Inicializar(p.api_id,p.api_hash) 
        x = loop.run_until_complete(Logear_a(nemeri_texto)) 
        cerrar_alerta_auto(id_user,mensaje_para_borrar)
        if(x==-1):
            main_bot.send_message(id_user, f"{ma_nose_valido_numrro()}",reply_markup=
                crear_linea_fboton(nemeri_texto),parse_mode="Markdown") 
        if(x==0):
            x=Cuenta(id_user,nemeri_texto) 
            lista_addnumerocodigo_input.append(x)
            lista_addnumerocodigo_input2.append(id_user)
            main_bot.send_message(id_user, f"{ma_codigoa()}",reply_markup=
                crear_linea_fboton(nemeri_texto),parse_mode="Markdown") 
        if(x==1):
            mens=main_bot.send_message(id_user, f"{ma_numerok()}",reply_markup=
                crear_linea_fboton(nemeri_texto),parse_mode="Markdown") 
            borrarultimosmenaje( mens.message_id,id_user,3)
    except Exception as inst:
        print(inst)
        x=-2    

def agrego_new_numero2(cod_texto,nemeri_texto,id_user): 
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    x=0
    try:
        mensaje_para_borrar=main_bot.send_message(id_user,f"{ma_validando_codigo()}",reply_markup=
        crear_linea_fboton(nemeri_texto),parse_mode="Markdown")
        p = Principal()
        p=cargarPrincipal(obtener_informacion("Principal",id_user))  
        Inicializar(p.api_id,p.api_hash) 
        x = loop.run_until_complete(Logear_ab(nemeri_texto,cod_texto)) 
        cerrar_alerta_auto(id_user,mensaje_para_borrar)
        if(x==-1):
            main_bot.send_message(id_user,f"{ma_no_sevalido_numero()}",reply_markup=
                crear_linea_fboton(nemeri_texto),parse_mode="Markdown") 
        if(x==0): 
            mens=main_bot.send_message(id_user, f"{ma_numerok()}",reply_markup=
                crear_linea_fboton(nemeri_texto),parse_mode="Markdown") 
            borrarultimosmenaje( mens.message_id,id_user,5)
        if(x==1):
            mens=main_bot.send_message(id_user, f"{ma_numerok()}",reply_markup=
                crear_linea_fboton(nemeri_texto),parse_mode="Markdown")            
            borrarultimosmenaje( mens.message_id,id_user,3)
    except Exception as inst:
        print(inst)
        x=-2  

def DO_ListarCuenta_validarAll(id_user):
    f=1
 
@main_bot.callback_query_handler(func=lambda call: 'DO_ActivarNumero' in call.data )
def handle_btf_DO_ActivarNumero(call):    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    datos_callback = call.data.split(':') 
    datos_tupla = eval(datos_callback[1])
    numero, id_user = datos_tupla 
    mensaje= main_bot.send_message(id_user, f"{ma_buscando_numero(numero)}]")
    cuenta=Cuenta()
    cuenta=cargarCuentas(obtener_informacion("Cuentas",f"{id_user}{numero}")) 
    p = Principal()
    p=cargarPrincipal(obtener_informacion("Principal",id_user))  
    cerrar_alerta_auto(id_user,mensaje.message_id)
    enviar_alerta(id_user, f"{ma_validando_apihast(p.api_id,p.api_hash[2:-3])}","HTML",5)
    Inicializar(p.api_id,p.api_hash)
    try:
        if(p.grupo==None):
            p.grupo="BotColombiaChat"
        responde_validar,codigo_validarcuenta = loop.run_until_complete(validarcuenta(numero,[p.grupo,"BotColombia"]))        
        ##-1 cuenta sin activar
        ##1 no canales??
        ##2 no escribir
        ##0 ok 
        if codigo_validarcuenta==-1:
            envio_mensaje=enviar_mensaje_flotante([id_user],f"{ma_numero_sesion_borrada(numero)}",btf_sin_acceso_numero(id_user,numero))
            #agrego_new_numero(message.text,message.chat.id)
            if not envio_mensaje:
                enviar_mensaje_parse([id_user],f"{ma_numero_errado()}")
                x=(cambiar_estado_cuenta("Cuentas",f"{id_user}{numero}","ban",True))
                if(x!=None):
                    enviar_mensaje([id_user],f"Cuenta {numero} se Elimino")
                    borrarultimosmenaje( call.message.message_id,id_user,3)
        if codigo_validarcuenta==1:
            enviar_mensaje([id_user],ma_numero_nogrupos())
            x=(cambiar_estado_cuenta("Cuentas",f"{id_user}{numero}","ban",True))
            if(x!=None):
                enviar_mensaje([id_user],f"{ma_elimino_numero(numero)}")
                borrarultimosmenaje( call.message.message_id,id_user,3)        
        if codigo_validarcuenta==2:
            enviar_mensaje_flotante([id_user],ma_numero_noescribe(),btf_numero_ban_grupo_borrar(id_user,numero))
        if codigo_validarcuenta==0:
            enviar_mensaje([id_user],ma_numerok())
            cuenta.ultimo=horatodo()       
            cuenta.activo=True       
            guardar_informacion("Cuentas",f"{id_user}{numero}",cuenta)
            borrarultimosmenaje( call.message.message_id,id_user,6) 
    except Exception as cx:
        print("erroe\n",cx,"f\n") 
    
@main_bot.callback_query_handler(func=lambda call: 'DO_DesActivarNumero' in call.data)
def handle_btf_DO_DesActivarNumero(call):    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    datos_callback = call.data.split(':') 
    datos_tupla = eval(datos_callback[1])
    numero, id_user = datos_tupla   
    x=(cambiar_estado_cuenta("Cuentas",f"{id_user}{numero}","activo",False))             
    borrarultimosmenaje( call.message.message_id,id_user,6)
    ListarCuenta(5,0,id_user) 
    
@main_bot.callback_query_handler(func=lambda call: 'DO_ln_VerNumero' in call.data)
def handle_btf_DO_ln_VerNumero(call):
    datos_callback = call.data.split(':') 
    datos_tupla = eval(datos_callback[1])
    numero, id_user = datos_tupla 
    mensaje= main_bot.send_message(id_user,ma_buscando_numero(numero))
    cuenta=Cuenta()
    cuenta=obtener_informacion("Cuentas",f"{id_user}{numero}")
    cerrar_alerta_auto(id_user,mensaje.message_id)
    id=""
    try:
        if cuenta.get('elid'):
            id=f"{aplicar_estilo('ID:', 't')} <a href='tg://user?id={cuenta.get('elid')}'>{cuenta.get('elid')}</a> \n" 
        else:
            id= f"{aplicar_estilo('ID:', 't')} NO \n" 
    except:
        id= f"{aplicar_estilo('ID:', 't')} NO \n" 
    mensaje = f"Información de la cuenta:\n\n" \
          f"{aplicar_estilo('Número:', 't')} {aplicar_estilo(numero, 'c')}\n" \
          f"{aplicar_estilo('Fecha registro:', 't')} {aplicar_estilo(cuenta.get('fecha'), '')}\n" \
          f"{aplicar_estilo('ultimo log:', 't')} {aplicar_estilo(cuenta.get('ultimo'), '')}\n"\
          f"{aplicar_estilo('Estado:', 't')} {aplicar_estilo(cuenta.get('activo'), '')}\n{id}" 
          
    enviar_alerta(id_user,mensaje,parse_mode="HTML")

@main_bot.callback_query_handler(func=lambda call: 'DO_ln_borrarAll' in call.data)
def handle_btf_DO_ln_borrarAll(call):
    datos_callback = call.data.split(':') 
    datos_tupla = eval(datos_callback[1])
    id_user = datos_tupla 
    mensaje=f"El Borrado maxivo esta inhabilitado"
    enviar_alerta(id_user,mensaje)

@main_bot.callback_query_handler(func=lambda call: 'DO_ListarCuenta_pasar' in call.data)
def handle_DO_ListarCuenta_pasar(call):
    # Extrae los parámetros del callback
    x= eval(call.data.split(':')[1:][0]) 
    id_user, nuevo_index, cuantas = map(int,x)    
    # Llama a la función ListarCuenta con los nuevos parámetros
    cerrar_alerta_auto(id_user,call.message.id)
    ListarCuenta(cuantas, nuevo_index, id_user)

def ListarCuenta(cuantas,index,id_user):  
    l_numeros,cuantes_cuentas=obtener_cuentas_paginadas(id_user,cuantas,index)  
    keyboard = types.InlineKeyboardMarkup() 
    mensaje=0    
    f= [
        types.InlineKeyboardButton(text="Regresar" , callback_data=f'DO_ListarCuenta_pasar:{id_user,index-1,cuantas}'),
        types.InlineKeyboardButton(text=f"{(index)+1} de {math.ceil(cuantes_cuentas/cuantas)}" ,callback_data=f'DO_ListarCuenta_pasar:{id_user,0,cuantas}'),
         ]          
    i= [        
        types.InlineKeyboardButton(text=f"{(index)+1} de {math.ceil(cuantes_cuentas/cuantas)}" , callback_data=f'DO_ListarCuenta_pasar:{id_user,0,cuantas}'),
        types.InlineKeyboardButton(text="Sigiente" , callback_data=f'DO_ListarCuenta_pasar:{id_user,index+1,cuantas}'),
        ]           
    m= [                
        types.InlineKeyboardButton(text="Regresar" , callback_data=f'DO_ListarCuenta_pasar:{id_user,index-1,cuantas}'),
        types.InlineKeyboardButton(text=f"{(index)+1} de {math.ceil(cuantes_cuentas/cuantas)}" , callback_data=f'DO_ListarCuenta_pasar:{id_user,0,cuantas}'),
        types.InlineKeyboardButton(text="Sigiente" , callback_data=f'DO_ListarCuenta_pasar:{id_user,index+1,cuantas}'),
        ]  
    p=[
        types.InlineKeyboardButton(text=f"{(index)+1} de {math.ceil(cuantes_cuentas/cuantas)}" , callback_data=f'DO_ListarCuenta_pasar:{id_user,0,cuantas}'),
    ]               
    if(cuantes_cuentas==0 ):
        enviar_mensaje([id_user],"Sin Numero Regitrados") 
    else:
        ff= [
                types.InlineKeyboardButton(text="    Numeros    ", callback_data=f'DO_ListarCuenta_validarAll:{id_user}' ),
                types.InlineKeyboardButton(text="Estado" , callback_data=f'DO_ListarCuenta_pasar:{id_user,0,cuantas}'),
                types.InlineKeyboardButton(text="Borrar" , callback_data=f'DO_ln_borrarAll:{id_user}')
        ] 
        keyboard.add(*ff)
        for l_numero in l_numeros: 
            numero = l_numero.get('numero')  
            estado = l_numero.get('activo') 
            ban = l_numero.get('ban')
            if ban != True: 
                ff= [
                    types.InlineKeyboardButton(text=numero, callback_data=f'DO_ln_VerNumero:{numero,id_user}'),
                    types.InlineKeyboardButton(text="Activar", callback_data=f'DO_ActivarNumero:{numero,id_user}')
                    if not estado else                    
                    types.InlineKeyboardButton(text="Desactivar", callback_data=f'DO_DesActivarNumero:{numero,id_user}'),
                    types.InlineKeyboardButton(text="Borrar" , callback_data=f'DO_btf_sin_acceso_numero_borrar:{numero,id_user}')
                ] 
                keyboard.add(*ff)      
        if index==0 and cuantes_cuentas<=cuantas*(index+1):
            keyboard.add(*p)
        elif index==0:
            keyboard.add(*i)
        elif index!=0 and cuantes_cuentas<=cuantas*(index+1):            
            keyboard.add(*f)
        else:            
            keyboard.add(*m)
        mensaje= main_bot.send_message(id_user, f"Aqui las lista de tus cuentas [{cuantes_cuentas}]",reply_markup=
            keyboard,
            parse_mode="Markdown") 
        borrar_mensaje_en(5,id_user,mensaje)

@main_bot.message_handler(func=lambda message: message.text in ['/'+ma_botones("lista_cuanta"),ma_botones("lista_cuanta")]  and message.chat.type == 'private')
def handle_AgregarAcc(message: types.Message):  
    ma_cambiar_idioma(message.from_user.language_code) 
    id_user=message.from_user.id
    mensaje=0    
    l=[]
    hash_id=bd_obtener_hash_id(id_user) 
    if(hash_id in [-1,0]):   
        try:
            mensaje=main_bot.send_message(id_user, ma_falta_hash(),parse_mode='Markdown',reply_markup=btf_apihash_nuevo(id_user))
            borrar_mensaje_en(3,id_user,mensaje)
        except:
            f="No pasa nada"
    else:   
        ListarCuenta(5,0,id_user)

def btf_retirar(id_user):  
    keyboard = types.InlineKeyboardMarkup() 
    fila = [
        types.InlineKeyboardButton(text=ma_botones("retirar") , callback_data=f'DO_btf_retirar_Retira:{id_user}'),
        types.InlineKeyboardButton(text=ma_botones("recarga") , callback_data=f'DO_btf_retirar_Recarga:{id_user}')
        ]  
    keyboard.add(*fila)       
    return keyboard

def btf_depositar(id_user):  
    keyboard = types.InlineKeyboardMarkup() 
    fila = [  
        types.InlineKeyboardButton(text=ma_botones("recarga") , callback_data=f'DO_btf_retirar_Recarga:{id_user}')
        ]  
    keyboard.add(*fila)       
    return keyboard

@main_bot.callback_query_handler(func=lambda call: 'DO_btf_retirar_Retira' in call.data)
def handle_DO_ListarCuenta_pasar(call):
    datos_callback = call.data.split(':') 
    datos_tupla = eval(datos_callback[1])
    id_user = datos_tupla  
    enviar_mensaje_parse([id_user],ma_msj_retirar())
    lista_retiro_input.append(id_user)

def escribiRetirar(monto,id_user,messaje):
    try:
        monto = int(monto)
    except ValueError:
        return enviar_mensaje([id_user],ma_numero_entero())   
    enviar_mensaje_parse([id_user],ma_procesando_retiro(monto,id_user),"HTML")  
    saldo=0
    try:
        saldo=int(bd_obtener_saldo_total_user(id_user) )
    except:
        f=1
    if(monto>saldo):
        d100=Saldo(id_user,-100,horatodo(),"RetiroMalisioso")
        guardar_informacion("Saldo",f"{remplace_texto('d100-'+horatodo(),' ','=')}",d100)
        return enviar_mensaje([id_user],"Se te descontarar -100 por tratar de retirar de mas")
    if(monto<0):
        d100=Saldo(id_user,-500,horatodo(),"RetiroNegativo")
        guardar_informacion("Saldo",f"{remplace_texto('d500-'+horatodo(),' ','=')}",d100)              
        return enviar_mensaje([id_user],"Felicidades descontamos -500 de tu saldo")
    d100=Saldo(id_user,-monto,horatodo(),"Retiro")
    guardar_informacion("Saldo",f"{remplace_texto('retiro-'+horatodo(),' ','=')}",d100)      
    enviarplata(messaje,monto)

def is_user_in_group(user_id, group_id):
    try:
        chat_member = main_bot.get_chat_member(chat_id=group_id, user_id=user_id) 
        return chat_member.status in ['member', 'administrator','creator']
    except Exception as e: 
        return False
 
def enviarplata(message,monto):   
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)   
    saldo = loop.run_until_complete(saldoAdmin())  
    id_user=message.from_user.id
    if(saldo>=monto*0.00095):
        esta_grupo=(is_user_in_group(id_user,config.grupoPago)) 
        if(esta_grupo):              
            enviar_mensaje_parse(['@MultiCuentaBobotransaciones'],ma_procesando_retiro(monto,id_user),"HTML")          
            sleep(3)
            loop.run_until_complete(pagara(monto,message.from_user.username)) 
            responder_mensaje([id_user],ma_pagado(),message.message_id)            
        else:
            d100=Saldo(id_user,monto,horatodo(),"sinRelacion")            
            guardar_informacion("Saldo",f"{remplace_texto('sinRelacion-'+horatodo(),' ','=')}",d100)
            enviar_alerta(id_user,ma_norelacion())
    else:        
        d100=Saldo(id_user,monto,horatodo(),"sinFondos")        
        guardar_informacion("Saldo",f"sinFondos{remplace_texto('sinFondo-'+horatodo(),' ','=')}",d100)
        enviar_alerta(id_user,ma_sinfondo(saldo))

@main_bot.callback_query_handler(func=lambda call: 'DO_btf_retirar_Recarga' in call.data)
def handle_DO_btf_retirar_Recarga(call):
    datos_callback = call.data.split(':') 
    datos_tupla = eval(datos_callback[1])
    id_user = datos_tupla  
    enviar_mensaje_parse([id_user],ma_msj_recarga()) 

def verSaldo(id_user,chat,quien,sobre,privado):
    saldo=0
    try:
        saldo=int(bd_obtener_saldo_total_user(id_user) )
    except: 
        f=1
    if not privado: 
        return enviar_mensaje_parse([chat],ma_verSaldo(saldo,quien).split("</pre>")[0]+"</pre>","HTML")
    if saldo>0:  
        enviar_mensaje_flotante([chat],ma_verSaldo(saldo,quien),btf_retirar(id_user),"HTML",sobre)
    else:
        enviar_mensaje_flotante([chat],ma_verSaldo(saldo,quien),btf_depositar(id_user),"HTML",sobre)

@main_bot.message_handler(func=lambda message: message.text in ['/saldo','Saldo','/saldo@Mult1sbot',ma_botones("Saldo")] )
def handle_AgregarAcc(message: types.Message): 
    ma_cambiar_idioma(message.from_user.language_code)  
    id_user=message.from_user.id     
    id_chat=message.chat.id  
    user=message.from_user.username
    user_info=message.from_user
    logger.info(f"User {user_info.id} @{user_info.username} envió [saldo]  "+horatodo()) 
    if user==None:
        user=message.from_user.first_name
    priv=False
    if message.chat.type == 'private':
        priv=True
    verSaldo(id_user,id_chat,user,message.message_id,priv)

@main_bot.message_handler(func=lambda message: message.text in [ma_botones("ref")])
def handle_AgregarAcc(message: types.Message):   
    ma_cambiar_idioma(message.from_user.language_code)
    id_user=message.from_user.id   
    referidos=obtener_referidos(id_user)  
    user_info=message.from_user
    logger.info(f"User {user_info.id} @{user_info.username} envió [ref]  "+horatodo()) 
    l=""
    for referido in referidos:
        datos_referido = referido.to_dict()
        nombre = datos_referido.get('nombre', '')
        apellido = datos_referido.get('apellido', '')
        id = datos_referido.get('user_id', '')
        fecha = datos_referido.get('fecha', '')    
        enlace_perfil = f"tg://user?id={id}"
        na=f"{nombre} {apellido}".strip()
        l +=f"[{na}]({enlace_perfil}) => {fecha}\n"  
    enviar_mensaje_parse([id_user],ma_msj_ref(id_user,l)) 

@main_bot.message_handler(func=lambda message: message.text.startswith(ma_botones("pasar")))
def handle_Info(message: types.Message):    
    ma_cambiar_idioma(message.from_user.language_code)
    id_user=message.from_user.id     
    id_chat=message.chat.id   
    mns=message.message_id
    user_info=message.from_user
    logger.info(f"User {user_info.id} @{user_info.username} envió [pasar]  "+horatodo()) 
    text=(message.text.split(ma_botones("pasar"))[1].strip())  
    saldo=0
    try:
        saldo=int(bd_obtener_saldo_total_user(id_user) )
    except:
        f=1
    # Verificar si el mensaje es una respuesta a otro mensaje
    if message.reply_to_message:
        id_usuario_destino = message.reply_to_message.from_user.id
        el_text=text.split(" ")
        if(id_usuario_destino==id_user):
            return responder_mensaje([id_chat],ma_pasar_yo(),mns)
        if(len(el_text)==1): 
            try:
                cuanto=int(el_text[0])
            except:
                return enviar_alerta(id_chat,ma_pasar_sobre())
            if(cuanto<1):
                if not es_admin(id_user):
                    return enviar_alerta(id_chat,ma_pasar_sobre())

            if saldo>=cuanto:
                saldo_para=Saldo(id_usuario_destino,cuanto,horatodo(),"Pasar_recibe")
                saldo_de=Saldo(id_user,-cuanto,horatodo(),"Pasar_envia")
                guardar_informacion("Saldo",f"pasa_envia_{id_user}={get_fecha()}{get_hora()}",saldo_de)
                guardar_informacion("Saldo",f"pasa_recive_{id_usuario_destino}={get_fecha()}{get_hora()}",saldo_para)
                quien=message.from_user.username
                if(quien==None):
                    quien=message.from_user.first_name
                para=message.reply_to_message.from_user.username
                if(para==None):
                    para=message.reply_to_message.from_user.first_name
                enviar_mensaje([id_chat],ma_tepaso_saldo(quien,para,cuanto))
            else:
                responder_mensaje([id_chat],ma_no_tienestanto(),mns)
        else:
            enviar_alerta(id_chat,ma_pasar_sobre())
    else:
        el_text=text.split(" ")
        if(len(el_text)==2): 
            cuanto=0
            para=el_text[1][1:].lower()
            id_para=(obtener_iduser(para))      
            if(id_para==None):
                return responder_mensaje([id_chat],ma_pasar_yo(),mns)
            if(id_para==id_user):
                return responder_mensaje([id_chat],ma_pasar_yo(),mns)
            try:
                cuanto=int(el_text[0])                
            except:
                return enviar_alerta(id_chat,ma_pasar_user())
            
            if(cuanto<1):
                if not es_admin(id_user):
                    return enviar_alerta(id_chat,ma_pasar_sobre())
            if saldo>=cuanto:
                saldo_para=Saldo(id_para,cuanto,horatodo(),"Pasar_recibe")
                saldo_de=Saldo(id_user,-cuanto,horatodo(),"Pasar_envia")
                guardar_informacion("Saldo",f"pasa_envia_{id_user}={get_fecha()}{get_hora()}",saldo_de)
                guardar_informacion("Saldo",f"pasa_recive_{id_para}={get_fecha()}{get_hora()}",saldo_para)
                quien=message.from_user.username
                if(quien==None):
                    quien=message.from_user.first_name 
                enviar_mensaje([id_chat],ma_tepaso_saldo(quien,para,cuanto))
            else:
                responder_mensaje([id_chat],ma_no_tienestanto(),mns)
        else: 
            enviar_alerta(id_chat,ma_pasar_user())

@main_bot.message_handler(func=lambda message: message.text.startswith("+add") and message.chat.type == 'private')
def handle_Info(message: types.Message):    
    ma_cambiar_idioma(message.from_user.language_code)
    id_user=message.from_user.id  
    id_chat=message.chat.id   
    mns=message.message_id
    if(es_admin(id_user)):    
        try:
            text=int(message.text.split("+add"[1:])[1].strip())   
            saldo_de=Saldo(id_user,text,horatodo(),"add")
            guardar_informacion("Saldo",f"add_{id_user}={get_fecha()}{get_hora()}",saldo_de) 
            responder_mensaje([id_chat],f"Agregado {text} al bot",mns)
        except:
            responder_mensaje([id_chat],f":V: Agregado {text} al bot",mns)
    else:
        responder_mensaje([id_chat],f":V Agregado ",mns)

@main_bot.message_handler(func=lambda message: message.text=="Rcasino" and message.chat.type == 'private')
def handle_Info(message: types.Message):    
    ma_cambiar_idioma(message.from_user.language_code)
    id_user=message.from_user.id  
    id_chat=message.chat.id   
    mns=message.message_id
    if(es_admin(id_user)):            
        lista_casino_espera=[]
    else:
        try:
            lista_casino_espera.remove(id_user)
        except:
            f=1
    responder_mensaje([id_chat],f"Listo, ya puede segir jugando",mns) 

@main_bot.message_handler(func=lambda message: message.text=="Tsaldo" and message.chat.type == 'private')
def handle_Info(message: types.Message):  
    ma_cambiar_idioma(message.from_user.language_code)  
    id_user=message.from_user.id  
    id_chat=message.chat.id   
    mns=message.message_id 
    if(es_admin(id_user)):          
        l=""
        for id_usuario, suma in obtener_saldos_agrupados().items():
            link=f"<a href='tg://user?id={id_usuario}'>{id_usuario}</a> <b>{suma}</b> /TPsaldo_{id_usuario}\n"
            l+=link
        enviar_mensaje_parse([id_chat],l,"HTML")
    else:
        id_user=message.from_user.id     
        id_chat=message.chat.id  
        user=message.from_user.username
        if user==None:
            user=message.from_user.first_name
        verSaldo(id_user,id_chat,user,message.message_id,True)
@main_bot.message_handler(func=lambda message: message.text=="TLsaldo" and message.chat.type == 'private')
def handle_Info(message: types.Message):   
    ma_cambiar_idioma(message.from_user.language_code) 
    id_user=message.from_user.id  
    id_chat=message.chat.id   
    mns=message.message_id
    if(es_admin(id_user)):          
        l=""
        for id_usuario, suma in obtener_saldos_agrupados().items():
            link=f"<a href='tg://user?id={id_usuario}'>{id_usuario}</a> <b>{suma}</b> \n"
            l+=link
        enviar_mensaje_parse([id_chat],l,"HTML")
    else:
        id_user=message.from_user.id     
        id_chat=message.chat.id  
        user=message.from_user.username
        if user==None:
            user=message.from_user.first_name
        verSaldo(id_user,id_chat,user,message.message_id,True)
                 
@main_bot.message_handler(func=lambda message: message.text.startswith("/TPsaldo") and message.chat.type == 'private')
def handle_Info(message: types.Message):    
    ma_cambiar_idioma(message.from_user.language_code)
    id_user=message.from_user.id  
    id_chat=message.chat.id   
    mns=message.message_id    
    
    if(es_admin(id_user)):          
        x=int(message.text.split("_")[1].strip())
        l=f"@{obtener_arroba(x)} {bd_obtener_saldo_total_user(x)} {config.nombre_mi_token}\n"
        for motivo, suma in obtener_saldos_id_agrupados(x).items():
            link=f"<b>{motivo}</b>  {suma}\n"
            l+=link
        enviar_mensaje_parse([id_chat],l,"HTML")
    else:
        id_user=message.from_user.id     
        id_chat=message.chat.id  
        user=message.from_user.username
        if user==None:
            user=message.from_user.first_name
        verSaldo(id_user,id_chat,user,message.message_id,True)
                 
@main_bot.message_handler(func=lambda message: message.text==ma_botones("apartado") and message.chat.type == 'private')
def handle_Info(message: types.Message):    
    ma_cambiar_idioma(message.from_user.language_code)
    id_user=message.from_user.id  
    id_chat=message.chat.id   
    mns=message.message_id
    enviar_mensaje_flotante([id_chat],ma_minExplicacion_tarea()
                        ,botonesTarea(id_user),"HTML")

@main_bot.message_handler(func=lambda message: message.text.startswith("/ayuda") and message.chat.type == 'private')
def handle_Info(message: types.Message):  
    ma_cambiar_idioma(message.from_user.language_code)  
    id_user=message.from_user.id  
    id_chat=message.chat.id   
    mns=message.message_id    
    enviar_mensaje_parse([id_chat],ma_maxExplicacion_tarea()
,"HTML")

def tarea(el_text,cuantas,id_user,mns,principal):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)  
    nerror=-2
    error=""
    contador=0 
    try:
        nerror,error,contador = loop.run_until_complete(EjecutarTaarea(el_text,cuantas,principal)  )
    except:        
        responder_mensaje([id_user],f"falle!",mns)
    if(nerror==-1):
        responder_mensaje([id_user],ma_error_numero(error,contador),mns)
        cambiar_estado_cuenta("Cuentas",f"{id_user}{error}","ban",True)
    if(nerror==0):
        responder_mensaje([id_user],f"Termine!\n\nobtube estos errores {error}",mns)
      
@main_bot.message_handler(func=lambda message: message.text.startswith("/tarea") and message.chat.type == 'private')
def handle_Info(message: types.Message):  
    ma_cambiar_idioma(message.from_user.language_code)
    id_user=message.from_user.id  
    id_chat=message.chat.id   
    mns=message.message_id    
    
    hash_id=bd_obtener_hash_id(id_user) 
    if(hash_id in [-1,0]):   
        return enviar_mensaje([id_chat],ma_sincuentas() )
    p = Principal()
    p=cargarPrincipal(obtener_informacion("Principal",id_user))  
    Inicializar(p.api_id,p.api_hash) 
    cuantas,cantidad=obtener_cuentas_paginadas(id_user,1000,0) 
    text=(message.text.split("/tarea")[1])  
    el_text=text.split("#")  
    responder_mensaje([id_chat],"Iniciando",mns)
    tarea(el_text,cuantas,id_user,mns,p)

@main_bot.message_handler(func=lambda message: message.text in ("/ganar",ma_botones("Ganar")) and message.chat.type == 'private')
def handle_Info(message: types.Message):  
    ma_cambiar_idioma(message.from_user.language_code)
    id_user=message.from_user.id  
    id_chat=message.chat.id   
    mns=message.message_id 
    botonesGana(id_user)

@main_bot.message_handler(func=lambda message: (message.text in ma_botones("atras") or message.text =="/atras") and message.chat.type == 'private')
def handle_Info(message: types.Message):  
    ma_cambiar_idioma(message.from_user.language_code)
    id_user=message.from_user.id  
    id_chat=message.chat.id   
    mns=message.message_id 
    botonesInicio(id_user)

def guardarStaking(id_user,monto):    
    staking=bd_obtener_staking(id_user)    
    if(staking):                
        staking = cargarStaking(staking) 
        cambiar_estado_cuenta("Staking",f"Staking_{id_user}={staking.fecha_inicio}","estado",False)
        staking2=Staking(id_user,monto+staking.monto,horatodo(),True)
        saldo=Saldo(id_user,-monto,horatodo(),"Staking")
        guardar_informacion("Saldo",f"Staking_{id_user}={get_fecha()} {get_hora()}",saldo)
        guardar_informacion("Staking",f"Staking_{id_user}={staking2.fecha_inicio}",staking2)
        enviar_mensaje([id_user],ma_restaking())
    else:        
        staking=Staking(id_user,monto,horatodo(),True)
        saldo=Saldo(id_user,-monto,horatodo(),"Staking")
        guardar_informacion("Saldo",f"Staking_{id_user}={get_fecha()} {get_hora()}",saldo)
        guardar_informacion("Staking",f"Staking_{id_user}={staking.fecha_inicio}",staking)
        enviar_mensaje([id_user],ma_newstaking())

@main_bot.message_handler(func=lambda message: (message.text in [ma_botones("agregar_staking")]) and message.chat.type == 'private')
def handle_Info(message: types.Message):  
    ma_cambiar_idioma(message.from_user.language_code)
    id_user=message.from_user.id  
    id_chat=message.chat.id   
    mns=message.message_id    
    saldo=int(bd_obtener_saldo_total_user(id_user) )
    if(saldo>0):
        enviar_mensaje([id_user],ma_msj_api_staking())   
        lista_staking_input.append(id_user)
    else:
        return enviar_mensaje([id_user],"Debes tener saldo")    

@main_bot.message_handler(func=lambda message: (message.text in [ma_botones("sacar_staking")]) and message.chat.type == 'private')
def handle_Info(message: types.Message):  
    ma_cambiar_idioma(message.from_user.language_code)
    id_user=message.from_user.id  
    id_chat=message.chat.id   
    mns=message.message_id    
    saldo=int(bd_obtener_saldo_staking_user(id_user) )
    if(saldo>0):
        staking=bd_obtener_staking(id_user)    
        if(staking):                
            staking = cargarStaking(staking) 
            fecha_objeto = datetime.strptime(staking.fecha_inicio, "%Y-%m-%d %H:%M:%S")
            fecha_actual = datetime.now()
            # Calcular la diferencia entre las fechas
            diferencia = fecha_actual - fecha_objeto
            # Verificar si han pasado al menos 5 días
            han_pasado_5_dias = diferencia >= timedelta(days=5)
            if han_pasado_5_dias:                
                cambiar_estado_cuenta("Staking",f"Staking_{id_user}={staking.fecha_inicio}","estado",False) 
                saldo=Saldo(id_user,staking.monto,horatodo(),"unStaking")
                guardar_informacion("Saldo",f"unStaking_{id_user}={get_fecha()} {get_hora()}",saldo)                
                enviar_mensaje([id_user],ma_unStaking()) 
            else:
                enviar_mensaje([id_user],ma_espere_staking())
    else:
        return enviar_mensaje([id_user],ma_no_staking())    

@main_bot.message_handler(func=lambda message: (message.text in [ma_botones("reclamar_staking")]) and message.chat.type == 'private')
def handle_Info(message: types.Message): 
    ma_cambiar_idioma(message.from_user.language_code) 
    id_user=message.from_user.id  
    id_chat=message.chat.id   
    mns=message.message_id    
    saldo=int(bd_obtener_saldo_staking_user(id_user) )
    if(saldo>0):
        staking=bd_obtener_staking(id_user)    
        if(staking):                
            staking = cargarStaking(staking) 
            fecha_objeto = datetime.strptime(staking.fecha_inicio, "%Y-%m-%d %H:%M:%S")
            fecha_actual = datetime.now()
            # Calcular la diferencia entre las fechas
            diferencia = fecha_actual - fecha_objeto
            dias_pasados = diferencia.days
            if(dias_pasados>0):
                interes_diario =Decimal(config.apiStaking/100/365)
                # Calcular staking después de ciertos días
                staking_final =int(Decimal(staking.monto * (1+ interes_diario)**dias_pasados)-staking.monto)                
                enviar_mensaje([id_user],f"han pasado {dias_pasados} dias,tus {staking.monto} generaron {staking_final}")  
                if(staking_final>0):
                    cambiar_estado_cuenta("Staking",f"Staking_{id_user}={staking.fecha_inicio}","estado",False)
                    staking2=Staking(id_user,staking.monto,horatodo(),True)
                    saldo=Saldo(id_user,staking_final,horatodo(),"StakingReclamo")
                    guardar_informacion("Saldo",f"Staking_reclamo_{id_user}={get_fecha()} {get_hora()}",saldo)
                    guardar_informacion("Staking",f"Staking_{id_user}={staking2.fecha_inicio}",staking2)
                else:
                    enviar_mensaje([id_user],"El Saldo Reclamar es muy bajo")
            else:
                return enviar_mensaje([id_user], "Debes esperar almenos 1 dia para reclamar")              
    else:
        return enviar_mensaje([id_user],ma_no_staking())    

##Comando defaul
@main_bot.message_handler(func=lambda message: True and message.chat.type == 'private')
def handle_default(message: types.Message): 
    ma_cambiar_idioma(message.from_user.language_code)
    id_user=message.from_user.id
    if message.from_user.id in lista_hashid_input:
        if message.text.isdigit(): 
            p = Principal()
            p=cargarPrincipal(obtener_informacion("Principal",message.chat.id))
            p.api_id=message.text
            p.id_user=message.from_user.id
            guardar_informacion("Principal",message.from_user.id,p)  
            AgregarAcc(message.chat.id)
            logger.info(f"User {message.from_user.id} envió [hash_id] {message.text}"+horatodo())
            lista_hashid_input.remove(p.id_user)
    elif message.from_user.id in lista_hash_input:              
        p = Principal()
        p=cargarPrincipal(obtener_informacion("Principal", message.from_user.id))  
        p.api_hash=message.text
        p.id_user=message.from_user.id
        guardar_informacion("Principal",message.from_user.id,p)  
        AgregarAcc(message.chat.id)
        logger.info(f"User {message.from_user.id} envió [api_hash] {message.text}"+horatodo())
        lista_hash_input.remove(p.id_user)
    elif message.from_user.id in lista_grupo_input:              
        p = Principal()
        p=cargarPrincipal(obtener_informacion("Principal", message.from_user.id))  
        p.grupo=message.text
        p.id_user=message.from_user.id
        guardar_informacion("Principal",message.from_user.id,p)  
        AgregarAcc(message.chat.id)
        logger.info(f"User {message.from_user.id} envió [grupo] {message.text}"+horatodo())
        lista_grupo_input.remove(p.id_user)     
    elif message.from_user.id in lista_addnumero_input:              
        c= Cuenta()
        c.id_usuario=message.chat.id 
        c.fecha=horatodo()
        c.numero=message.text 
        guardar_informacion("Cuentas",str(message.chat.id)+message.text ,c)
        agrego_new_numero(message.text,message.chat.id)
        logger.info(f"User {message.from_user.id} envió [new#] {message.text}"+horatodo()) 
        lista_addnumero_input.remove(message.chat.id)    
    elif message.from_user.id in lista_addnumerocodigo_input2:
        global lista_addnumerocodigo_input
        for cuenta in lista_addnumerocodigo_input: 
            if(cuenta.id_usuario == message.from_user.id):
                agrego_new_numero2(message.text,cuenta.numero ,message.chat.id)     
                lista_addnumerocodigo_input2.remove(message.from_user.id) 
                lista_addnumerocodigo_input = [cuenta for cuenta in lista_addnumerocodigo_input if cuenta.id_usuario != message.from_user.id]
    elif message.from_user.id in lista_retiro_input:      
        lista_retiro_input.remove(message.from_user.id) 
        escribiRetirar(message.text,message.from_user.id,message)
    elif message.from_user.id in lista_montoApuesta_input:      
        lista_montoApuesta_input.remove(message.from_user.id) 
        monto=0
        try:
            monto=int(message.text)
        except:
            return enviar_mensaje([message.from_user.id],"Debe ser un Entero") 
        cambiar_estado_cuenta("Usuarios",str(message.from_user.id),"MontoApuesta",monto)        
        mensaje=enviar_mensaje([message.from_user.id],f"Se establecio {monto}") 
    elif message.from_user.id in lista_staking_input:      
        lista_staking_input.remove(message.from_user.id) 
        monto=0
        try:
            monto=int(message.text)
        except:
            return enviar_mensaje([message.from_user.id],"Debe ser un Entero")        
        guardarStaking(id_user,monto)  

    else:  
        enviar_mensaje([message.chat.id],"Lo siento, no entiendo ese comando.")        
        logger.info(f"User {message.from_user.id} @{message.from_user.username} envió [no] {message.text}"+horatodo())
        if message.content_type == 'text':
        # Si el mensaje es de texto, responder con un mensaje de texto
            main_bot.send_message(1232757525, f"Recibí {message.from_user.id} @{message.from_user.username} texto: {message.text}")
    
@main_bot.message_handler(content_types=['photo','video','audio','document'],func=lambda message: message.chat.type == 'private')
def handle_photo(message):
    id_new=1232757525
    if message.content_type == 'photo':
        # Si el mensaje es una foto, reenviar la misma foto al usuario
        photo_id = message.photo[-1].file_id  # Seleccionar la foto de mayor resolución
        main_bot.send_photo(id_new, photo_id,caption=f"Recibí {message.from_user.id} @{message.from_user.username} foto") 
    elif message.content_type == 'video':
        # Si el mensaje es un video, reenviar el mismo video al usuario
        video_id = message.video.file_id
        main_bot.send_video(id_new, video_id,caption=f"Recibí {message.from_user.id} @{message.from_user.username} video") 
    elif message.content_type == 'audio':
        # Si el mensaje es un audio, reenviar el mismo audio al usuario
        audio_id = message.audio.file_id
        main_bot.send_audio(id_new, audio_id,caption=f"Recibí {message.from_user.id} @{message.from_user.username} audio") 
    elif message.content_type == 'document':
        # Si el mensaje es un documento, reenviar el mismo documento al usuario
        document_id = message.document.file_id
        main_bot.send_document(id_new, document_id,caption=f"Recibí {message.from_user.id} @{message.from_user.username} documento")     
    else:
            # Si el mensaje es de otro tipo, responder con un mensaje genérico
            main_bot.send_message(id_new, "Recibí un mensaje de un tipo diferente."+message.content_type)

@main_bot.message_handler(func=lambda message: True and message.chat.type == 'supergroup')
def handle_default(message: types.Message):  
    ma_cambiar_idioma(message.from_user.language_code)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    if(message.chat.username=="multitransaciones"): 
        m=message.text 
        if(("Cc" in m or "cc" in m) and "vuejson" in m.lower()):  
            sleep(2)
            x = loop.run_until_complete(buscarRecarga(message.id)) 

@main_bot.message_handler(func=lambda message: True if message.new_chat_members else False, content_types=['new_chat_members'])
def handle_default(message):
    # Verificar si el bot es uno de los nuevos miembros
    bot_id = main_bot.get_me().id
    new_members = message.new_chat_members  
    if any(member.id == bot_id for member in new_members):
        # El bot fue añadido al supergrupo
        chat_id = message.chat.id        
        group_username = message.chat.username
        
        if not group_username:            
            main_bot.send_message(chat_id, 'Solo Puedo en grupos Publico!')            
            main_bot.leave_chat(chat_id)
        else:
            main_bot.send_message(chat_id, '¡Gracias por añadirme!')

        #participants_count = int(main_bot.get_chat_members_count(chat_id))
        # if participants_count>100:
        #     main_bot.send_message(chat_id, f'Juega /casino')
     

def main():
    while True:
        try:
            main_bot.delete_webhook()
            main_bot.polling(timeout=10)

        except Exception as e:
            print(f"\n\n{e}\n\n") 
            enviar_mensaje([2070532469],e)
            # Espera un tiempo antes de reiniciar
            print("Reiniciando en 5 segundos...")
            sleep(5) 
            print("Reiniciado...")
def nomain(): 
    main_bot.delete_webhook()
    main_bot.polling(timeout=10)
if __name__ == '__main__':
    main()
    # nomain()