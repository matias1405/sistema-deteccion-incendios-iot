#!/usr/bin/python3

# Universidad Tecnológica Nacional - Facultad Regional Tucumán
# Proyecto Final de grado
# Sistema de Alarma contra Incendios basado en Tecnologías de IoT
# Dessarolladores:
#    + Matías Alfaro - matiasalfaro1405@gmail.com
#    + Romina Farías - romii12mf@gmail.com


"""
Este script crea un bot para Telegram el cual notificará a los interesados
cuando el Sistema de Alarma contra Incendios detecte un incendio activo o
alguna novedad sobre el estado del sistema. Por ejemplo: si la batería de
algún dispositivo está baja.
El usuario de telegram que desee ser notificado deberá iniciar el bot y
colocar la contraseña del sistema.
"""


import os
import time

from paho.mqtt import client as mqtt_client
from telegram.ext import(
    CommandHandler,
    Updater,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters
)
from telegram import(
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Bot
)

#============== definicion de variables ===================================

_token = os.environ['TOKEN'] #obtenemos el token de una varible de entorno
password = '1405'
chats_aceptados = []
broker = 'localhost'
port = 1883
topic = "s-alerta-incendio/estado"

#================ definicion de clases ===================================

class BaseDeDatos:
    def __init__(self, _path):
        self.path = _path
        self.chats_aceptados = []
        try:
            with open(self.path, 'rt') as f:
                self.chats_aceptados = f.readlines()
        except:
            with open(self.path, 'wt') as f:
                pass

    def add(id):
        id = str(id) + "\n"
        if id not in self.chats_aceptados:
            with open(self.path, 'r+t') as f:
                f.write(id)
            with open(self.path, 'rt') as f:
                self.chats_aceptados = f.readlines()

    def remove(id):
        id = str(id) + "\n"
        with open(self.path, 'wt') as f:
            for chat in self.chats_aceptados:
                if chat != id:
                    f.write(chat)
        with open(self.path, 'rt') as f:
            self.chats_aceptados = f.readlines()

    def get_id():
        return [int(chat) for chat in self.chats_aceptados]


#============== definicion de funciones ==================================

def start(update, context):
    """
    El bot devuelve un mensaje de bienvenida junto a un boton llamado
    "verificacion", si el usuario oprime el boton se devuelve en forma de
    callback data la palabra 'password'.
    """
    button_1 = InlineKeyboardButton(
        text = 'Verificación',
        callback_data = 'password'
    )
    update.message.reply_text(
        text = 'Bienvenidos al Sistema de Alerta de Incedios',
        reply_markup = InlineKeyboardMarkup([[button_1]])
    )


def callback_password(update, context):
    """
    Responde silenciosamente al llamado de una callback_query, luego cambia el
    boton y texto asociado por un mensaje.
    Esta funcion esta dentro de una ConversationHandler así que devuelve la
    cadena estate_1 para relacionarlo con un estado de conversacion.
    Es el primer paso para que el usuario ingrese la contraseña de verificacion
    """
    query = update.callback_query
    query.answer()
    query.edit_message_text(text='Por favor, Ingrese la contraseña')
    return 'estate_1'


def callback_terminado(update, context):
    """
    Responde silenciosamente al llamado de una callback_query, luego cambia el
    boton y texto asociado por un mensaje.
    Esta funcion es llamada si el usuario avisa al bot que el incendio
    termino para que este a su vez, avise al sistema.
    """
    query = update.callback_query
    query.answer()
    query.edit_message_text(text='Aviso enviado')
    print('Aviso de incendio terminado RECIBIDO')


def callback_dar_baja(update, context):
    """
    Responde silenciosamente al llamado de una callback_query, luego cambia el
    boton y texto asociado por un mensaje.
    Esta funcion se lanza si el usuario oprime el boton para dar de baja el
    servicio de notificaciones. Busca y elimina el id del usuario en la base de
    datos
    """
    query = update.callback_query
    query.answer()
    db.remove(update.message.chat.id)


