# coding=utf-8
"""
relay.py - Sopel Relay Module
Copyright 2020, Natalie Fearnley

http://sopel.chat
"""
from __future__ import unicode_literals, absolute_import, print_function
import functools
import logging

from sopel.module import rule, require_chanmsg
from sopel.trigger import PreTrigger

LOGGER = logging.getLogger("sopel.relay")


def require_user(*users):
    """This command only responds to the specified user(s)
    """
    def actual_decorator(fn):
        @functools.wraps(fn)
        def guarded(bot, trigger, *args, **kwargs):
            if trigger.nick in users:
                return fn(bot, trigger, *args, **kwargs)
        return guarded
    return actual_decorator


@require_chanmsg()
@require_user("envoy")
@rule(r"^<([^>]*)> (.*)$")
def keyword_match(bot, trigger):
    channel = trigger.sender
    nick, message = trigger.groups()
    pretrigger = PreTrigger(bot.nick, f":{nick}!{nick}@discord.com PRIVMSG {channel} :{message}")
    bot.dispatch(pretrigger)
