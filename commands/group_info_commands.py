from language import _, user_locale, group_locales
from utils import (escape_md, dev_only, group_admin_only, if_group_admin,
                   mention, groups_only_response, pm_only_response, check_group_link, link_markdown)
from telegram.parsemode import ParseMode
import datetime
from telegram.ext import CommandHandler
from shared_vars import dispatcher
from shared_vars import Group as GroupSetting


@group_locales
@groups_only_response
@group_admin_only
def setlink_callback(bot, update, args):
    chat = update.effective_chat
    grp = GroupSetting.from_tg_chat_object(chat)
    if chat.username:
        link = "https://t.me/{}".format(chat.username)
    else:
        if args:
            res = check_group_link(args[0])
            if res:
                link = res.group(0)
            else:
                update.effective_message.reply_text(_("The link you provided is invalid."))
                return
        else:
            update.effective_message.reply_text(_("Please provide the group link."))
            return
    grp.setlink(link)
    update.effective_message.reply_text(_("The link is set to: {}").format(link_markdown(chat.title, link)),
                                        parse_mode=ParseMode.MARKDOWN)


@group_locales
@groups_only_response
def link_callback(bot, update):
    chat = update.effective_chat
    grp = GroupSetting.from_tg_chat_object(chat)
    if chat.username:
        link = "https://t.me/{}".format(chat.username)
        grp.setlink(link)
    if grp.link:
        update.effective_message.reply_text(_("This is the group link: {}").format(link_markdown(chat.title, grp.link)),
                                            parse_mode=ParseMode.MARKDOWN)
    else:
        update.effective_message.reply_text(_("The group link has not been set yet."))
    return


@group_locales
@groups_only_response
@group_admin_only
def setinfo_callback(bot, update):
    pass


@group_locales
@groups_only_response
def info_callback(bot, update):
    pass


def register():
    dispatcher.add_handler(CommandHandler("setlink", setlink_callback, pass_args=True))
    dispatcher.add_handler(CommandHandler("link", link_callback))
    dispatcher.add_handler(CommandHandler("setinfo", setinfo_callback))
    dispatcher.add_handler(CommandHandler("info", info_callback))
