from language import _, user_locale, group_locales
from utils.utils import (escape_md, dev_only, group_admin_only, if_group_admin, pass_db,
                         mention, groups_only_response, pm_only_response, check_group_link, link_markdown)
from telegram.parsemode import ParseMode
import datetime
from telegram.ext import CommandHandler
from telegram.error import BadRequest
from shared_vars import dispatcher, Session
from shared_vars import Group as GroupSetting


@group_locales
@groups_only_response
@group_admin_only
@pass_db(chat_only=True)
def setlink_callback(bot, update, grp, args):
    chat = update.effective_chat
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
                                        parse_mode=ParseMode.MARKDOWN,
                                        disable_web_page_preview=True)


@group_locales
@groups_only_response
@pass_db(chat_only=True)
def link_callback(bot, update, grp):
    chat = update.effective_chat
    if chat.username:
        link = "https://t.me/{}".format(chat.username)
        grp.setlink(link)
    if grp.link:
        update.effective_message.reply_text(_("This is the group link: {}").format(link_markdown(chat.title, grp.link)),
                                            parse_mode=ParseMode.MARKDOWN,
                                            disable_web_page_preview=True)
    else:
        update.effective_message.reply_text(_("The group link has not been set yet."))
    return


@group_locales
@groups_only_response
@group_admin_only
@pass_db(chat_only=True)
def setinfo_callback(bot, update, grp, args):
    msg = update.effective_message
    if msg.reply_to_message:
        msg = msg.reply_to_message
        md_text = msg.text_markdown
    else:
        if not args:
            msg.reply_text(_("Please reply to an old message or use `/setinfo something here`."),
                           parse_mode=ParseMode.MARKDOWN)
            return
        else:
            md_text = msg.text.split(None, 1)[1]
    try:
        sent = msg.reply_text(md_text, parse_mode=ParseMode.MARKDOWN,
                              disable_web_page_preview=True)
        sent.edit_text(_("Group info has been saved."))
        grp.setinfo(md_text)
    except BadRequest as e:
        if 'parse entities' in e.message:
            msg.reply_text(_("Group info cannot be saved, there is probably some markdown error."))
        else:
            raise BadRequest


@group_locales
@groups_only_response
@pass_db(chat_only=True)
def info_callback(bot, update, grp):
    msg = update.effective_message
    if not grp.info:
        msg.reply_text(_("Info has not been set in this group."))
        return
    else:
        try:
            msg.reply_text(_("*Group Info*:\n{}").format(grp.info), parse_mode=ParseMode.MARKDOWN,
                           disable_web_page_preview=True)
        except BadRequest as e:
            if 'too long' in e.message:
                msg.reply_text(_("The saved info message was too long. Please `/setinfo` again."),
                               parse_mode=ParseMode.MARKDOWN)
                return
            else:
                raise BadRequest
        return


@group_locales
@groups_only_response
@group_admin_only
@pass_db(chat_only=True)
def setrules_callback(bot, update, grp, args):
    msg = update.effective_message
    if msg.reply_to_message:
        msg = msg.reply_to_message
        md_text = msg.text_markdown
    else:
        if not args:
            msg.reply_text(_("Please reply to an old message or use `/setrules something here`."),
                           parse_mode=ParseMode.MARKDOWN)
            return
        else:
            md_text = msg.text.split(None, 1)[1]
    try:
        sent = msg.reply_text(md_text, parse_mode=ParseMode.MARKDOWN,
                              disable_web_page_preview=True)
        sent.edit_text(_("Group rules has been saved."))
        grp.setrules(md_text)
    except BadRequest as e:
        if 'parse entities' in e.message:
            msg.reply_text(_("Group rules cannot be saved, there is probably some markdown error."))
        else:
            raise BadRequest


@group_locales
@groups_only_response
@pass_db(chat_only=True)
def rules_callback(bot, update, grp):
    msg = update.effective_message
    if not grp.rules:
        msg.reply_text(_("Rules has not been set in this group."))
        return
    else:
        try:
            msg.reply_text(_("*Group Rules*:\n{}").format(grp.rules), parse_mode=ParseMode.MARKDOWN,
                           disable_web_page_preview=True)
        except BadRequest as e:
            if 'too long' in e.message:
                msg.reply_text(_("The saved rules message was too long. Please `/setinfo` again."),
                               parse_mode=ParseMode.MARKDOWN)
                return
            else:
                raise BadRequest
        return


def register():
    dispatcher.add_handler(CommandHandler("setlink", setlink_callback, pass_args=True))
    dispatcher.add_handler(CommandHandler("link", link_callback))
    dispatcher.add_handler(CommandHandler("setinfo", setinfo_callback, pass_args=True))
    dispatcher.add_handler(CommandHandler("info", info_callback))
    dispatcher.add_handler(CommandHandler("setrules", setrules_callback, pass_args=True))
    dispatcher.add_handler(CommandHandler("rules", rules_callback))
