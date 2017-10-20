import logging

from telegram.ext import CommandHandler, Filters

from commands import basic_commands, group_management_commands
from shared_vars import updater, dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)


def error_handler(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    dispatcher.add_handler(CommandHandler("start", basic_commands.start_callback, filters=Filters.private))
    dispatcher.add_handler(CommandHandler("test", basic_commands.test_callback, filters=Filters.group))
    dispatcher.add_handler(CommandHandler("system", basic_commands.system_callback))
    dispatcher.add_handler(CommandHandler("settings", basic_commands.group_settings_callback))
    # group man
    dispatcher.add_handler(CommandHandler("ban", group_management_commands.ban_callback))
    dispatcher.add_handler(CommandHandler("kick", group_management_commands.kick_callback))
    dispatcher.add_handler(CommandHandler("tempban", group_management_commands.tempban_callback, pass_args=True,
                                          pass_job_queue=True))
    dispatcher.add_handler(CommandHandler("unban", group_management_commands.unban_callback))
    dispatcher.add_error_handler(error_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
