import subprocess
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = '7305880074:AAH7QaJuWW2xpKbMQah5JtInxbGC7Doe9Ww'
BOT_USERNAME: Final = '@raratesttsstbot'

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Thanks for chatting with me.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I control the Minecraft server.')

async def startserver_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Starting Minecraft server...")
    subprocess.run(['python3', 'startmcserver.py'])

async def stopserver_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Stopping Minecraft server...')
    subprocess.run(['python3', 'stopmcserver.py'])

async def reloadserver_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Reloading Minecraft server...')
    subprocess.run(['python3', 'reloadserver.py'])

async def command_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.split(' ', 1)
    if len(user_input) != 2:
        await update.message.reply_text('Invalid command format. Please use: /command "your_command"')
        return

    command_to_run = user_input[1]

    try:
        subprocess.run(['screen', '-S', 'minecraft', '-p', '0', '-X', 'stuff', f'{command_to_run}\n'])
        await update.message.reply_text(f'Command "{command_to_run}" sent to Minecraft server.')
    except Exception as e:
        await update.message.reply_text(f'An error occurred: {e}')

def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hi' in processed:
        return 'hi'
    else:
        return 'I don\'t understand what you wrote.'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('startserver', startserver_command))
    application.add_handler(CommandHandler('stopserver', stopserver_command))
    application.add_handler(CommandHandler('reloadserver', reloadserver_command))
    application.add_handler(CommandHandler('command', command_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error)

    application.run_polling()

if __name__ == '__main__':
    print('Starting bot.')
    main()
