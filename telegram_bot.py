from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from io import BytesIO

chatID = 1848570232
updateID = 888098247
token = '5102092002:AAGoNcOJ8ob-3t4dPzztIb7KBKBg3IcTMzM'

def send_document(doc_filename='test.txt', message='test'):
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    context = CallbackContext(dispatcher)
    context.bot.send_message(chat_id=chatID, text=message)
    with open(doc_filename, 'rb') as tmp:
        obj = BytesIO(tmp.read())
        obj.name = doc_filename
        # bot.send_document(message.from_user.id, data=obj, caption='your file')
        context.bot.sendDocument(chat_id=chatID, document=obj)

    updater.start_polling()
    updater.stop()



def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    #print(update.effective_chat.id)
    #print(update.update_id)
    #context.bot.send_message(chat_id=chatID, text=update.message.text)

def caps(update: Update, context: CallbackContext):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

def test_bot():
    updater = Updater(token=token, use_context=True)

    #start_handler = CommandHandler('start', start)
    dispatcher = updater.dispatcher
    #dispatcher.add_handler(start_handler)

    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    context = CallbackContext(dispatcher)
    context.bot.send_message(chat_id=chatID, text='test message')
    with open('test.txt', 'rb') as tmp:
        obj = BytesIO(tmp.read())
        obj.name = 'test.txt'
        #bot.send_document(message.from_user.id, data=obj, caption='your file')
        context.bot.sendDocument(chat_id=chatID, document=obj)

    #print(updater.bot())

    #caps_handler = CommandHandler('caps', caps)
    #dispatcher.add_handler(caps_handler)

    updater.start_polling()
    updater.stop()

def test_bot2():
    send_document()


if __name__ == '__main__':
    test_bot2()