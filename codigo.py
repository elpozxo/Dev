import requests, json, re, sys, os,colorama,asyncio
from telethon import TelegramClient, sync, events, functions, types
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import (
    GetHistoryRequest,
    GetBotCallbackAnswerRequest,
)
from telethon.tl.types import  InputPeerEmpty
from telethon.tl.functions.account import ReportPeerRequest
from telethon.errors import SessionPasswordNeededError
from time import sleep
from colorama import Fore, Back, Style
from datetime import datetime
from decimal import Decimal 
from random import choice
from string import ascii_lowercase


api_id=''
api_hash=''

def Inicializar(id,hash):
    global api_id, api_hash  # Declarar como globales
    api_hash=hash
    api_id=id


def clickBotonera(client, channel_username, message_history, columna, fila):
    sleep(1)
    channel_id = message_history.messages[0].id
    client(
        GetBotCallbackAnswerRequest(
            channel_username,
            channel_id,
            data=message_history.messages[0]
            .reply_markup.rows[columna]
            .buttons[fila]
            .data,
        )
    )
    sleep(1)

def clickBotonera2(client, channel_username, message_history, columna, fila):
    sleep(1)
    channel_id = message_history.messages[0].id
    client(
        GetBotCallbackAnswerRequest(
            channel_username,
            channel_id,
            data=message_history.messages[0]
            .reply_markup.rows[columna]
            .buttons[fila]
            .data,
        )
    )
    sleep(1)

async def MensajePlano(mensaje, bot, client):
    await client.send_message(entity=bot, message=mensaje)

def MensajeResponder(mensaje,botOcanal,client,reply):
    client.send_message(entity=botOcanal,message=mensaje, reply_to=reply)

def MensajeFoto(mensaje, bot, client):
    client.send_file(entity=bot, file=mensaje)

def UltimoMensaje(client, channel_entity):
    return client(
        GetHistoryRequest(
            peer=channel_entity,
            limit=1,
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0,
        )
    )

def UltimoMensaje2(client, channel_entity):
    return client(
        GetHistoryRequest(
            peer=channel_entity,
            limit=2,
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0,
        )
    )

def mensaje2(mensaje, a, aa, b, bb):
    return mensaje.messages[0].message.split(a)[aa].split(b)[bb]

def mensaje(mensaje, a, aa):
    return mensaje.messages[0].message.split(a)[aa]


