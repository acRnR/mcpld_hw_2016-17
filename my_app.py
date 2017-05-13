import flask
import telebot
import conf

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN, threaded=False)
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет, я бот, который ничего не умеет, кроме как считать слова")


@bot.message_handler(func=lambda m: True)
def send_len(message):
    a = message.text.replace('.', ' ')
    a = a.replace(',', ' ')
    a = a.replace(';', ' ')
    a = a.replace(':', ' ')
    lnth = str(len(a.split()))
    if lnth[-1] == '1' and lnth != '11':
        word = ' слово'
    elif int(lnth[-1]) <= 4 and lnth != '12' and lnth != '13' and lnth != '14':
        word = ' слова'
    else:
        word = ' слов'
    n_words = lnth + word
    bot.send_message(message.chat.id, 'В этом сообщении {} :D'.format(n_words))


@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'


@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)
