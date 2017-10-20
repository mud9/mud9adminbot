from telegram.utils.helpers import escape_markdown as escape_md
from telegram.utils.helpers import mention_markdown as mention
from config import DEV
from functools import wraps
from mwt import MWT
from language import _


def dev_only(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in DEV:
            update.effective_message.reply_text(_("You are not a developer!"))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


def group_admin_only(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        if user_id not in group_admins(bot, chat_id):
            update.effective_message.reply_text(_("You are not an admin in this chat!"))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


@MWT(timeout=60*10)
def group_admins(bot, chat_id):
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]


def if_group_admin(bot, chat_id, user_id):
    return user_id in group_admins(bot, chat_id)

