# encoding: utf-8
from telegram.ext import CommandHandler

def main(dispatcher):
    help_handler = CommandHandler('help', help)
    dispatcher.add_handler(help_handler)
    
def help(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                    text="""Puedes usar los siguientes comandos: \n- /help ayuda y explicación de los comandos a usar \n- /login para iniciar sesión\n- /poll para crear una nueva votación""")