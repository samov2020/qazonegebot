import telebot
from telebot import types
import logging
import time
import flask
import os

API_TOKEN = '1418888936:AAHSr7P3oWrQTtaEL2DDrc2pkIithtZFCJg'

WEBHOOK_HOST = 'https://qazonegebot.herokuapp.com/'
WEBHOOK_PORT = int(os.environ.get('PORT', 5000))  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = './qazonegebot.herokuapp.com.key'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = './qazonegebot.herokuapp.com.cert'  # Path to the ssl private key


WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)


app = flask.Flask(__name__)
bot = telebot.TeleBot(API_TOKEN)

# Empty webserver index, return nothing, just http 200
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''


# Process webhook calls
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


user = bot.get_me()

### Language choice
languageMarkup = types.InlineKeyboardMarkup()
kzButton = types.InlineKeyboardButton( 'ҚЗ',callback_data ='kz' )
ruButton = types.InlineKeyboardButton( 'РУ',callback_data ='ru' )
languageMarkup.add( kzButton, ruButton)

lngChooseButton = types.InlineKeyboardButton( text = 'Тілді өзгерту/Сменить язык', callback_data = 'lang' )

### RU section
startMarkup = types.InlineKeyboardMarkup()
zoomButton = types.InlineKeyboardButton( '📹Zoom', callback_data = 'zoomru' )
skillcupButton = types.InlineKeyboardButton( '🥛Skill Cup', callback_data = 'skillcupru' )
otherButton = types.InlineKeyboardButton( 'Другое', callback_data = 'otherru' )
startMarkup.add( zoomButton, skillcupButton, otherButton, lngChooseButton )

zoomMarkupru = types.InlineKeyboardMarkup( row_width = 3 )
zoomButton1ru = types.InlineKeyboardButton( text = 'Инструкция по установке ZOOM на ваше устройство', url = 'https://youtu.be/avGVFLILcrA')
zoomButton2ru = types.InlineKeyboardButton( text = 'Инструкция по основным функциям ZOOM', url = 'https://youtu.be/b8MLT2F0ZSo')
gobackButtonru = types.InlineKeyboardButton( text  = '⬅️', callback_data = 'gobackru')
zoomMarkupru.add( zoomButton1ru, zoomButton2ru, gobackButtonru )

skillcupMarkupru = types.InlineKeyboardMarkup( row_width = 3 )
skillcupButton1ru = types.InlineKeyboardButton(text='Инструкция по использованию Skill Cup', url='https://youtu.be/KUv0ytlDt1U')
skillcupMarkupru.add(skillcupButton1ru,gobackButtonru)

otherMarkupru = types.InlineKeyboardMarkup( row_width = 3 )
otherButtonru = types.InlineKeyboardButton( text = 'Форма обращения', url = 'tiny.cc/skillcup' )
otherMarkupru.add( otherButtonru, gobackButtonru )

### KZ Setion
startMarkupkz = types.InlineKeyboardMarkup()
zoomButtonkz = types.InlineKeyboardButton('📹Zoom', callback_data = 'zoomkz' )
skillcupButtonkz = types.InlineKeyboardButton( '🥛Skill Cup', callback_data = 'skillcupkz' )
otherButtonkz = types.InlineKeyboardButton( 'Басқа', callback_data = 'otherkz' )
startMarkupkz.add(zoomButtonkz,skillcupButtonkz,otherButtonkz,lngChooseButton)

zoomMarkupkz = types.InlineKeyboardMarkup( row_width = 3)
zoomButton1kz = types.InlineKeyboardButton( text='Орнату нұсқаулық', url = 'https://youtu.be/DSnxu1s5aV4')
zoomButton2kz = types.InlineKeyboardButton( text='Пайдалану нұсқаулық', url = 'https://youtu.be/LR4qDy9Jpek')
gobackButtonkz = types.InlineKeyboardButton( text = '⬅️', callback_data = 'gobackkz')
zoomMarkupkz.add(zoomButton1kz, zoomButton2kz, gobackButtonkz)

skillcupMarkupkz = types.InlineKeyboardMarkup(row_width = 3)
skillcupButton1kz = types.InlineKeyboardButton(text = 'Skill Cup қолданау нұсқаулық', url='https://youtu.be/J0fs6lYbge4')
skillcupMarkupkz.add(skillcupButton1kz, gobackButtonkz)

otherMarkupkz = types.InlineKeyboardMarkup(row_width =3 )
otherButton1kz = types.InlineKeyboardButton(text = 'Кері байланыс нысаны', url='tiny.cc/skillcup')
otherMarkupkz.add(otherButton1kz, gobackButtonkz)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Тілді таңдаңыз:/Выберите язык:',reply_markup = languageMarkup)


@bot.callback_query_handler(func = lambda call:True)
def callback_inline(call):
    if call.message:
        if call.data == 'kz':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Қош келдіңіз! Сізге қандай көмек көрсете аламын?", reply_markup = startMarkupkz)
        elif call.data == 'ru':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Добро пожаловать! Чем я могу вам помочь?", reply_markup = startMarkup)
        elif call.data == 'zoomru':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Видеоинструкции по ZOOM:", reply_markup = zoomMarkupru)
        elif call.data == 'skillcupru':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Видеоинструкции по Skill Cup:", reply_markup = skillcupMarkupru)
        elif call.data == 'otherru':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Если у вас возникли вопросы, вы можете обратиться за помощью по адресу: tiny.cc/skillcup", reply_markup = otherMarkupru)
        elif call.data == 'gobackru':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Добро пожаловать! Чем я могу вам помочь?", reply_markup = startMarkup)
        elif call.data == 'zoomkz':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="ZOOM үшін бейне нұсқаулар:", reply_markup = zoomMarkupkz)
        elif call.data == 'skillcupkz':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Skill Cup үшін бейне нұсқаулар:", reply_markup = skillcupMarkupkz)
        elif call.data == 'otherkz':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Егер сізде сұрақтар туындаса, tiny.cc/skillcup сайтынан көмек сұрай аласыз:", reply_markup = otherMarkupkz)
        elif call.data == 'gobackkz':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Қош келдіңіз! Сізге қандай көмек көрсете аламын?", reply_markup = startMarkupkz)
        elif call.data == 'lang':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Тілді таңдаңыз:/Выберите язык:',reply_markup = languageMarkup)

bot.remove_webhook()

time.sleep(0.1)

# Set webhook
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

# Start flask server
app.run(host=WEBHOOK_LISTEN, port=WEBHOOK_PORT, ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV), debug = True)
