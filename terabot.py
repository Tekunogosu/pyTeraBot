#!/usr/bin/env python3

import os
from twitchio.ext import commands

bot = commands.Bot(
    token=os.environ['OTHER_TOKEN'],
    irc_token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[os.environ['CHANNEL']]
)


@bot.event
async def event_ready():
    print(f"{os.environ['BOT_NICK']} is online!")
    ws = bot.ws
    await ws.send_privmsg(os.environ['CHANNEL'], f"/me has landed")


if __name__ == '__main__':
    bot.run()
