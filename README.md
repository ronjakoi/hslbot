# HSLbot

HSLbot is an IRC bot for finding public transportation routes in the Helsinki, Finland metropolitan area.
It uses publicly available JSON and GraphQL [APIs](https://digitransit.fi/en/developers/).

You can try the bot on IRCnet with the command `/query hslbot !help route`.

You are also welcome to join the `#hslbot` channel.

## Requirements

IRCbot is only tested on Python 3. It may work on Python 2, but I have no idea.

Packages used:

* irc3
* requests
* objectpath
## Usage

```bash
virtualenv -p python3 .
. bin/activate
pip3 install -r requirements.txt
```

At this point you want to edit your `config.ini` to configure the bot's nick, which server to connect to, etc.

Lastly:

```bash
irc3 config.ini
```

## Command syntax

Querying routes is done with the command `!route`. The bot responds with a NOTICE.

Type `!help route` for the command syntax.

## TODO

* Support for route times other than "depart now".
* Other options?
