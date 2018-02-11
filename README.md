# HSLbot

HSLbot is an IRC bot for finding public transportation routes in the Helsinki, Finland metropolitan area.
It uses publicly available JSON and GraphQl APIs.

## Usage

```bash
virtualenv -p python3
. bin/activate
pip3 -r requirements.txt
```

At this point you want to edit your `config.ini` to configure the bot's nick, which server to connect to, etc.

Lastly:

```bash
irc3 config.ini
```