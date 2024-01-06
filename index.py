import config,re,logging, threading,requests,asyncio
from flask import Flask, request, abort
from telebot import TeleBot, types, util
from telegram import KeyboardButton, ReplyKeyboardMarkup
from datetime import datetime
from modelo.user import Cuenta, Principal, Usuario
from modelo.mensajesAlmacenados import *
from codigo import Inicializar, Logear_a, Logear_ab, validarcuenta
from bd import *
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
    # Define tus estilos aquí

    # - Negrita: <b>texto en negrita</b>, <strong>negrita</strong>
    # - Cursiva: <i>texto en cursiva</i>, <em>cursiva</em>
    # - Subrayado: <u>texto subrayado</u>, <ins>subrayado</ins>
    # - Tachado: <s>texto tachado</s>, <strike>tachado</strike>, <del>tachado</del> 
    # <a href="tg://user?id=123456789">inline mention of a user</a>
    # - Código: <code>texto con el código</code>
    # - Indica a la API que debe respetar los saltos de línea y los espacios en blanco: <pre>Texto con saltos de línea y espacios</pre>
    

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
    for usuario_id in lista_ids:
        try:
            main_bot.send_message(usuario_id, mensaje) 
        except Exception as e:
            # Manejar otras excepciones no previstas
            print(f"Error desconocido al enviar mensaje a usuario {usuario_id} ")
    
def enviar_alerta(usuario_id, mensaje,parse_mode="NO",minutos=3):
    # Crear un mensaje con teclado en línea vacío
    markup = types.InlineKeyboardMarkup()
    
    # Crear un botón "Cerrar" que no realiza ninguna acción
    btn_cerrar = types.InlineKeyboardButton("Cerrar", callback_data='cerrar_alerta')
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
    except Exception  as x :
        print(f"Error al manejar la acción del botón flotante[DO_Agregar_Api]:  {x}")

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
    except Exception  as x :
        print(f"Error al manejar la acción del botón flotante[DO_Agregar_grupo]:  {x}")

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
    except Exception  as x :
        print(f"Error al manejar la acción del botón flotante[DO_disponible]:  {x}")

@main_bot.callback_query_handler(func=lambda call: 'DO_Agregar_Numero' in call.data)
def handle_btf_DO_Agregar_Numero(call):
    try:        
        id_user = int(call.data.split(":")[1])
        main_bot.delete_message(id_user, call.message.message_id)         
        mensaje_para_borrar=main_bot.send_message(id_user, "_Validando Api_",reply_markup=
        crear_linea_fboton("::[Espere por favor]"),parse_mode="Markdown")
        main_bot.delete_message(id_user, mensaje_para_borrar.message_id)         
        mensaje_para_borrar=main_bot.send_message(id_user, 
            "Ejemplo de numero Celular +573001112233\nDonde +57 es el *indicativo* del pais\n*Envie el Numero*",
            reply_markup= crear_linea_fboton("Envie numero celular"),parse_mode="Markdown")
        lista_addnumero_input.append(id_user)
        minutos=3
        threading.Timer(minutos*60, cerrar_alerta_auto, args=[id_user,mensaje_para_borrar]).start()


        logger.info(f"User {id_user} envió [DO_Agregar_Numero]  "+horatodo()) 
    except Exception  as x :
        print(f"Error al manejar la acción del botón flotante[DO_Agregar_Numero]:  {x}")


def btf_apihash_nuevo(id_user):  
    keyboard = types.InlineKeyboardMarkup() 
    fila = [
        types.InlineKeyboardButton(text="Agregar Api_Id" , callback_data=f'DO_Agregar_Api_id:{id_user}'),
        types.InlineKeyboardButton(text="Agregar Api_Hash" , callback_data=f'DO_Agregar_Api:{id_user}') ] 
    keyboard.add(*fila) 
    return keyboard

