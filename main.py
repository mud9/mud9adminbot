import logging
from shared_vars import updater, dispatcher
import polib
import pathlib
from commands import basic_commands, group_management_commands, group_info_commands


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


def error_handler(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))


def prepare():
    lst = sorted(pathlib.Path.cwd().glob("**/*.po"))
    for pth in lst:
        if pth.suffix == '.po':
            po = polib.pofile(str(pth))
            po.save_as_mofile(str(pth).replace(".po", ".mo"))


def main():
    # basic commands
    basic_commands.register()
    # group man
    group_management_commands.register()
    # group info
    group_info_commands.register()
    # error handler
    dispatcher.add_error_handler(error_handler)
    # start the bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
