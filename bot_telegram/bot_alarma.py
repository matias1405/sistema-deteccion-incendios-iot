from telegram.ext import CommandHandler, Updater, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Bot
import os
import time

_token = os.environ['TOKEN']
password = '1405'
input_text = 0
chats_aceptados = []

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
    print('avisado')

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
    time.sleep(100)
    print('noificando...')
    bot=Bot(_token)
    button = InlineKeyboardButton(text = 'Incendio Terminado',
                                  callback_data = 'incendio_terminado')
    for id_acep in chats_aceptados:
        bot.send_message(chat_id=id_acep,
                         text='avisa de incendio',
                         reply_markup = InlineKeyboardMarkup([[button]]))

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
    while(True):
        notificar()
    updater.idle()
