import subprocess
from typing import Final
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN: Final = 'bot token here'
BOT_USERNAME: Final = 'bot username here (@botsusername)'


def start_command(update: Update, context: CallbackContext):
    update.message.reply_text('Hello! Thanks for chatting with me.')

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text('I control the minecraft server')

def startserver_command(update: Update, context: CallbackContext):
    update.message.reply_text("Starting Minecraft server..")
    subprocess.run(['python3', 'startmcserver.py'])

def stopserver_command(update: Update, context: CallbackContext):
    update.message.reply_text('Stopping minecraft server..')
    subprocess.run(['python3', 'stopmcserver.py'])
    
def reloadserver_command(update: Update, context: CallbackContext):
    update.message.reply_text('Reloading minecraft server..')
    subprocess.run(['python3', 'reloadserver.py'])

def command_command(update: Update, context: CallbackContext):
    # Extract the command from the user's message
    user_input = update.message.text.split(' ', 1)
    if len(user_input) != 2:
        update.message.reply_text('Invalid command format. Please use: /command "your_command"')
        return

    command_to_run = user_input[1]

    try:
        # Run the command on the Minecraft server using the screen session
        subprocess.run(['screen', '-S', 'minecraft', '-p', '0', '-X', 'stuff', f'{command_to_run}\n'])
        update.message.reply_text(f'Command "{command_to_run}" sent to Minecraft server.')
    except Exception as e:
        update.message.reply_text(f'An error occurred: {e}')



def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hi' in processed:
        return 'hi'
    else:
        return 'I don\'t understand what you wrote.'

def handle_message(update: Update, context: CallbackContext):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:', response)
    update.message.reply_text(response)

def error(update: Update, context: CallbackContext):
    print(f'Update {update} caused error {context.error}')

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('startserver', startserver_command))
    dp.add_handler(CommandHandler('stopserver', stopserver_command))
    dp.add_handler(CommandHandler('reloadserver', reloadserver_command))
    dp.add_handler(CommandHandler('command', command_command))

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    print('Starting bot.')
    main()
