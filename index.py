from flask import Flask, request, abort
from telebot import TeleBot, types, util
import config,re,logging, threading,requests
from datetime import datetime
from modelo.user import Principal, Usuario
from modelo.mensajesAlmacenados import *
from bd import bd_contar_disponibles, bd_obtener_hash, bd_obtener_hash_id, bd_obtener_id_users_principales, bd_obtener_saldo_total, inicializar_firebase, guardar_informacion, obtener_ids, obtener_informacion, saber_admin
# Inicializar Firebase
inicializar_firebase()



app = Flask(__name__)
main_bot = TeleBot(config.MAIN_BOT_TOKEN)
tokens = {config.MAIN_BOT_TOKEN: True}
lista_hashid_input=[]
lista_hash_input=[]
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
    for usuario_id in lista_ids:
        try:
            main_bot.send_message(usuario_id, mensaje) 
        except Exception as e:
            # Manejar otras excepciones no previstas
            print(f"Error desconocido al enviar mensaje a usuario {usuario_id} ")
    
def enviar_alerta(usuario_id, mensaje):
    # Crear un mensaje con teclado en línea vacío
    markup = types.InlineKeyboardMarkup()
    
    # Crear un botón "Cerrar" que no realiza ninguna acción
    btn_cerrar = types.InlineKeyboardButton("Cerrar", callback_data='cerrar_alerta')
    markup.add(btn_cerrar)

    # Enviar el mensaje con el teclado en línea
    mensaje_enviado = main_bot.send_message(usuario_id, mensaje, reply_markup=markup)

    # Configurar el temporizador para cerrar el mensaje después de 3 minutos
    minutos=3
    threading.Timer(minutos*60, cerrar_alerta_auto, args=[mensaje_enviado.chat.id, mensaje_enviado.message_id]).start()

# Función para cerrar automáticamente el mensaje
def cerrar_alerta_auto(chat_id, message_id):
    try:
        main_bot.delete_message(chat_id, message_id)
    except:
        f=1

# Manejar la acción de cerrar alerta
@main_bot.callback_query_handler(func=lambda call: call.data == 'cerrar_alerta')
def cerrar_alerta_callback(query):
    # Eliminar el mensaje original con el teclado en línea
    try:
        main_bot.delete_message(query.message.chat.id, query.message.message_id)
    except:
        f=1

def botonesInicio(id):
    main_bot.send_message(id, "Mira Nuestro Menu", 
        reply_markup=crear_linea_boton(["Agregar Cuenta;Listar Cuenta","Saldo;Referidos","Casino;"+ma_botones("Info")] ))

def lanzar_dado(chat_id):
    url = f"https://api.telegram.org/bot{config.MAIN_BOT_TOKEN}/sendDice"
    params = {"chat_id": chat_id}
    response = requests.get(url, params=params)
    json_data = response.json()

    if 'ok' in json_data and json_data['ok']:
        dice_value = json_data.get('result', {}).get('dice', {}).get('value')
        if dice_value:
            main_bot.send_message(chat_id, dice_value)
        else:
            main_bot.send_message(chat_id, "No se pudo obtener el valor del dado.")
    else:
        main_bot.send_message(chat_id, "Lo sentimos, su Telegram no soporta el comando :dado.")

def btf_texto_dado():  
    keyboard = types.InlineKeyboardMarkup() 
    fila = [types.InlineKeyboardButton(text="Cambiar Monto Apuesta"   
    , callback_data=f'apuesta_cambiar_monto') ]
    keyboard.add(*fila)     

    return keyboard

# Manejar la acción del botón flotante
@main_bot.callback_query_handler(func=lambda call: 'DO_Agregar_Api_id' in call.data)
def handle_btf_apihash_nuevo(call):
    try:
        main_bot.delete_message(call.message.chat.id, call.message.message_id)
        # Obtener el id_user del callback_data
        id_user = int(call.data.split(":")[1])
        # Llamar a la función con el id_user
        DO_Agregar_Api_id(id_user)
    except Exception  :
        print(f"Error al manejar la acción del botón flotante:  ")

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
    except Exception  :
        print(f"Error al manejar la acción del botón flotante:  ")

def DO_Agregar_Api(id_user):
    main_bot.send_message(id_user, ma_envia_hash_id(), parse_mode="Markdown") 
    lista_hashid_input.append(id_user)

def btf_apihash_nuevo(id_user):  
    keyboard = types.InlineKeyboardMarkup() 
    fila = [
        types.InlineKeyboardButton(text="Agregar Api_Id" , callback_data=f'DO_Agregar_Api_id:{id_user}'),
        types.InlineKeyboardButton(text="Agregar Api_Hash" , callback_data=f'DO_Agregar_Api:{id_user}') ] 
    keyboard.add(*fila)     

    return keyboard


@app.route(f"/{config.WEBHOOK_PATH}/<token>", methods=['POST'])
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

