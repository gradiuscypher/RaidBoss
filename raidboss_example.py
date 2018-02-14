#!/usr/bin/env python

import discord
import configparser

config = configparser.RawConfigParser()
config.read('config.conf')

client = discord.Client()


@client.event
async def on_ready():
    """
    Fires when the account is logged in.
    :return:
    """
    print('Logged in as {} with the ID {}\n'.format(client.user.name, client.user.id))


@client.async_event
async def on_message(message):
    """
    Fires when a message is received.
    :param message: Discord message object
    :return:
    """
    print(message.content)
    if message.content == '!startest':
        print("In start test.")
        embed_message = discord.Embed(title='Embed Title', color=discord.Color.red())
        embed_message.add_field(name='HP', value='50/50')
        embed_message.add_field(name='Target', value='Bob')
        embed_message.set_thumbnail(url='https://imgur.com/upKJXhH.png')
        embed_message.set_image(url='https://i.imgur.com/muX6mfe.png')
        embed_message.description = 'Test description.'
        embed_message.set_footer(text='Footer Text', icon_url='https://i.imgur.com/muX6mfe.png')
        message = await client.send_message(message.channel, embed=embed_message)
        await client.add_reaction(message, "\N{CROSSED SWORDS}")
        await client.add_reaction(message, "\N{LEFTWARDS BLACK ARROW}")
        await client.add_reaction(message, "\N{BLACK RIGHTWARDS ARROW}")


@client.async_event
async def on_reaction_add(reaction, user):
    await client.send_message(reaction.message.channel, "{} reacted with {}".format(user.name, reaction.emoji))
    if client.user != user:
        await client.remove_reaction(reaction.message, reaction.emoji, user)


@client.async_event
async def on_reaction_remove(reaction, user):
    await client.send_message(reaction.message.channel, "{} removed reaction {}".format(user.name, reaction.emoji))


if __name__ == '__main__':
    token = config.get('Account', 'token')
    client.run(token)
