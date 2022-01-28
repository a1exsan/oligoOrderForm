from telegram.ext import Updater
from telegram.ext import CallbackContext
from io import BytesIO

def send_document(doc_filename='test.txt', message='test', token='', chat_id=''):
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    context = CallbackContext(dispatcher)
    context.bot.send_message(chat_id=chat_id, text=message)
    with open(doc_filename, 'rb') as tmp:
        obj = BytesIO(tmp.read())
        obj.name = doc_filename
        context.bot.sendDocument(chat_id=chat_id, document=obj)

    updater.start_polling()
    updater.stop()

def test_bot2():
    send_document()


if __name__ == '__main__':
    test_bot2()