from language import _, user_locale, group_locales
from utils import escape_md, dev_only, group_admin_only, groups_only_response, pm_only_response
from shared_vars import dispatcher
from telegram.ext import CommandHandler, Filters


@user_locale
@pm_only_response
def start_callback(bot, update):
    update.message.reply_text(_("Thank you for starting me!"))


@group_locales
def test_callback(bot, update):
    update.message.reply_text(_("This is a test!"))


@user_locale
@dev_only
def system_callback(bot, update):
    update.message.reply_text(_("Pong!"))


@group_locales
@group_admin_only
def group_settings_callback(bot, update):
    update.message.reply_text(_("Nothing to set now."))


def register():
    dispatcher.add_handler(CommandHandler("start", start_callback))
    dispatcher.add_handler(CommandHandler("test", test_callback))
    dispatcher.add_handler(CommandHandler("system", system_callback))
    dispatcher.add_handler(CommandHandler("settings", group_settings_callback))
