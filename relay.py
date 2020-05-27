# coding=utf-8
"""
relay.py - Sopel Relay Module
Copyright 2020, Natalie Fearnley

http://sopel.chat
"""
from __future__ import unicode_literals, absolute_import, print_function
import functools
import logging
import re

from sopel.module import rule, require_chanmsg, unblockable
from sopel.trigger import PreTrigger

LOGGER = logging.getLogger("sopel.relay")
FORMATTING_RE = re.compile(r"\x1f|\x02|\x12|\x0f|\x16|\x03(?:\d{1,2}(?:,\d{1,2})?)?")


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
@unblockable
def keyword_match(bot, trigger):
    channel = trigger.sender
    nick, message = trigger.groups()
    nick = FORMATTING_RE.sub('', nick)
    LOGGER.debug("NICK")
    LOGGER.debug(f"{nick}")
    pretrigger = PreTrigger(bot.nick, f":{nick}!{nick}@discord.com PRIVMSG {channel} :{message}")
    bot.dispatch(pretrigger)
