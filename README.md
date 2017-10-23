# Mud9AdminBot
Mud9AdminBot is a group management telegram bot made by @Mud9 ([@Mud9BotDev]) in Python 3.


### Dependencies
----
This bot made use of [python-telegram-bot] as its framework with [mysql] as database backend.

* [python-telegram-bot] - The best Python framework for telegram bots!
* [PyMySQL] - Pure Python MySQL Client.
* [SQLAlchemy] - The Database Toolkit for Python - used for SQL connection pooling.
* [pytz] - Timezone management.
* [polib] - Internationalization management.

### Installation
----
Mud9AdminBot requires [Python] v3.3+ to run.

First, Clone the project and install the dependencies. (If `pip` fails, you may have to use `pip3`.) A virtual environment is recommended.


```bash
$ git clone https://github.com/mud9/mud9adminbot/mud9adminbot.git
$ cd mud9adminbot
$ pip install -r requirements.txt
$ cp config_example.py config.py
```

Edit your new copied `config.py` and include your telegram bot token (You can get one from [@botfather](https://t.me/botfather)), your telegram ID (send a message to [@UserInfoBot](https://t.me/userinfobot)), and your mysql server details.

```bash
$ nano config.py
```

All things set, fire up your bot!
```bash
$ python3 start_bot.py
```

### Translation
----
> To be continued.


### Todos
----
> To be continued.

### License
----
This project is on GPLv3. You are free to fork, clone and modify it as long as you keep it open-sourced.



   [python-telegram-bot]: <http://python-telegram-bot.org>
   [PyMySQL]: <https://github.com/PyMySQL/PyMySQL>
   [SQLAlchemy]: <https://www.sqlalchemy.org/>
   [pytz]: <https://pypi.python.org/pypi/pytz>
   [polib]: <https://pypi.python.org/pypi/polib>
   [Python]: <https://www.python.org/>
   [@Mud9BotDev]: <https://t.me/mud9botdev>

