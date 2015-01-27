#!/usr/bin/env python
from ConfigParser import RawConfigParser
from irc.bot import SingleServerIRCBot
from subprocess import check_output, check_call
import re
import os

TRIGGER = 'peer pl0x'
CJDROUTE = '/var/lib/yrd/cjdroute.conf'
PEERS = '/var/lib/yrd/peers.d/'


def check(title, verb, flag):
    if flag:
        print('[+] %s is %s' % (title, verb))
    else:
        print('[-] %s is not %s' % (title, verb))
    return flag


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
            print('[*] authorizing %r' % nick)
            out = check_output(['yrd', 'peer', 'auth', nick]).split('\n')
            c.privmsg(nick, out[0])
            c.privmsg(nick, out[2])
        else:
            c.privmsg(nick, 'not understood, type %r' % TRIGGER)

    def on_pubmsg(self, c, e):
        if e.arguments[0] == '!peers':
            c.privmsg(self.channel, 'likes to peer')


def main():
    config = RawConfigParser()
    config.read('config.cfg')

    if not check('yrd', 'there', not check_call(['which', 'yrd'])):
        return

    if not check(CJDROUTE, 'accessible', os.access(CJDROUTE, os.R_OK)):
        return

    if not check(PEERS, 'writable', os.access(PEERS, os.W_OK)):
        return

    server = config.get('promisc', 'host')
    port = config.getint('promisc', 'port')
    channel = config.get('promisc', 'channel')

    nick = config.get('promisc', 'nick')
    realname = config.get('promisc', 'realname')

    bot = Promisc(server, channel, nick, realname, port)
    print('[*] starting...')
    bot.start()


if __name__ == '__main__':
    main()
