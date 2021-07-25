import time
from django.core.management.base import BaseCommand
from django.conf import settings
from telegram.utils.request import Request as TelegramRequest
from telegram import Bot, Update, message, ForceReply
from telegram.ext import CallbackContext, Filters, MessageHandler, Updater
from telegram.ext import CommandHandler
from tasks.models import Customer, Task


def log_errors(f):

    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Error: {e}'
            print(error_message)
            raise e

    return inner


@log_errors
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    text = '''
    Welcome! Here you will get updates on your tasks.
If you are not registered please enter your phone.'''
    update.message.reply_text(
        text=text,
    )


@log_errors
def get_tasks(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    phone = update.message.text

    customer, _ = Customer.objects.get_or_create(
        telegram_id=chat_id,
        defaults={
            'name': update.message.from_user.name,
            'phone': phone,
        }
    )

    queryset = Task.objects.filter(customer=customer).values()
    results = [(task['id'], task['status']) for task in queryset]

    if len(queryset) != 0:
        def get_results():
            msg = ''
            for task in results:
                id, status = task
                msg += f"\nID: {id} - Status: {status}"
            return msg

        reply_text = f"Your requests:\n{get_results()}"
        update.message.reply_text(text=reply_text)
    else:
        reply_text = f"No requests yet."
        update.message.reply_text(text=reply_text)

    # check every 10 seconds if status changed
    while True:

        time.sleep(10)

        updated_queryset = Task.objects.filter(customer=customer).values()
        update_results = [(task['id'], task['status'])
                          for task in updated_queryset]

        if results != update_results:
            results = update_results
            new_results = get_results()

            new_text = f"Your requests changed status:\n{new_results}"
            update.message.reply_text(text=new_text)


class Command(BaseCommand):
    help = 'Telegram-bot'

    def handle(self, *args, **kwargs):
        # connection
        task = TelegramTask(
            connect_timeout=1.0,
            read_timeout=2.0,
        )
        bot = Bot(
            task=task,
            token=settings.TOKEN,
        )

        print(bot.get_me())

        # handlers
        updater = Updater(
            bot=bot,
            use_context=True,
        )

        message_handler = MessageHandler(Filters.text, get_tasks)
        updater.dispatcher.add_handler(CommandHandler("start", start))
        updater.dispatcher.add_handler(message_handler)

        updater.start_polling()
        updater.idle()