async def Logear_a(phone_number):
    if not os.path.exists("session"):
        os.makedirs("session")
    client = TelegramClient("session/" + phone_number, api_id, api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        try:
            await client.send_code_request(phone_number)
        except Exception as inst:
            print(inst)
            return -1
    if not await client.is_user_authorized():
        return 0
    else:
        return 1
 
async def Logear_ab(phone_number,clave):
    if not os.path.exists("session"):
        os.makedirs("session")
    client = TelegramClient("session/" + phone_number, api_id, api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        try:
            await client.send_code_request(phone_number)
            await client.sign_in(phone_number,clave)
        except Exception as inst:
            print(inst)
            return -1
    if not await client.is_user_authorized():
        return 0
    else:
        return 1
 
def CorreoFalso(cantidad):
    letters = ascii_lowercase
    result_str = "".join(choice(letters) for i in range(cantidad))
    return result_str

def NumeroFalso(cantidad):
    letters = ["0","1","2","3","4","5","6","7","8","9"]
    result_str = "".join(choice(letters) for i in range(cantidad))
    return result_str


def Des(Celular, Nombre, mostrar):
    if not os.path.exists("session"):
        os.makedirs("session")
    api_id = Confi.id()
    api_hash = Confi.hash()
    phone_number = Celular
    client = TelegramClient("session/" + phone_number, api_id, api_hash)
    if client.is_connected:
        client.disconnect()
        sleep(3)
        client.disconnect()


async def unirseCanal(client, canal):
    await client(JoinChannelRequest(canal))


def unirsecanalPriv(client, canal):
    client(functions.messages.ImportChatInviteRequest(hash=canal))


async def A_unirseCanal(client, canal):
    await client(JoinChannelRequest(canal))


def desbloquiar(client, bot):
    client(functions.contacts.UnblockRequest(bot))


def bloquiar(client, bot):
    client(functions.contacts.BlockRequest(bot))


def salircanal(cliente, bot):
    return cliente(functions.channels.LeaveChannelRequest(channel=bot))


def eliminarcanal(client, bot):
    return client.delete_dialog(bot)


def autorefer(client, bot, ref):
    client(functions.messages.StartBotRequest(bot=bot, peer=bot, start_param=ref))


def foto(mensaje):
    return mensaje.messages[0].media.photo


def resta(a):
    b = a.split("-")
    b1 = int(b[0])
    b2 = int(b[1])
    i = int(b1 - b2)
    return str(i)


def suma(a):
    b = a.split("+")
    b1 = int(b[0])
    b2 = int(b[1])
    i = int(b1 + b2)
    return str(i)


 

def acusar(ah):
    # warna
    colorama.init(autoreset=True)
    Cverde = Style.RESET_ALL + Style.BRIGHT + Fore.GREEN
    Camarillo = Style.RESET_ALL + Style.BRIGHT + Fore.YELLOW
    Crojo = Style.RESET_ALL + Style.BRIGHT + Fore.RED
    numerox=0
    if not os.path.exists("session"):
        os.makedirs("session")
    archivo = open(Q, "r")

    for linea in archivo:
        phone_number = linea.split(",")[0]
        Nombre = linea.split(",")[1]
        client = TelegramClient("session/" + phone_number, api_id, api_hash)
        client.connect()
        if not client.is_user_authorized():
            print(Crojo + "No Login de " + Nombre)
        else:
            tiempo = datetime.now()
            print(Cverde + "\n\nEjecutando en[" + Nombre + "]  ")
            numerox += 1
            print(numerox)
            print(Camarillo + str(tiempo.time()))
        try:
            bot = ["@NacionCrypto", "@notoscam"]
            ty = client.get_entity(bot[1])
            client.send_message(entity=(ty), message="eh scammer " + ah)
            
        except Exception as inst:
            print(
                Crojo
                + "\n\n**********\n*****\rError por captcha, entrar y ver dos anuncios a a mano\n**********\n"
            )
            print(inst)
        print(Crojo + "Finalizo en[" + Nombre + "]")
        tiempo = datetime.now()
        print(Camarillo + str(tiempo.time()))
        max = 1
        while client.is_connected():
            max = max + 1
            if max == 3:
                break
            client.disconnect()
            sleep(2)
 
def denuciar(arroba):
    # warna
    colorama.init(autoreset=True)
    Cverde = Style.RESET_ALL + Style.BRIGHT + Fore.GREEN
    Camarillo = Style.RESET_ALL + Style.BRIGHT + Fore.YELLOW
    Crojo = Style.RESET_ALL + Style.BRIGHT + Fore.RED
    numerox=0
    archivo = []

    if not os.path.exists("session"):
        os.makedirs("session")
    archivo = open(Q, "r")

    for linea in archivo:
        phone_number = linea.split(",")[0]
        Nombre = linea.split(",")[1]
        client = TelegramClient("session/" + phone_number, api_id, api_hash)
        client.connect()
        if not client.is_user_authorized():
            print(Crojo + "No Login de " + Nombre)
        else:
            tiempo = datetime.now()
            print(Cverde + "\n\nEjecutando en[" + Nombre + "]  ")
            numerox += 1
            print(numerox)
            print(Camarillo + str(tiempo.time()))
        try:
            user_entity = client.get_entity(arroba)

            x=client(
                ReportPeerRequest(
                    peer=user_entity,
                    reason=types.InputReportReasonSpam(),
                    message="Este usuario está violando las reglas de Telegram.",
                )
            )
            print(x)
            x=client(
                ReportPeerRequest(
                    peer=user_entity,
                    reason=types.InputReportReasonFake(),
                    message="Este usuario está violando las reglas de Telegram.",
                )
            )
            print(x)
            salircanal(client,user_entity) 
            

        except Exception as inst:
            print(Crojo + "\nsin denunciar")
            print(inst)
        print(Crojo + "Finalizo en[" + Nombre + "]")
        tiempo = datetime.now()
        print(Camarillo + str(tiempo.time()))
        max = 1
        while client.is_connected():
            max = max + 1
            if max == 3:
                break
            client.disconnect()
            sleep(2)
 
def reportarCanalesPfake(canales,message):
    colorama.init(autoreset=True)
    Cverde = Style.RESET_ALL + Style.BRIGHT + Fore.GREEN
    Camarillo = Style.RESET_ALL + Style.BRIGHT + Fore.YELLOW
    Crojo = Style.RESET_ALL + Style.BRIGHT + Fore.RED
    # Sistem_Script
    if not os.path.exists("session"):
        os.makedirs("session")
    archivo = open(Q, "r")
    numerox = 0
    ya = 1
    por = 0
    canalesPriv=[
        'Gt-CByz93KEyZDBh',
        'pt2Al28V_eg1ZTE5',
        'IRnkPdaWGCE4MTU1'
    ]
    for linea in archivo:
        phone_number = linea.split(",")[0]
        Nombre = linea.split(",")[1]
        client = TelegramClient("session/" + phone_number, api_id, api_hash)
        client.connect()
        if not client.is_user_authorized():
            print(Crojo + "No Login de " + Nombre)
        else:
            tiempo = datetime.now()
            print(Cverde + "\n\nEjecutando en[" + Nombre + "]  ")
            numerox += 1
            print(numerox)
            print(Camarillo + str(tiempo.time()))
        if ya > por:
            try:
                for canal in canalesPriv:
                    try:
                        unirsecanalPriv(client,canal)
                    except:
                        print("no me pude unir aP "+canal)
                dialogs = client.get_dialogs()
                for dialog in dialogs:
                    if dialog.is_channel:
                        if any(canal in dialog.title for canal in canales):                           
                            print(
                                f"ID del canal: {dialog.id}, nombre del canal: {dialog.title}"
                            )
                            fake=types.InputReportReasonFake()
                            x = client(
                                functions.account.ReportPeerRequest(
                                    peer=dialog.id, 
                                    reason=fake,
                                    message=message                       
                                )
                            ) 
                            print(x)
                            salircanal(client,dialog.id)
            except Exception as inst:
                print(inst)
        ya = ya + 1
        print(Crojo + "Finalizo en[" + Nombre + "]")
        tiempo = datetime.now()
        print(Camarillo + str(tiempo.time()))
        max = 1
        while client.is_connected():
            max = max + 1
            if max == 3:
                break
            client.disconnect()
            sleep(2)
        if numerox % 500 == 0:
            input("OK?\npara segir?") 
 
def vista(canales,message):
    colorama.init(autoreset=True)
    Cverde = Style.RESET_ALL + Style.BRIGHT + Fore.GREEN
    Camarillo = Style.RESET_ALL + Style.BRIGHT + Fore.YELLOW
    Crojo = Style.RESET_ALL + Style.BRIGHT + Fore.RED
    # Sistem_Script
    if not os.path.exists("session"):
        os.makedirs("session")
    archivo = open(Q, "r")
    numerox = 0
    ya = 1
    por = 0 
    for linea in archivo:
        phone_number = linea.split(",")[0]
        Nombre = linea.split(",")[1]
        client = TelegramClient("session/" + phone_number, api_id, api_hash)
        client.connect()
        if not client.is_user_authorized():
            print(Crojo + "No Login de " + Nombre)
        else:
            tiempo = datetime.now()
            print(Cverde + "\n\nEjecutando en[" + Nombre + "]  ")
            numerox += 1
            print(numerox)
            print(Camarillo + str(tiempo.time()))
        if ya > por:
            try: 
                result =client(
                    functions.messages.GetMessagesViewsRequest(
                    peer=canales,
                    id=message,
                    increment=True
                    )
                )
                print(result) 
                            
            except Exception as inst:
                print(inst)
        ya = ya + 1
        print(Crojo + "Finalizo en[" + Nombre + "]")
        tiempo = datetime.now()
        print(Camarillo + str(tiempo.time()))
        max = 1
        while client.is_connected():
            max = max + 1
            if max == 3:
                break
            client.disconnect()
            sleep(2)
        if numerox % 500 == 0:
            input("OK?\npara segir?") 
 
def algodeencuesta():
    # client(
    #         GetBotCallbackAnswerRequest
    #         GetBotCallbackAnswerRequest(
    #             peer=bot,
    #             msg_id=x.messages[0].id,
    #             data=x.messages[0].poll.poll.answers[7].option,  # Opción "Otro país"
    #         ) 
    #     )   
    f=1

def emogi(canales,message,emoticon='🔥'):
    colorama.init(autoreset=True)
    Cverde = Style.RESET_ALL + Style.BRIGHT + Fore.GREEN
    Camarillo = Style.RESET_ALL + Style.BRIGHT + Fore.YELLOW
    Crojo = Style.RESET_ALL + Style.BRIGHT + Fore.RED
    # Sistem_Script 
    numerox = 0
    ya = 1
    por = 0 
    if not os.path.exists("session"):
        os.makedirs("session")
    archivo = open(Q, "r")

    for linea in archivo:
        phone_number = linea.split(",")[0]
        Nombre = linea.split(",")[1]
        client = TelegramClient("session/" + phone_number, api_id, api_hash)
        client.connect()
        if not client.is_user_authorized():
            print(Crojo + "No Login de " + Nombre)
        else:
            tiempo = datetime.now()
            print(Cverde + "\n\nEjecutando en[" + Nombre + "]  ")
            numerox += 1
            print(numerox)
            print(Camarillo + str(tiempo.time()))
        if ya > por:
            try: 
                 
                result = client(functions.messages.SendReactionRequest(
                    peer=canales,
                    msg_id=message,
                    big=True,
                    add_to_recent=True,
                    reaction=[types.ReactionEmoji(
                        emoticon
                    )]
                ))
                print(result) 
                            
            except Exception as inst:
                print(inst)
        ya = ya + 1
        print(Crojo + "Finalizo en[" + Nombre + "]")
        tiempo = datetime.now()
        print(Camarillo + str(tiempo.time()))
        max = 1
        while client.is_connected():
            max = max + 1
            if max == 3:
                break
            client.disconnect()
            sleep(2)
        if numerox % 500 == 0:
            input("OK?\npara segir?") 
 


def ponerWalletBot():
    # warna
    colorama.init(autoreset=True)
    Cverde = Style.RESET_ALL + Style.BRIGHT + Fore.GREEN
    Camarillo = Style.RESET_ALL + Style.BRIGHT + Fore.YELLOW
    Crojo = Style.RESET_ALL + Style.BRIGHT + Fore.RED
    # Sistem_Script
    if not os.path.exists("session"):
        os.makedirs("session")
    archivo = open(Q, "r")
    numerox = 0
    for linea in archivo:
        phone_number = linea.split(",")[0]
        Nombre = linea.split(",")[1]
        client = TelegramClient("session/" + phone_number, api_id, api_hash)
        client.connect()
        bot = [client.get_entity("@LendBirdbot"), client.get_entity("@cctip_bot")]
        if not client.is_user_authorized():
            print(Crojo + "No Login de " + Nombre)
        else:
            tiempo = datetime.now()
            print(Cverde + "\n\nEjecutando en[" + Nombre + "]  ")
            numerox += 1
            print(numerox)
            print(Camarillo + str(tiempo.time()))
        try:
            MensajePlano("⚜️ ᴡᴀʟʟᴇᴛ", bot[0], client)
            sleep(3)
            clickBotonera(client, bot[0], UltimoMensaje(client, bot[0]), 0, 0)
            MensajePlano("deposit dgb", bot[1], client)
            sleep(3)
            dgb = mensaje(UltimoMensaje(client, bot[1]), ":", 1).strip()
            MensajePlano(dgb, bot[0], client)

        except Exception as inst:
            print(
                Crojo
                + "\n\n**********\n*****\rError por captcha, entrar y ver dos anuncios a a mano\n**********\n"
            )
            print(inst)
        print(Crojo + "Finalizo en[" + Nombre + "]")
        tiempo = datetime.now()
        print(Camarillo + str(tiempo.time()))
        max = 1
        while client.is_connected():
            max = max + 1
            if max == 3:
                break
            client.disconnect()
            sleep(2)


def Salirser(x):
    colorama.init(autoreset=True)
    Cverde = Style.RESET_ALL + Style.BRIGHT + Fore.GREEN
    Camarillo = Style.RESET_ALL + Style.BRIGHT + Fore.YELLOW
    Crojo = Style.RESET_ALL + Style.BRIGHT + Fore.RED
    # Sistem_Script
    if not os.path.exists("session"):
        os.makedirs("session")
    numerox = 0
    if not os.path.exists("session"):
        os.makedirs("session")
    archivo = open(Q, "r")

    # archivo=["+573102820183,ff,hug","+573001403046,hjhjijj,huh"]

    for linea in archivo:
        phone_number = linea.split(",")[0]
        Nombre = linea.split(",")[1]
        client = TelegramClient("session/" + phone_number, api_id, api_hash)
        client.connect()
        if not client.is_user_authorized():
            print(Crojo + "No Login de " + Nombre)
        else:
            tiempo = datetime.now()
            print(Cverde + "\n\nEjecutando en[" + Nombre + "]  ")
            numerox += 1
            print(numerox)
            print(Camarillo + str(tiempo.time()))
        try: 
            for canal in x:
                try:
                    participant = client(functions.phone.GetParticipantRequest(canal.entity, 'me'))
                    if not participant.participant.admin_rights:
                        salircanal(client, client.get_entity(canal))
                        print("sali de "+canal)
                except Exception as inst:
                    print("nop sali de "+canal)
                    # print(inst)
                    f = 1
            # try:
            #     bloquiar(client,bot)
            #     eliminarcanal(client,client.get_entity(bot))
            # except Exception as inst :
            #     print(inst)

        except Exception as inst:
            print(
                Crojo
                + "\n\n**********\n*****\rError por captcha, entrar y ver dos anuncios a a mano\n**********\n"
            )
            print(inst)
        print(Crojo + "Finalizo en[" + Nombre + "]")
        tiempo = datetime.now()
        print(Camarillo + str(tiempo.time()))
        max = 1
        while client.is_connected():
            max = max + 1
            if max == 3:
                break
            client.disconnect()
            sleep(2)
        input("ss")
 

def SalirTotal():
    colorama.init(autoreset=True)
    Cverde = Style.RESET_ALL + Style.BRIGHT + Fore.GREEN
    Camarillo = Style.RESET_ALL + Style.BRIGHT + Fore.YELLOW
    Crojo = Style.RESET_ALL + Style.BRIGHT + Fore.RED
    # Sistem_Script
    if not os.path.exists("session"):
        os.makedirs("session") 

    numerox=0
    if not os.path.exists("session"):
        os.makedirs("session")
    archivo = open(Q, "r")

    for linea in archivo:
        phone_number = linea.split(",")[0]
        Nombre = linea.split(",")[1]
        client = TelegramClient("session/" + phone_number, api_id, api_hash)
        client.connect()
        if not client.is_user_authorized():
            print(Crojo + "No Login de " + Nombre)
        else:
            tiempo = datetime.now()
            print(Cverde + "\n\nEjecutando en[" + Nombre + "]  ")
            numerox += 1
            print(numerox)
            print(Camarillo + str(tiempo.time()))
        try:
            dialogs = client.get_dialogs()
            for dialog in dialogs:
                if isinstance(dialog.entity, types.Channel):
                    try:
                        try:
                            CANALES.index(str(dialog.entity.username).lower())
                        except: 
                            try:
                                participants = client(functions.channels.GetParticipants(
                                    channel=dialog.entity,
                                    filter=types.ChannelParticipantsAdmins(),
                                    offset=0,
                                    limit=200,  # Ajusta el límite según sea necesario
                                ))

                                # Verifica si eres el creador o administrador
                                is_admin = any(participant.user_id == client.get_me().id for participant in participants.participants)
                                if not is_admin:
                                    salircanal(client, dialog.entity.id)
                                    print(Cverde + "Canal " + dialog.entity.username)
                            except:
                                salircanal(client, dialog.entity.id)
                                print(Cverde + "Canal " + dialog.entity.username)
                            
                    except Exception as x:
                        print(Cverde, x)
                else:
                    try:
                        if dialog.entity.bot:
                            try:
                                BOTS.index(str(dialog.entity.username).lower())
                            except:
                                bloquiar(client, ((dialog.entity.id)))
                                eliminarcanal(client, ((dialog.entity.id)))
                                print(Crojo + "Bot   " + dialog.entity.username)
                    except Exception as x:
                        print(Crojo, x)

            for canal in CANALES:
                try:
                    unirseCanal(client, canal)
                except:
                    print("no me pude unir a " + canal)

        except Exception as inst:
            print(Crojo, inst)
        print(Crojo + "Finalizo en[" + Nombre + "]")
        tiempo = datetime.now()
        print(Camarillo + str(tiempo.time()))
        max = 1
        while client.is_connected():
            max = max + 1
            if max == 3:
                break
            client.disconnect()
            sleep(2)

def SalirTotalF():
    colorama.init(autoreset=True)
    Cverde = Style.RESET_ALL + Style.BRIGHT + Fore.GREEN
    Camarillo = Style.RESET_ALL + Style.BRIGHT + Fore.YELLOW
    Crojo = Style.RESET_ALL + Style.BRIGHT + Fore.RED
    # Sistem_Script
    if not os.path.exists("session"):
        os.makedirs("session") 
    archivo = open(Q, "r")
    numerox = 0 
    for linea in archivo:
        phone_number = linea.split(",")[0]
        Nombre = linea.split(",")[1]
        client = TelegramClient("session/" + phone_number, api_id, api_hash)
        client.connect()
        if not client.is_user_authorized():
            print(Crojo + "No Login de " + Nombre)
        else:
            tiempo = datetime.now()
            print(Cverde + "\n\nEjecutando en[" + Nombre + "]  ")
            numerox += 1
            print(numerox)
            print(Camarillo + str(tiempo.time()))
        try:
            dialogs = client.get_dialogs()
            for dialog in dialogs:
                if isinstance(dialog.entity, types.Channel):
                    try: 
                        salircanal(client, ((dialog.entity.id)))
                        print(Cverde + "Canal " + dialog.entity.username)
                    except Exception as x:
                        print(Cverde, x)
                else:
                    try:
                        if dialog.entity.bot: 
                            bloquiar(client, ((dialog.entity.id)))
                            eliminarcanal(client, ((dialog.entity.id)))
                            print(Crojo + "Bot   " + dialog.entity.username)
                    except Exception as x:
                        print(Crojo, x)

             

        except Exception as inst:
            print(Crojo, inst)
        print(Crojo + "Finalizo en[" + Nombre + "]")
        tiempo = datetime.now()
        print(Camarillo + str(tiempo.time()))
        max = 1
        while client.is_connected():
            max = max + 1
            if max == 3:
                break
            client.disconnect()
            sleep(2)


def selectIcons(mensaje):
    a = mensaje.messages[0].message
    b = a[-1]
    # print(Camarillo, mensaje.messages[0].reply_markup)
    d = str(mensaje.messages[0].reply_markup).split("', d")
    f = 0
    columna = 0
    fila = 0
    for x in d:
        if f < 9:
            if x[-1] != b:
                if fila == 3:
                    fila = 0
                    columna += 1
                fila += 1
            else:
                return [columna, fila]
            f += 1

def pasarSaldo(moneda):
    bot = ["@botcolombiachat", "@cctip_bot"]
    # warna
    colorama.init(autoreset=True)
    Cverde = Style.RESET_ALL + Style.BRIGHT + Fore.GREEN
    Camarillo = Style.RESET_ALL + Style.BRIGHT + Fore.YELLOW
    Crojo = Style.RESET_ALL + Style.BRIGHT + Fore.RED
    # Sistem_Script
    if not os.path.exists("session"):
        os.makedirs("session") 
    numerox = 0

    if not os.path.exists("session"):
        os.makedirs("session")
    archivo = open(Q, "r") 
    archivo2=[]    
    archivo2.append("+573135545431,milena,mio")
    for linea in archivo:
        archivo2.append(linea)
    for linea in archivo2:
        phone_number = linea.split(",")[0]
        Nombre=""
        try:
            Nombre = linea.split(",")[1]
        except:
            Nombre=""
        client = TelegramClient("session/" + phone_number, api_id, api_hash)
        try:
            client.connect()
            if not client.is_user_authorized():
                print(Crojo + "No Login de " + Nombre)
            else:
                tiempo = datetime.now()
                print(Cverde + "\n\nEjecutando en[" + Nombre + "]  ")
                numerox += 1
                print(numerox)
                print(Camarillo + str(tiempo.time()))

            try: 
                ty = client.get_entity(bot[1])
                client.send_message(
                    entity=client.get_entity(ty), message="balance " + moneda
                )
                sleep(3)
                texto = mensaje2(UltimoMensaje(client, ty), ":", 2, "👉", 0) 
                print("tengo= "+texto+" "+moneda)
                gana=0
                try:
                    gana = Decimal(texto.strip())
                except Exception as inst:  
                    gana=0
                try: 
                    if gana > 0 and phone_number != "+573102820183":
                        gana_str = str(gana)
                        message="cc " + (gana_str) + " " + moneda + " @vuejson"
                        client.send_message(
                            entity=client.get_entity(bot[0]),
                            message=message,
                        )
                except:
                    x=""
                    if(moneda=='dgb'):
                        x="Withdraw "+str(gana*0,99)+" dgb dgb1q7jlyuz4vchz4f2fg70af3yv5p0lv3v8fm53vyt" 
                    if(moneda=='trx'):
                        x="Withdraw "+str(gana*0,95)+" trx TG6eArVrfDrhX1qckJ2GxLFsrAAeHxmN8w" 
                    client.send_message(
                        entity=client.get_entity(ty), message=x
                    )
                 

            except Exception as inst: 
                print(inst)
            print(Crojo + "Finalizo en[" + Nombre + "]")
            tiempo = datetime.now()
            print(Camarillo + str(tiempo.time()))
            max = 1
            while client.is_connected():
                max = max + 1
                if max == 3:
                    break
                client.disconnect()
                sleep(2)
        except:
            f=1
def buscarMensaje(client, channel_entity,ultimo=0):
    return client(
        GetHistoryRequest(
            peer=channel_entity,
            limit=1,
            offset_date=None,
            offset_id=ultimo,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0,
        )
    )

def  rando(ini, fin):
    return choice(range(ini,fin))

def laWallet(client,moneda):
    arro="@cctip_bot"
    MensajePlano("Deposit "+moneda,arro,client)
    sleep(5) 
    dgb = mensaje(UltimoMensaje(client,arro), ":", 1).strip()
    return dgb
 
def Soy():
    colorama.init(autoreset=True)
    Cverde = Style.RESET_ALL + Style.BRIGHT + Fore.GREEN
    Camarillo = Style.RESET_ALL + Style.BRIGHT + Fore.YELLOW
    Crojo = Style.RESET_ALL + Style.BRIGHT + Fore.RED
    numerox=0
    if not os.path.exists("session"):
        os.makedirs("session")
    archivo = open(Q, "r")

    ya=1
    por=45

    for linea in archivo:
        if ya > por:
            phone_number = linea.split(",")[0]
            Nombre = linea.split(",")[1]
            client = TelegramClient("session/" + phone_number, api_id, api_hash)
            client.connect()
            if not client.is_user_authorized():
                print(Crojo + "No Login de " + Nombre)
            else:
                tiempo = datetime.now()
                print(Cverde + "\n\nEjecutando en[" + Nombre + "]  ")
                numerox += 1
                print(numerox)
                print(Camarillo + str(tiempo.time()))  
                me = client.get_me() 
                text=f'\tInfo.Script\n\nNombre:{me.first_name} {me.last_name}\nnumero: `{me.phone}`\nId: `{me.id}`\nUser: @{me.username}\nTRC: `{laWallet(client,"bttnew")}` \nDGB: `{laWallet(client,"dgb")}`'
                try:
                    MensajePlano(text,PRINCIPAL,client)
                except:
                    print(Crojo,"Error")
                max=0
            while client.is_connected():
                max = max + 1
                if max == 3:
                    break
                client.disconnect()
                sleep(2) 
        ya = ya + 1
        

 
def salir():
    colorama.init(autoreset=True)
    Cverde = Style.RESET_ALL + Style.BRIGHT + Fore.GREEN
    Camarillo = Style.RESET_ALL + Style.BRIGHT + Fore.YELLOW
    Crojo = Style.RESET_ALL + Style.BRIGHT + Fore.RED
    # Sistem_Script
    if not os.path.exists("session"):
        os.makedirs("session")
    archivo = open(Q, "r")
    numerox = 0
    ya = 1
    por = 0 
    bot = "@coindesk_dgbairdrop_bot"
    ref = "2070532469"
    salirl = [
        "SportsPotOffcial"
    ]
    
    if not os.path.exists("session"):
        os.makedirs("session")
    archivo = open(Q, "r")

    for linea in archivo:
        phone_number = linea.split(",")[0]
        Nombre = linea.split(",")[1]
        client = TelegramClient("session/" + phone_number, api_id, api_hash)
        client.connect()
        if not client.is_user_authorized():
            print(Crojo + "No Login de " + Nombre)
        else:
            tiempo = datetime.now()
            print(Cverde + "\n\nEjecutando en[" + Nombre + "]  ")
            numerox += 1
            print(numerox)
            print(Camarillo + str(tiempo.time()))
        if ya > por:
            try: 
                for canal in salirl:
                    try:
                        salircanal(client, canal) 
                    except:
                        print("no me pude unir a " + canal)  
            except Exception as inst:
                print(inst)
     
        ya = ya + 1
 
        print(Crojo + "Finalizo en[" + Nombre + "]")
        tiempo = datetime.now()
        print(Camarillo + str(tiempo.time()))
        max = 1
        while client.is_connected():
            max = max + 1
            if max == 3:
                break
            client.disconnect()
            sleep(2)
        if numerox % 100 == 0:
            input("OK?\npara segir?")
  
 
def EstoyCanal(canal,client):
    dialogs = client.get_dialogs()
    estoy=False
    for dialog in dialogs:
        try:
            if(dialog.entity.username==canal):
                return True
                break
        except:
            pass
    return False

def BorrarTodosMensaje(canal,client):
    for message in client.iter_messages(canal, from_user='me'):
        client.delete_messages(canal, [message.id])

def cambiarArroba(client,arroba):
    result = client(functions.account.UpdateUsernameRequest(
                         username=arroba[:25]
                    ))
      
def BotRefe(client,bot,ref):
    client(
        functions.messages.StartBotRequest(
            bot=bot, peer=bot, start_param=ref
        )
    ) 
 

################################################################3
################################################################3
################################################################3
################################################################3
async def EjecutarTaarea(el_text,cuentas,principal,ini=0,fin=100000,por=0):
    ##-1 no conexion cliente no autorizado
    ##0 un error en lo que debe hacer
    contador=0 
    for cuenta in cuentas:
        if ini==fin:
            return 1,errores,contador
        if contador>=por:
            ini+=1 ##solo para saber en cuanta se ejecutara
            phone_number = cuenta.get("numero") 
        
            client = TelegramClient("session/" + phone_number, api_id, api_hash)
            await client.connect()
            if not await client.is_user_authorized(): 
                return -1,cuenta.get("numero"),contador
            errores="_"
            bot=""
            ref=""
            for x in el_text:  
                if x.startswith("unirser"):
                    canales=x[8:].split(",")
                    l=[]
                    for canal in canales: 
                        if canal[0]=="@":
                            l.append(canal[1:])
                        if canal.startswith("http"):
                            l.append(canal.split("t.me/")[1])
                    for canal in l:
                        try:
                            await unirseCanal(client, canal)
                        except:
                            errores+=f"{phone_number} no se pudo unir a {canal}\n"
                
                if x.startswith("unirserPriv"):
                    canales=x[12:].split(",")
                    l=[]
                    for canal in canales: 
                        if canal[0]=="@":
                            l.append(canal[2:])
                        if canal[0]=="1":
                            l.append(canal[1:])
                        if canal.startswith("http"):
                            l.append(canal.split("t.me/+")[1])
                    
                    for canal in l:
                        try:
                            await unirsecanalPriv(client, canal)
                        except:
                            errores+=f"{phone_number} no se pudo unir ap {canal}\n"
            
                if x.startswith("mensaje"):
                    f="" 
                    try:
                        if x[8]=="@":
                            patron = r'@(\w+)'
                            coincidencias = re.findall(patron, x)  
                            canal="@"+coincidencias[0] 
                            mensaje=x.split(canal)[1] 
                            await MensajePlano(mensaje, canal,client)
                        else:
                            await MensajePlano(x[7:],bot,client)
                    except:
                        errores+=f"{phone_number}no se puedo enviar mensaje\n"

                if x.startswith("ini"):
                    try:
                        ini=int(x[4:])
                    except:
                        errores+=f"El inicio no fue cambiado {x[4:]}\n"
                if x.startswith("fin"):
                    try:
                        fin=int(x[4:])
                    except:
                        errores+=f"El fin no fue cambiado {x[4:]}\n"
                if x.startswith("por"):
                    try:
                        por=int(x[4:])
                    except:
                        errores+=f"El por no fue cambiado {x[4:]}\n"
            
                if x.startswith("desbloquiar"):
                    canales=x[12:].split(",")
                    l=[]
                    for canal in canales: 
                        if canal[0]=="@":
                            l.append(canal[1:])
                        if canal.startswith("http"):
                            l.append(canal.split("t.me/")[1])
                    for canal in l:
                        try:
                            await desbloquiar(client, canal)
                        except:
                            errores+=f"{phone_number} no se pudo desbloquiar a {canal}\n"
               
                if x.startswith("botRef"):
                    link=x.split("?")
                    bot=link[0].split("t.me/")[1]
                    ref=link[1].split("=")[1]
                if x.startswith("bot"): 
                    bot=x[5:]
                if x.startswith("Ref"): 
                    ref=x[4:]
                
                if x.startswith("envia"): 
                    cual=x.split(" ")
                    if(len(cual)==1):
                        mensaje=await UltimoMensaje(client,bot)
                        mensaje=mensaje.messages[0].message
                    else:
                        try:
                            cual=int(cual[1])
                        except:
                            errores+=f"al #enviar debe ser un numero\n"
                            cual=0
                        id_mns=await UltimoMensaje(client,bot)
                        id_mns=id_mns.messages[0].id
                        mensaje=await buscarMensaje(client,bot,id_mns-cual)
                        mensaje=mensaje.messages[0].message
                    await MensajePlano(mensaje,bot,client)
                
                if x.startswith("renvia"): 
                    cual=x.split(" ")
                    if(len(cual)==1):
                        mensaje=await UltimoMensaje(client,bot) 
                        mensaje=mensaje.messages[0].message
                    else:
                        try:
                            cual=int(cual[1])
                        except:
                            errores+=f"al #enviar debe ser un numero\n"
                            cual=0
                        id_mns=await UltimoMensaje(client,bot)
                        id_mns=id_mns.messages[0].id
                        mensaje=await buscarMensaje(client,bot,id_mns-cual)                        
                        mensaje=mensaje.messages[0].message
                    await MensajePlano(mensaje,principal.grupo,client)

                if x.startswith("esperar"): 
                    cual=x.split(" ")
                    if(len(cual)==1):
                        errores+=f"al #esperar debe ser un numero\n"
                        sleep(2)
                    else:
                        try:
                            v=int(cual[1])
                        except:
                            errores+=f"al #esperar debe ser un numero\n"
                            v=2
                        sleep(v)
            
            await client.disconnect()
        contador+=1
    return 0,errores,contador
    

async def validarcuenta(phone_number,canales): 
    ##-1 cuenta sin activar
    ##1 no canales??
    ##2 no escribir
    ##0 ok
    colorama.init(autoreset=True)
    Cverde = Style.RESET_ALL + Style.BRIGHT + Fore.GREEN
    Camarillo = Style.RESET_ALL + Style.BRIGHT + Fore.YELLOW
    Crojo = Style.RESET_ALL + Style.BRIGHT + Fore.RED
    if not os.path.exists("session"):
        os.makedirs("session")       
    client = TelegramClient("session/" + phone_number, api_id, api_hash)
    await client.connect()
    if not await client.is_user_authorized():        
        print(Crojo +f"No tengo autorizacion {phone_number}")
        return "No tengo autorizacion",-1
    else:
        tiempo = datetime.now()  
        print(Camarillo + str(tiempo.time()))
    ok=0
    for canal in canales:
        try:
            await unirseCanal(client, canal)
        except:
            ok=1
            print(Crojo+"no me pude unir a " + canal)  
    me = await client.get_me() 
    text=f'\tInfo.Script[{api_id}]\n\n'\
        f'Nombre:{me.first_name} {me.last_name}\n'\
        f'numero: `{me.phone}`\n'\
        f'Id: `{me.id}`\n'\
        f'User: @{me.username}'
    try:
        await MensajePlano(text,canales[0],client) 
    except:
        ok=2
        print(Crojo+"Error")
    tiempo = datetime.now()
    print(Camarillo + str(tiempo.time()))
    max = 1
    while client.is_connected():
        max = max + 1
        if max == 3:
            break
        client.disconnect()
        sleep(2) 
    return "Tengo acceso",ok