def btf_apihash(id_user):  
    keyboard = types.InlineKeyboardMarkup() 
    fila = [
        types.InlineKeyboardButton(text="Agregar Api_Id" , callback_data=f'DO_Agregar_Api_id:{id_user}'),
        types.InlineKeyboardButton(text="Agregar Api_Hash" , callback_data=f'DO_Agregar_Api:{id_user}') 
        ] 
    
    fila1 = [
        types.InlineKeyboardButton(text="Agregar Tu Grupo" , callback_data=f'DO_Agregar_grupo:{id_user}'),
        types.InlineKeyboardButton(text="Disponible" , callback_data=f'DO_disponible:{id_user}') 
        ] 
    fila2=[
         types.InlineKeyboardButton(text="Agregar Numero" , callback_data=f'DO_Agregar_Numero:{id_user}') 
    ]
    keyboard.add(*fila)     
    keyboard.add(*fila1)     
    keyboard.add(*fila2)     
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
            enviar_mensaje([user_id_referente], f"Invitaste a @{user_info.username}")  
            ##BONO? 
        enlace_perfil = f"tg://user?id={user_id_referente}"
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

@main_bot.message_handler(func=lambda message: message.text in ['/'+ma_botones("add_cuenta"),ma_botones("add_cuenta")])
def handle_AgregarAcc(message: types.Message):   
    AgregarAcc(message.chat.id)

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

