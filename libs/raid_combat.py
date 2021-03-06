import asyncio
import discord
import traceback
import json


class RaidMonster:
    def __init__(self, filename):
        """
        A representation of a RaidBoss monster
        :param filename: name of the monster file to load
        """
        # TODO: create a list of Discord Emojis to react with and store in this object rather than doing it later.
        # Iterate over this list and add all reactions
        monster = json.load(open('data/monsters/' + filename))

        self.name = monster['name']
        self.image = monster['image']
        self.current_hp = monster['max_hp']
        self.max_hp = monster['max_hp']
        self.current_target = None
        self.message_id = None


class CombatManager:
    def __init__(self, discord_client, discord_server):
        self.discord_client = discord_client
        self.discord_server = discord_server
        self.monsters = {}

        try:
            self.rb_channel = discord.utils.get(self.discord_server.channels, name='raidboss')
        except:
            print(traceback.format_exc())
            exit(1)

    def build_monster_embed(self, monster):
        """
        Takes input settings for building a monster embed and builds an Embed object out of it
        :param monster: dictionary of monster properties
        :return: Discord Embed
        """
        embed_message = discord.Embed(title=monster.name, color=discord.Color.red())
        embed_message.add_field(name='HP', value='{}/{}'.format(monster.current_hp, monster.max_hp))
        embed_message.add_field(name='Current Target', value=monster.current_target)
        embed_message.set_thumbnail(url=monster.image)

        return embed_message

    @asyncio.coroutine
    async def start_combat(self):
        monster = RaidMonster('tim.json')

        embed_message = self.build_monster_embed(monster)

        message = await self.discord_client.send_message(self.rb_channel, content='Message with embed.',  embed=embed_message)
        monster.message_id = message.id

        self.monsters[monster.message_id] = monster

        await self.discord_client.add_reaction(message, "\N{CROSSED SWORDS}")
        await self.discord_client.add_reaction(message, "\N{LEFTWARDS BLACK ARROW}")
        await self.discord_client.add_reaction(message, "\N{BLACK RIGHTWARDS ARROW}")

    @asyncio.coroutine
    async def route_action(self, reaction, user):
        await self.discord_client.send_message(reaction.message.channel, "{} reacted with {} to message {}".format(user.name, reaction.emoji, reaction.message.id))
        self.monsters[reaction.message.id].current_hp -= 10
        monster_embed = self.build_monster_embed(self.monsters[reaction.message.id])
        await self.discord_client.edit_message(reaction.message, embed=monster_embed, new_content='Im edited!')
