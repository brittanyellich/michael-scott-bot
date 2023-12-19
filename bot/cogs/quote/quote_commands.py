from datetime import datetime, timezone, time
import asyncio

from nextcord import slash_command, Interaction, SlashOption, Permissions, Member, TextChannel
from nextcord.ext import commands, tasks

from bot.utils import messages
from db.helpers import birthday_helper

class QuoteCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    ##############################
    # Admin Slash Commands
    ##############################

    @slash_command(name='quote-admin',
                   description='Quote admin commands', default_member_permissions=Permissions(manage_guild=True))
    async def quote_admin(self, interaction: Interaction):
        pass

    @quote_admin.subcommand(name='remove', description='Remove a quote')
    async def quote_admin_remove(self, interaction: Interaction,
                                number: int = SlashOption(name='number', description='Quote number to delete')):
        # Allow admin to delete any quote
        await interaction.send('Not implemented yet.')

    ##############################
    # Regular Slash Commands
    ##############################

    @slash_command(name='quote',
                   description='Quote commands')
    async def quote(self, interaction: Interaction):
        pass

    @quote.subcommand(name='add', description='Add a quote')
    async def quote_add(self, interaction: Interaction,
                            name: str = SlashOption(name='name', description='Name of person who said quote'),
                            quote: str = SlashOption(name='quote', description='Quote')):
        await interaction.send('Not implemented yet.')
    
    @quote.subcommand(name='random', description='Get a random quote')
    async def quote_random(self, interaction: Interaction,
                            name: Member = SlashOption(name='name',
                                                         description='Optional name to get a random quote for', required=False),):
        await interaction.send('Not implemented yet.')
        
    @quote.subcommand(name='list', description='List quotes')
    async def quote_list(self, interaction: Interaction,
                            name: Member = SlashOption(name='name',
                                                         description='Optional name to list quotes for', required=False),):
        await interaction.send('Not implemented yet.')

    @quote.subcommand(name='remove', description='Remove a birthday')
    async def quote_remove(self, interaction: Interaction,
                                number: str = SlashOption(name='number', description='Number of quote to delete')):
        # Allow user to delete quote if they created it
        await interaction.send('Not implemented yet.')
