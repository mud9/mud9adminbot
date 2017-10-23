#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Telegram bot to play UNO in group chats
# Copyright (c) 2016 Jannes Höke <uno@jhoeke.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import gettext
from functools import wraps

from locales import available_locales as available
from shared_vars import User as UserSetting
from shared_vars import Group as GroupSetting

GETTEXT_DOMAIN = 'mud9admin'
GETTEXT_DIR = 'locales'


class _Underscore(object):
    """Class to emulate flufl.i18n behaviour, but with plural support"""
    def __init__(self):
        self.translators = {
            locale: gettext.GNUTranslations(
                open(gettext.find(
                    GETTEXT_DOMAIN, GETTEXT_DIR, languages=[locale]
                ), 'rb')
            )
            for locale
            in available.keys()
            if locale != 'en_US'  # No translation file for en_US
        }
        self.locale_stack = list()

    def push(self, locale):
        self.locale_stack.append(locale)

    def pop(self):
        if self.locale_stack:
            return self.locale_stack.pop()
        else:
            return None

    @property
    def code(self):
        if self.locale_stack:
            return self.locale_stack[-1]
        else:
            return None

    def __call__(self, singular, plural=None, n=1, locale=None):
        if not locale:
            locale = self.locale_stack[-1]

        if locale not in self.translators.keys():
            if n is 1:
                return singular
            else:
                return plural

        translator = self.translators[locale]

        if plural is None:
            return translator.gettext(singular)
        else:
            return translator.ngettext(singular, plural, n)

_ = _Underscore()


def __(singular, plural=None, n=1, multi=False):
    """Translates text into all locales on the stack"""
    translations = list()

    if not multi and len(set(_.locale_stack)) >= 1:
        translations.append(_(singular, plural, n, 'en_US'))

    else:
        for locale in _.locale_stack:
            translation = _(singular, plural, n, locale)

            if translation not in translations:
                translations.append(translation)

    return '\n'.join(translations)


def user_locale(func):
    @wraps(func)
    def wrapped(bot, update, *pargs, **kwargs):
        user, chat = _user_chat_from_update(update)

        us = UserSetting.from_tg_user_object(user)

        if us and us.lang != 'en_US':
            _.push(us.lang)
        else:
            _.push('en_US')

        result = func(bot, update, *pargs, **kwargs)
        _.pop()
        return result
    return wrapped


def group_locales(func):
    @wraps(func)
    def wrapped(bot, update, *pargs, **kwargs):
        user, chat = _user_chat_from_update(update)
        locales = list()

        if chat.type == 'private':
            us = UserSetting.from_tg_user_object(user)
        else:
            us = GroupSetting.from_tg_chat_object(chat)

        if us and us.lang != 'en_US':
            loc = us.lang
        else:
            loc = 'en_US'

        _.push(loc)
        locales.append(loc)

        result = func(bot, update, *pargs, **kwargs)

        while _.code:
            _.pop()

        return result
    return wrapped


def _user_chat_from_update(update):
    user = update.effective_user
    chat = update.effective_chat
    return user, chat