def verificacion_password(update, context):
    """
    Esta función es llamada cuando el usuario ingreso la contraseña de
    verificacion.
    + Si la contraseña es correcta se responde positivamente y se llama a
    la funcion agregar_usuario.
    + Si la contraseña no es correcta se responde negativamente. Nota: en este
    caso si el usuario quiere ser avisado por el bot deberá volver a iniciarlo.

    Luego termina la conversacion.
    """
    if password == update.message.text:
        update.message.reply_text('Contraseña aceptada')
        update.message.reply_text('Se enviará una alerta en caso de incendio')
        db.add(update.message.chat.id)
    else:
        update.message.reply_text('Contraseña incorrecta')
    return ConversationHandler.END


def connect_mqtt() -> mqtt_client:
    """
    Crea el objeto cliente y lo conecta al broker de mqtt.
    Llama a un funcion callback on_connect  que avisa si el bot pudo o no
    conectarse.
    Devuelve un objeto de la clase mqtt_client.
    """
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client()
    client.on_connect = on_connect
    print('2')
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    """
    Recibe un objeto de la clase mqtt_client.
    Subscribe al topic indicado y en caso de recibir un mensaje llama a la
    funcion callback on_message. Esta funcion muestra el mensaje en pantalla
    y en caso de que la palabra recibida sea incendio, llama a la funcion
    notificar.
    """
    def on_message(client, userdata, msg):
        mensaje = msg.payload.decode()
        print(f"Received `{mensaje}` from `{msg.topic}` topic")
        if mensaje == 'incendio':
            notificar()

    client.subscribe(topic)
    client.on_message = on_message


def notificar():
    """
    Esta funcion crea otro bot que avisa a los usuarios en caso de incendio.
    El aviso se da a todos los usuarios registrados en la base de datos.
    El mensaje consta de un texto y un boton que el usuario deberára presionar
    cuando el incendio haya terminado para avisar al sistema.
    """
    aviso = 'Este es un aviso de INCENDIO, por favor contacta con las\
    autoridades de emergencia.\nNro tel Bomberos: 105\nNro tel Policia\
    101\nPor favor notifique por este medio al Sistema cuando la situación\
    de incendio haya terminado'
    print('noificando...')
    bot=Bot(_token)
    button = InlineKeyboardButton(
        text = 'Incendio Terminado',
        callback_data = 'incendio_terminado'
    )
    for id_acep in db.get_id():
        bot.send_message(
            chat_id=id_acep,
            text=aviso,
            reply_markup = InlineKeyboardMarkup([[button]])
        )


if __name__ == '__main__':

    #creacion de la base de datos

    db = BaseDeDatos("./chats_id.txt")

    #========== comandos de para interactuar con telegram ====================

    #crea un bot a traves del objeto updater - actualizador
    updater = Updater(token = _token, use_context = True)
    #creamos el dispatcher para manejar los metodos handler
    dp = updater.dispatcher
    #cuando el bot reciba el comando '/start', llama a la fucion start
    dp.add_handler(CommandHandler('start', start))
    #cuando el se reciba un callback_data relacionado a la palabra pattern
    #llama a la funcion callback especificada
    dp.add_handler(CallbackQueryHandler(
        pattern = 'incendio_terminado',
        callback = callback_terminado)
    )
    dp.add_handler(CallbackQueryHandler(
        pattern = 'baja',
        callback = callback_dar_baja)
    )
    #crea una conversacion con los siguientes puntos de entradas y estados
    dp.add_handler(ConversationHandler(
        entry_points = [CallbackQueryHandler(
            pattern = 'password',
            callback = callback_password)
        ],
        states = {
            'estate_1' : [MessageHandler(Filters.text, verificacion_password)],
            'estate_2' : []
        },
        fallbacks=[])
    )
    #empieza a escanear el updater en busca de novedades en segundo plano
    updater.start_polling()

    #============= comandos para interactuar con el broker de mqtt ===========

    #crea un objeto cliente de la clase mqtt_client
    client = connect_mqtt()
    subscribe(client)
    #busca novedades del cliente en segundo plano
    client.loop_forever()
    updater.idle()
