from paho.mqtt import client as mqtt_client
from telegram.ext import CommandHandler, Updater, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Bot
import os
import time

#_token = os.environ['TOKEN']
password = '1405'
_token = "5129425944:AAE9qC_w4bvcXH-j6Zuf0Mb1Qf27KR7h4IM"
input_text = 0
chats_aceptados = []

broker = 'localhost'
port = 1883
topic = "python/mqtt"


def start(update, context):
    button_1 = InlineKeyboardButton(
        text = 'Verificación',
        callback_data = 'password')
    update.message.reply_text(
        text = 'Bienvenidos al Sistema de Alerta de Incedios',
        reply_markup = InlineKeyboardMarkup([[button_1]]))

def callback_password(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text='Por favor, Ingrese la contraseña')
    return 'estate_1'

def callback_terminado(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text='Aviso enviado')
    print('Aviso de incendio terminado RECIBIDO')

def callback_dar_baja(update, context):
    query = update.callback_query
    query.answer()

def verificacion_password(update, context):
    if password == update.message.text:
        update.message.reply_text('Contraseña aceptada')
        update.message.reply_text('Se enviará una alerta en caso de incendio')
        chats_aceptados.append(update.message.chat.id)
    else:
        update.message.reply_text('Contraseña incorrecta')
    return ConversationHandler.END

def notificar():
    aviso = 'Este es un aviso de INCENDIO, por favor contacta con las \
    autoridades de emergencia.\nNro tel Bomberos: 105\nNro tel Policia \
    101\n Por favor notifique por este medio al Sistema cuando la situacion\
    de incendio alla terminado'
    print('noificando...')
    bot=Bot(_token)
    button = InlineKeyboardButton(text = 'Incendio Terminado',
                                  callback_data = 'incendio_terminado')
    for id_acep in chats_aceptados:
        bot.send_message(chat_id=id_acep,
                         text=aviso,
                         reply_markup = InlineKeyboardMarkup([[button]]))

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client()
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        mensaje = msg.payload.decode()
        print(f"Received `{mensaje}` from `{msg.topic}` topic")
        if mensaje == 'incendio':
            notificar()
    client.subscribe(topic)
    client.on_message = on_message

if __name__ == '__main__':
    _entry = [CallbackQueryHandler(pattern = 'password', callback = callback_password)]
    _states = {'estate_1' : [MessageHandler(Filters.text, verificacion_password)],
              'estate_2' : []}

    updater = Updater(token = _token, use_context = True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(pattern = 'incendio_terminado', callback = callback_terminado))
    dp.add_handler(CallbackQueryHandler(pattern = 'baja', callback = callback_dar_baja))
    dp.add_handler(ConversationHandler(entry_points=_entry, states=_states,
    fallbacks=[]))
    updater.start_polling()
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()
    updater.idle()
