# encoding: utf-8
from telegram.ext import (CommandHandler, Filters, ConversationHandler, MessageHandler)
# import utils.logger as logger

DESCRIPTION, QUESTION = range(2)

def name(bot,update):
     update.message.reply_text('Vas a crear una nueva votación. En primer lugar, indica el nombre de la misma :)')

     return ConversationHandler.DESCRIPTION

def description(bot,update):
#     logger.info("Name of poll: %s", update.message.text)
     update.message.reply_text('¡De acuerdo! A continuación, indica la descripción.')

     return ConversationHandler.QUESTION

def question(bot,update):
#     logger.info("Description of poll: %s", update.message.text)
     update.message.reply_text('Todo listo, ¡nos vemos!')

     return ConversationHandler.END
	
def cancel(bot, update):
     user = update.message.from_user
     update.message.reply_text('La creación de la votación se ha cancelado :(')

     return ConversationHandler.END

def main(dispatcher):
     # start_handler = CommandHandler('poll', poll)
     # dispatcher.add_handler(start_handler)
     conv_handler = ConversationHandler(
     states={
          DESCRIPTION: [MessageHandler(Filters.text, description)],

          QUESTION: [MessageHandler(Filters.text, question)],
     },

     fallbacks=[CommandHandler('cancel', cancel)]
     )
     dispatcher.add_handler(conv_handler)

     start_handler = CommandHandler('name', name)
     dispatcher.add_handler(start_handler)