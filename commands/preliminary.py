from telegram.ext.dispatcher import run_async
from shared_vars import User as DBUser
from shared_vars import Group as DBGroup
from shared_vars import dispatcher
from telegram.ext import MessageHandler, Filters


@run_async
def process_message(bot, update):
    user = update.effective_user
    add_user(user)
    if update.effective_message.reply_to_message:
        user2 = update.effective_message.reply_to_message.from_user
        add_user(user2)
    if update.effective_chat.type != 'private':
        add_group(update.effective_chat)


def add_user(user):
    DBUser.from_tg_user_object(user)


def add_group(group):
    DBGroup.from_tg_chat_object(group)


def register():
    dispatcher.add_handler(MessageHandler(Filters.all, process_message), -1)