@main_bot.message_handler(commands=['start'])
def handle_start(message: types.Message):
    user_id_referente = message.text.split(' ')[1] if len(message.text.split(' ')) > 1 else None
    user_info = message.from_user

    us = Usuario(
        nombre=user_info.first_name,
        apellidos=user_info.last_name,
        user=user_info.username,
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
        if(message.from_user.id!=user_id_referente ):
            us.ref_id=user_id_referente 
            main_bot.send_message(user_id_referente, f"Invitaste a @{user_info.username}")  
            ##BONO?
        enlace_perfil = f"tg://openmessage?user_id={user_id_referente}"
        mensaje = f"¡Hola! \nInvitado por [{user_id_referente}]({enlace_perfil})."
        main_bot.send_message(message.chat.id, mensaje, parse_mode="Markdown") 
        logger.info(f"User {message.from_user.id} envió /hola "+user_id_referente+horatodo())        
        guardar_informacion("Usuarios",us.user_id,us)
        enviar_alerta(message.chat.id,ma_enviarmensaje_Nuevo())
    else:
        main_bot.send_message(message.chat.id, "¡Hola!:")  
        logger.info(f"User {message.from_user.id} envió /hola"+horatodo())
    botonesInicio(message.chat.id)

@main_bot.message_handler(commands=['hora'])
def handle_start(message: types.Message):    
    main_bot.send_message(message.chat.id, "¡Hora!:", reply_markup=crear_linea_fboton([remplace_texto(get_fecha(),"-",";"),remplace_texto(get_hora(),":",";")] ))
    logger.info(f"User {message.from_user.id} envió /hora"+horatodo())

@main_bot.message_handler(commands=['mensajem'])
def handle_mensaje(message: types.Message):    
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
            enviar_mensaje(obtener_ids(), {' '.join(map(str, args))})
            main_bot.send_message(message.chat.id, "Mensaje enviado a todos")
    else:
        main_bot.send_message(message.chat.id, f"Formato de comando no válido. Uso: `/mensajem id1,id2;@ mensaje alv`",parse_mode="Markdown")

@main_bot.message_handler(func=lambda message: message.text in ['/'+ma_botones("Info"),ma_botones("Info")])
def handle_Info(message: types.Message):    
    idl=bd_obtener_id_users_principales()
    enviar_alerta(message.chat.id,ma_enviarmensaje_info(len(idl),bd_contar_disponibles(idl),bd_obtener_saldo_total()))
    logger.info(f"User {message.from_user.id} envió /info "+horatodo())

@main_bot.message_handler(func=lambda message: message.text in ['/'+ma_botones("Casino"),ma_botones("Casino")])#incompleto
def handle_Info(message: types.Message):   
    #lanzar_dado(message.chat.id) 
    monto_user_id=0#??
    main_bot.send_message(message.chat.id, ma_texto_de_apuesta(monto_user_id), reply_markup=btf_texto_dado())
    logger.info(f"User {message.from_user.id} envió /casino "+horatodo())

def AgregarAcc(message):
    mensaje=0
    hash_id=bd_obtener_hash_id(message.chat.id)
    hash=bd_obtener_hash(message.chat.id)
    if(hash_id in [-1,0] or True):  
        mensaje=main_bot.send_message(message.chat.id, ma_falta_hash(),parse_mode='Markdown',reply_markup=btf_apihash_nuevo(message.chat.id))
    else: 
        mensaje=main_bot.send_message(message.chat.id, ma_no_falta_hash(hash_id,hash),parse_mode='Markdown',reply_markup=crear_linea_fboton(["Agregar API_ID;Agregar API_HASH","Agregar Numero"]))
    minutos=5
    threading.Timer(minutos*60, cerrar_alerta_auto, args=[mensaje.chat.id,mensaje]).start()

@main_bot.message_handler(func=lambda message: message.text in ['/'+ma_botones("add_cuenta"),ma_botones("add_cuenta")])
def handle_AgregarAcc(message: types.Message):   
    AgregarAcc(message)

##Comando defaul
@main_bot.message_handler(func=lambda message: True)
def handle_default(message: types.Message):    
    p=Principal()
    if message.from_user.id in lista_hashid_input:
        if message.text.isdigit(): 
            p.api_id=message.text
            p.id_user=message.from_user.id
            guardar_informacion("Principal",message.from_user.id,p)  
            AgregarAcc(message)
            logger.info(f"User {message.from_user.id} envió [no] {message.text}"+horatodo())
    elif message.from_user.id in lista_hash_input:
        f=2
    else:
        main_bot.send_message(message.chat.id, "Lo siento, no entiendo ese comando.")
        logger.info(f"User {message.from_user.id} envió [no] {message.text}"+horatodo())


if __name__ == '__main__':
    main_bot.delete_webhook()
    main_bot.polling()

