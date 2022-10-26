#!/usr/bin/env python3
import datetime
import os
from typing import List, Callable, Tuple, Any

from twitchio import Channel, User, Message, Client
from twitchio.ext import commands, routines
from twitchio.ext.commands import Command, Context

from utils import now


class TeraBot(commands.Bot):

    def __init__(self):
        super().__init__(
            token=os.getenv('TWITCH_TOKEN'),
            prefix='!',
            initial_channels=[os.getenv('TWITCH_CHANNEL')],
        )

    # Called once the bot is ready, seems to be executed after event_join
    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'user id is | {self.user_id}')

    # Called whenever someone joins the channel
    async def event_join(self, channel: Channel, user: User):
        print(f'{datetime.datetime.now()} {self.nick} joined {channel.name}')

    async def event_message(self, message: Message) -> None:
        """runs every time a message is sent"""

        if message.echo:
            return

        await self.handle_commands(message)

        print(f'{now()} "{message.content}" sent by {message.author.name}')

        # Get the context directly from the bot
        # ctx = await self.get_context(message)
        print(f'{message.tags}')

        ctx = await self.get_context(message)

        if message.tags['user-type'] == 'mod':
            await ctx.send(f'Oh look its another mod.. how original : {message.author.name}')
        else:
            if 'broadcaster' not in message.tags['badges']:
                await ctx.send('regular user, how .. regular?')

        if 'tera' in message.content.lower():
            await ctx.send("tera blah blah blah")

    async def event_command_error(self, context: Context, error: Exception) -> None:
        # TODO: punish spammers of invalid commands. Maybe more than 5 within X seconds
        # TODO: Log to log file for bot
        print(f'{now()} ({error.args[0]}) sent by {context.author.name}')

        await context.send(f"Invalid command {context.message.content}")

    # @routines.routine(seconds=30, iterations=2)
    # async def dosomething(self, arg: str):
    #     print(f'Something happening here every 30s {arg}')
    #
    # @dosomething.after_routine
    # async def afterstuff(self):
    #     print(f'This happened after the routine')
    #
    # @dosomething.before_routine
    # async def beforestuff(self):
    #     print(f'this is doing some stuff before the routine')

    @commands.command()
    async def hello(self, ctx: Context):
        await ctx.send(f'Hello {ctx.author.name}!')

        users = await self.get_webhook_subscriptions()
        print(f'{users}')

    @commands.command(name="register", aliases=['reg', 'signup', 'create'])
    async def register(self, ctx: Context):
        print(f'Registering a new user.... {ctx.author.name}')
        await ctx.send(f'Registered user {ctx.author.name}')

    @commands.command(name="chatters")
    async def chatters(self, ctx: Context):
        users = tuple(i.name for i in ctx.chatters)
        await ctx.send(f'Currently we have {len(users)} people chatting. {users}')


if __name__ == '__main__':
    bot = TeraBot()


    # this is a blocking call which starts your bot
    bot.run()
