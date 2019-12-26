from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging, test
updater = Updater(token='TOKEN', use_context=True)

dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, lad! \nTo retrieve forecast, please, enter city name.\nNote, report generation takes time")

def help(update, context):
    update.message.reply_text("Use /start to test this bot.")

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=str(test.pusher(update.message.text)))


echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


updater.start_polling()



