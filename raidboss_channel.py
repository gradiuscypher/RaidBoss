#!/usr/bin/env python

import discord
import configparser
from libs import raid_combat

# Setup the config and Discord client
config = configparser.RawConfigParser()
config.read('config.conf')
client = discord.Client()

# create the dict of combat managers for each server
combat_managers = {}


@client.event
async def on_ready():
    """
    Fires when the account is logged in.
    :return:
    """
    print('Logged in as {} with the ID {}\n'.format(client.user.name, client.user.id))
    # setup a combat manager for each server connected
    for server in client.servers:
        combat_managers[server.name] = raid_combat.CombatManager(client, server)


@client.async_event
async def on_message(message):
    """
    Fires when a message is received.
    :param message: Discord message object
    :return:
    """
    if message.content == '!test':
        await combat_managers[message.server.name].start_combat()


@client.async_event
async def on_reaction_add(reaction, user):
    # await client.send_message(reaction.message.channel, "{} reacted with {}".format(user.name, reaction.emoji))
    if client.user != user:
        await combat_managers[reaction.message.server.name].route_action(reaction, user)
        await client.remove_reaction(reaction.message, reaction.emoji, user)


if __name__ == '__main__':
    token = config.get('Account', 'token')
    client.run(token)
