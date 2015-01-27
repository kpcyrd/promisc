Promisc
=======

cjdns peering bot

Installation
------------

This bot uses [yrd](https://github.com/kpcyrd/yrd) for authorization. You need to install it first.

```
sudo apt-get install python-irc
```

The user running this bot needs read access to `/var/lib/yrd/cjdroute.conf` and write access to `/var/lib/yrd/peers.d/`.

Usage
-----

Edit the configuration file at `config.cfg`.

Next, just start the bot.

```
./promisc.py
```

The bot does not fork, so run it in screen or tmux.

License
-------

GPLv3
