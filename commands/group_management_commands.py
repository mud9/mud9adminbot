from language import _, user_locale, group_locales
from utils import (escape_md, dev_only, group_admin_only, if_group_admin,
                   mention, groups_only_response, pm_only_response)
from telegram.parsemode import ParseMode
import datetime
from telegram.ext import CommandHandler, Filters
from shared_vars import dispatcher
from shared_vars import User as DBUser


@group_locales
@groups_only_response
@group_admin_only
def ban_callback(bot, update, args):
    chat_id = update.effective_chat.id
    user = update.effective_user
    if update.effective_message.reply_to_message:
        to_user = update.effective_message.reply_to_message.from_user
        db_user = DBUser.from_tg_user_object(to_user)
    else:
        if not args:
            update.effective_message.reply_text(_("Reply to someone or use `/ban username/id`."),
                                                parse_mode=ParseMode.MARKDOWN)
            return
        else:
            try:
                to_user_id = int(args[0])
                db_user = DBUser.from_user_id(to_user_id)
                if not db_user:
                    update.effective_message.reply_text(_("Sorry, I probably have never seen this user."))
                    return
            except ValueError:
                to_user_username = args[0]
                if not args[0].startswith("@"):
                    update.effective_message.reply_text(_("Reply to someone or use `/ban username/id`."),
                                                        parse_mode=ParseMode.MARKDOWN)
                    return
                else:
                    to_user_username = to_user_username[1:]
                db_user = DBUser.from_username(to_user_username)
                if not db_user:
                    update.effective_message.reply_text(_("Sorry, I probably have never seen this user."))
                    return
    if if_group_admin(bot, chat_id, db_user.telegramid):
        update.effective_message.reply_text(_("You cannot ban an admin!"))
        return
    else:
        bot.kick_chat_member(chat_id, db_user.telegramid)
        update.effective_message.reply_text(
            _("{0} (`{1}`) has been banned by {2}.").format(db_user.markdown_first,
                                                            db_user.telegramid,
                                                            user.mention_markdown(user.first_name)),
            parse_mode=ParseMode.MARKDOWN)
        return


@group_locales
@groups_only_response
@group_admin_only
def kick_callback(bot, update):
    chat_id = update.effective_chat.id
    user = update.effective_user
    if update.effective_message.reply_to_message:
        to_user = update.effective_message.reply_to_message.from_user
    if if_group_admin(bot, chat_id, to_user.id):
        update.effective_message.reply_text(_("You cannot kick an admin!"))
        return
    else:
        bot.kick_chat_member(chat_id, to_user.id)
        bot.unban_chat_member(chat_id, to_user.id)
        update.effective_message.reply_text(
            _("{0} (`{1}`) has been kicked by {2}.").format(to_user.mention_markdown(to_user.first_name),
                                                            to_user.id,
                                                            user.mention_markdown(user.first_name)),
            parse_mode=ParseMode.MARKDOWN)
        return


def secret_unban(bot, job):
    chat_id, user_id = job.context
    bot.unban_chat_member(chat_id, user_id)
    return


@group_locales
@groups_only_response
@group_admin_only
def tempban_callback(bot, update, args, job_queue):
    chat_id = update.effective_chat.id
    user = update.effective_user
    temptime = 10
    if args:
        try:
            temptime = int(args[0])
        except ValueError:
            temptime = 10
    if update.effective_message.reply_to_message:
        to_user = update.effective_message.reply_to_message.from_user
    if if_group_admin(bot, chat_id, to_user.id):
        update.effective_message.reply_text(_("You cannot tempban an admin!"))
        return
    else:
        now = datetime.datetime.now().replace(microsecond=0)
        temp = now + datetime.timedelta(minutes=temptime)
        bot.kick_chat_member(chat_id, to_user.id)
        job_queue.run_once(secret_unban, temp, context=(chat_id, to_user.id))
        update.effective_message.reply_text(
            _("{0} (`{1}`) has been tempbanned "
              "by {2} for {3} minutes.").format(to_user.mention_markdown(to_user.first_name),
                                                to_user.id,
                                                user.mention_markdown(user.first_name),
                                                temptime),
            parse_mode=ParseMode.MARKDOWN)
        return


@group_locales
@groups_only_response
@group_admin_only
def unban_callback(bot, update):
    chat_id = update.effective_chat.id
    user = update.effective_user
    if update.effective_message.reply_to_message:
        to_user = update.effective_message.reply_to_message.from_user
    if if_group_admin(bot, chat_id, to_user.id):
        update.effective_message.reply_text(_("You cannot ban an admin!"))
        return
    else:
        bot.unban_chat_member(chat_id, to_user.id)
        update.effective_message.reply_text(
            _("{0} (`{1}`) has been unbanned by {2}.").format(to_user.mention_markdown(to_user.first_name),
                                                              to_user.id,
                                                              user.mention_markdown(user.first_name)),
            parse_mode=ParseMode.MARKDOWN)
        return


def register():
    dispatcher.add_handler(CommandHandler("ban", ban_callback, pass_args=True))
    dispatcher.add_handler(CommandHandler("kick", kick_callback))
    dispatcher.add_handler(CommandHandler("tempban", tempban_callback, pass_args=True,
                                          pass_job_queue=True))
    dispatcher.add_handler(CommandHandler("unban", unban_callback))
