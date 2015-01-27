#!/usr/bin/env python
from ConfigParser import RawConfigParser
from irc.bot import SingleServerIRCBot

TRIGGER = 'peer pl0x'


class Promisc(SingleServerIRCBot):
    def __init__(self, server, channel, nick, real, port=6667):
        SingleServerIRCBot.__init__(self, [(server, port)],
                                    nick, real)
        self.channel = channel

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + '_')

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        nick = e.source.nick
        msg = e.arguments[0]

        if not re.match('^[a-zA-Z0-9_]+$', nick):
            c.privmsg(nick, 'your nick looks too scary')
        elif msg == TRIGGER:
            c.privmsg(nick, 'generating credentials...')
            c.privmsg(nick, '> cjdns peer string')
            c.privmsg(nick, '> yrd command')
        else:
            c.privmsg(nick, 'not understood, type %r' % TRIGGER)

    def on_pubmsg(self, c, e):
        if e.arguments[0] == '!peers':
            c.privmsg(self.channel, 'likes to peer')


def main():
    config = RawConfigParser()
    config.read('config.cfg')

    server = config.get('promisc', 'host')
    port = config.getint('promisc', 'port')
    channel = config.get('promisc', 'channel')

    nick = config.get('promisc', 'nick')
    realname = config.get('promisc', 'realname')

    bot = Promisc(server, channel, nick, realname, port)
    print('starting...')
    bot.start()


if __name__ == '__main__':
    main()