def agrego_new_numero(nemeri_texto,id_user):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    x=0
    try:
        mensaje_para_borrar=main_bot.send_message(id_user, "_Validando Numero_",reply_markup=
        crear_linea_fboton(nemeri_texto),parse_mode="Markdown")
        p = Principal()
        p=cargarPrincipal(obtener_informacion("Principal",id_user))  
        Inicializar(p.api_id,p.api_hash) 
        x = loop.run_until_complete(Logear_a(nemeri_texto)) 

        cerrar_alerta_auto(id_user,mensaje_para_borrar)
        if(x==-1):
            main_bot.send_message(id_user, "No se pudo Validar el numero",reply_markup=
                crear_linea_fboton(nemeri_texto),parse_mode="Markdown") 
        if(x==0):
            x=Cuenta(id_user,nemeri_texto) 
            lista_addnumerocodigo_input.append(x)
            lista_addnumerocodigo_input2.append(id_user)
            main_bot.send_message(id_user, "Se envio un Codigo a: ",reply_markup=
                crear_linea_fboton(nemeri_texto),parse_mode="Markdown") 
        if(x==1):
            mens=main_bot.send_message(id_user, "Numero Ok.",reply_markup=
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
        mensaje_para_borrar=main_bot.send_message(id_user, "_Validando Codigo_",reply_markup=
        crear_linea_fboton(nemeri_texto),parse_mode="Markdown")
        p = Principal()
        p=cargarPrincipal(obtener_informacion("Principal",id_user))  
        Inicializar(p.api_id,p.api_hash) 
        x = loop.run_until_complete(Logear_ab(nemeri_texto,cod_texto)) 
        cerrar_alerta_auto(id_user,mensaje_para_borrar)
        if(x==-1):
            main_bot.send_message(id_user, "No se pudo Validar el numero",reply_markup=
                crear_linea_fboton(nemeri_texto),parse_mode="Markdown") 
        if(x==0): 
            mens=main_bot.send_message(id_user, "Numero Ok.",reply_markup=
                crear_linea_fboton(nemeri_texto),parse_mode="Markdown") 
            borrarultimosmenaje( mens.message_id,id_user,5)
        if(x==1):
            mens=main_bot.send_message(id_user, "Numero Ok",reply_markup=
                crear_linea_fboton(nemeri_texto),parse_mode="Markdown")            
            borrarultimosmenaje( mens.message_id,id_user,3)
    except Exception as inst:
        print(inst)
        x=-2  

def DO_ListarCuenta_validarAll(id_user):
    f=1
def listarCuentaBotoflotante():
    f=1
 
@main_bot.callback_query_handler(func=lambda call: 'DO_ActivarNumero' in call.data)
def handle_btf_DO_ActivarNumero(call):    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    datos_callback = call.data.split(':') 
    datos_tupla = eval(datos_callback[1])
    numero, id_user = datos_tupla 
    mensaje= main_bot.send_message(id_user, f"Buscando la informacion de [{numero}]")
    cuenta=Cuenta()
    cuenta=obtener_informacion("Cuentas",f"{id_user}{numero}")
    p = Principal()
    p=cargarPrincipal(obtener_informacion("Principal",id_user))  
    cerrar_alerta_auto(id_user,mensaje.message_id)
    enviar_alerta(id_user, f"Validando Tu Api Tg [{p.api_id}]:[{aplicar_estilo('**'+p.api_hash[2:-3]+'***','ta')}]","HTML",5)
    Inicializar(p.api_id,p.api_hash)
    try:
        x,y = loop.run_until_complete(validarcuenta(numero,[p.grupo,"BotColombia"]))
        print(x,y)
    except Exception as cx:
        print("erroe\n",cx,"f\n")
    print("ya")
    

@main_bot.callback_query_handler(func=lambda call: 'DO_ln_VerNumero' in call.data)
def handle_btf_DO_ln_VerNumero(call):
    datos_callback = call.data.split(':') 
    datos_tupla = eval(datos_callback[1])
    numero, id_user = datos_tupla 
    mensaje= main_bot.send_message(id_user, f"Buscando la informacion de [{numero}]")
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



def ListarCuenta(cuantas,index,id_user):     
    l_numeros,cuantes_cuentas=obtener_cuentas_paginadas(id_user,cuantas,index) 
    keyboard = types.InlineKeyboardMarkup() 
    mensaje=0    
    f= [
        types.InlineKeyboardButton(text="Regresar" , callback_data=f'DO_:{id_user}'),
        types.InlineKeyboardButton(text=f"{(index)+1} de {round(cuantes_cuentas/cuantas)}" , callback_data=f'DO_:{id_user}') ,
         ]          
    i= [        
        types.InlineKeyboardButton(text=f"{(index)+1} de {round(cuantes_cuentas/cuantas)}" , callback_data=f'DO_:{id_user}') ,
        types.InlineKeyboardButton(text="Sigiente" , callback_data=f'DO_:{id_user}')
        ]           
    m= [                
        types.InlineKeyboardButton(text="Regresar" , callback_data=f'DO_:{id_user}'),
        types.InlineKeyboardButton(text=f"{(index)+1} de {round(cuantes_cuentas/cuantas)}" , callback_data=f'DO_:{id_user}') ,
        types.InlineKeyboardButton(text="Sigiente" , callback_data=f'DO_:{id_user}')
        ]                 
    if(cuantes_cuentas==0 ):
        if index!=0:            
            keyboard.add(*f)
        else:
            enviar_mensaje([id_user],"Sin Numero Regitrados") 
    else:
        ff= [
                types.InlineKeyboardButton(text="    Numeros    ", callback_data=f'DO_ListarCuenta_validarAll:{id_user}' ),
                types.InlineKeyboardButton(text="Estado" , callback_data=f'DO_:{id_user}'),
                types.InlineKeyboardButton(text="Borrar" , callback_data=f'DO_:{id_user}')
        ] 
        keyboard.add(*ff)
        for l_numero in l_numeros: 
            numero = l_numero.get('numero')  
            estado = l_numero.get('estado')
            ban = l_numero.get('ban')
            if ban != True:
                e = "Activar" if not estado else "Desactivar" 
                ff= [
                    types.InlineKeyboardButton(text=numero, callback_data=f'DO_ln_VerNumero:{numero,id_user}'),
                    types.InlineKeyboardButton(text=e, callback_data=f'DO_ActivarNumero:{numero,id_user}'),
                    types.InlineKeyboardButton(text="Borrar" , callback_data=f'DO_:{id_user}')
                ] 
                keyboard.add(*ff)
            
          
        keyboard.add(*f)

        mensaje= main_bot.send_message(id_user, f"Aqui las lista de tus cuentas [{cuantes_cuentas}]",reply_markup=
            keyboard,
            parse_mode="Markdown") 
        borrar_mensaje_en(5,id_user,mensaje)


@main_bot.message_handler(func=lambda message: message.text in ['/'+ma_botones("lista_cuanta"),ma_botones("lista_cuanta")])
def handle_AgregarAcc(message: types.Message):   
    id_user=message.from_user.id
    mensaje=0    
    l=[]
    hash_id=bd_obtener_hash_id(id_user) 
    if(hash_id in [-1,0]):  
        mensaje=main_bot.send_message(id_user, ma_falta_hash(),parse_mode='Markdown',reply_markup=btf_apihash_nuevo(id_user))
        borrar_mensaje_en(3,id_user,mensaje)
    else:   
        ListarCuenta(5,0,id_user)
    
##Comando defaul
@main_bot.message_handler(func=lambda message: True)
def handle_default(message: types.Message): 
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
      

    else:
        main_bot.send_message(message.chat.id, "Lo siento, no entiendo ese comando.")
        logger.info(f"User {message.from_user.id} envió [no] {message.text}"+horatodo())

if __name__ == '__main__':  
    main_bot.delete_webhook()
    main_bot.polling()
