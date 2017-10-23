from language import user_locale
from utils.utils import dev_only
from telegram.parsemode import ParseMode
from telegram.ext import CommandHandler
from telegram.vendor.ptb_urllib3.urllib3 import PoolManager
from config import POEDITOR_WEBHOOK
from shared_vars import dispatcher


@user_locale
@dev_only
def update_language_callback(bot, update):
    r = PoolManager()
    result = r.request('GET', POEDITOR_WEBHOOK)
    update.message.reply_rext("`{}`".format(result.reason), parse_mode=ParseMode.MARKDOWN)
    return


def register():
    dispatcher.add_handler(CommandHandler("updatelang", update_language_callback))
