from language import _, user_locale, group_locales
from utils import (escape_md, dev_only, group_admin_only, if_group_admin,
                   mention, groups_only_response, pm_only_response)
from telegram.parsemode import ParseMode
from shared_vars import dispatcher
from telegram.ext import CommandHandler, MessageHandler, Filters
from shared_vars import User as DBUser
from shared_vars import Group as DBGroup
import re
from telegram.error import BadRequest
from telegram import User, Chat


@group_locales
@groups_only_response
@group_admin_only
def setwelcome_callback(bot, update, args):
    if not args:
        update.effective_message.reply_text(_("Please enter your desired welcome message."))
        return
    msg = update.effective_message
    grp = DBGroup.from_tg_chat_object(update.effective_chat)
    welcome_msg = msg.text.split(None, 1)[1]
    try:
        sent = msg.reply_text(welcome_msg, parse_mode=ParseMode.MARKDOWN,
                              disable_web_page_preview=True)
        sent.edit_text(_("Group welcome has been saved."))
        grp.setwelcome(welcome_msg)
    except BadRequest as e:
        if 'parse entities' in e.message:
            msg.reply_text(_("Group welcome cannot be saved, there is probably some markdown error."))
        else:
            raise BadRequest


@group_locales
def send_welcome_callback(bot, update):
    chat = update.effective_chat
    grp = DBGroup.from_tg_chat_object(chat)
    if not grp.welcome:
        return
    for user in update.effective_message.new_chat_members:
        to_send = replace_welcome_vars(user, chat, grp.welcome)
        update.effective_message.reply_text(to_send, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True,
                                            quote=False)


def replace_welcome_vars(user: User, chat: Chat, text: str):
    if user.username:
        text = text.replace("$username", "@" + escape_md(user.username))
    text = text.replace("$firstname", escape_md(user.first_name))
    text = text.replace("$name", escape_md(user.first_name) if not user.last_name else "{} {}".format(
        escape_md(user.first_name), escape_md(user.last_name)))
    text = text.replace("$title", escape_md(chat.title))
    text = text.replace("$id", str(user.id))
    return text


def register():
    dispatcher.add_handler(CommandHandler("setwelcome", setwelcome_callback, pass_args=True))
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, send_welcome_callback))
