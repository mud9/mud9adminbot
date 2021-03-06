from telegram.utils.helpers import escape_markdown as escape_md
from telegram.utils.helpers import mention_markdown as mention
from config import DEV
from functools import wraps
from .mwt import MWT
from language import _
from shared_vars import Group as Grp, User as Usr
import re


def pass_db(chat_only=False, user_only=False):
    def pass_db_real(func):
        @wraps(func)
        def wrapped(bot, update, *args, **kwargs):
            usr = Usr.from_tg_user_object(update.effective_user)
            if not update.effective_chat.type == 'private':
                grp = Grp.from_tg_chat_object(update.effective_chat)
            else:
                grp = None
            if chat_only:
                return func(bot, update, grp, *args, **kwargs)
            if user_only:
                return func(bot, update, usr, *args, **kwargs)
            return func(bot, update, grp, usr, *args, **kwargs)
        return wrapped
    return pass_db_real


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


def groups_only_response(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        if update.effective_chat.type != 'group' and update.effective_chat.type != 'supergroup':
            update.effective_message.reply_text(_("This command can only be used in groups!"))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


def pm_only_response(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        if update.effective_chat.type != 'private':
            update.effective_message.reply_text(_("This command can only be used in PM!"))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


def check_group_link(link):
    pattern = "^(http:\/\/|https:\/\/)?t(elegram)?\.(me|dog)\/joinchat\/[a-zA-Z0-9-_]{22}$"
    return re.match(pattern, link)


def link_markdown(name, link):
    return "[{}]({})".format(escape_md(name), link)
