from datetime import datetime, timezone, time
import asyncio

from nextcord import slash_command, Interaction, SlashOption, Permissions, Member, TextChannel
from nextcord.ext import commands, tasks

from bot.config import Config
from bot.utils import messages
from db.helpers import birthday_helper

class BirthdayCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.post_birthdays.start()
    
    # Every day at 5AM Pacific Time post birthday messages
    # @tasks.loop(time=time(hour=12, minute=0, second=0, tzinfo=timezone.utc))
    @tasks.loop(seconds=10)
    async def post_birthdays(self):
        if not self.bot.is_ready():
            return

        birthdays_by_guild_id = birthday_helper.get_todays_birthdays()
        for guild_id, birthdays in birthdays_by_guild_id.items():
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                # Can't find guild, skip posting these birthdays
                continue
            birthday_channel_id = birthday_helper.get_birthday_channel_id(guild_id)
            if birthday_channel_id is None:
                # No birthday channel set, skip posting these birthdays
                continue
            channel = self.bot.get_channel(birthday_channel_id)
            if channel is None:
                # Can't find channel, skip posting these birthdays
                continue
            # Assemble birthday message
            message = messages.birthday_message()
            for birthday in birthdays:
                member = guild.get_member(birthday.user_id)
                message = messages.birthday_entry(message, birthday, member)
            message = messages.get_special_birthday_fields(message)
            await channel.send(embed=message)
        baby_month_milestones = birthday_helper.get_todays_baby_month_milestones()
        for guild_id, birthdays in baby_month_milestones.items():
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                # Can't find guild, skip posting these birthdays
                continue
            baby_month_milestone_channel_id = birthday_helper.get_baby_month_milestone_channel_id(guild_id)
            if baby_month_milestone_channel_id is None:
                # No baby month milestone channel set, skip posting these birthdays
                continue
            channel = self.bot.get_channel(baby_month_milestone_channel_id)
            if channel is None:
                # Can't find channel, skip posting these birthdays
                continue
            # Assemble baby month milestone message
            for birthday in birthdays:
                message = messages.baby_month_milestone_message(birthday, member)
                await channel.send(embed=message)

    @post_birthdays.error
    async def post_birthdays_error(self, e):
        print(e)
        # sentry_sdk.capture_exception(e)
        await asyncio.sleep(60)
        self.post_birthdays.restart()

    ##############################
    # Admin Slash Commands
    ##############################

    @slash_command(name='birthday-admin',
                   description='Birthday commands', default_member_permissions=Permissions(manage_guild=True))
    async def birthday_admin(self, interaction: Interaction):
        pass

    @birthday_admin.subcommand(name='settings', description='Configure birthday settings')
    async def birthday_config(self, interaction: Interaction,
                                birthday_channel: TextChannel = SlashOption(name='birthday_channel',
                                                                description='Channel to post birthday messages in.', required=False),
                                baby_month_milestone_channel: TextChannel = SlashOption(name='baby_month_milestone_channel', 
                                                                description='Channel to post baby month milestone messages in.', required=False)):
        if birthday_channel is not None:
            success = birthday_helper.update_birthday_channel_settings(interaction.guild_id, birthday_channel.id)
            if not success:
                return await interaction.send(f'An error occurred when updating birthday channel settings.')
            
        if baby_month_milestone_channel is not None:
            success = birthday_helper.update_baby_month_channel_settings(interaction.guild_id, baby_month_milestone_channel.id)
            if not success:
                return await interaction.send(f'An error occurred when updating baby milestone channel settings.')
        await interaction.send('Successfully updated birthday settings!')

    ##############################
    # Regular Slash Commands
    ##############################

    @slash_command(name='birthday',
                   description='Birthday commands')
    async def birthday(self, interaction: Interaction):
        pass

    @birthday.subcommand(name='add', description='Add a birthday')
    async def birthday_add(self, interaction: Interaction,
                            name: str = SlashOption(name='name', description='Name of person celebrating a birthday'),
                            date: str = SlashOption(name='date', description='Date of birthday (MM/DD/YYYY)')):
        # Get date from added date, validate, and add to the database. Return an error if the name already exists or the date is invalid.
        try:
            dt = datetime.strptime(date, '%m/%d/%Y')
            success = birthday_helper.add_birthday(interaction.guild_id, interaction.user.id, name.lower(), dt.month, dt.day, dt.year)
            if success:
                await interaction.send('Birthday added.')
            else:
                await interaction.send(f'Birthday already exists for {name.title()}. Try a different name, or remove the existing birthday first.')
        except ValueError:
            return await interaction.send('Please provide a date in the format MM/DD/YYYY')
        
    @birthday.subcommand(name='list', description='List birthdays')
    async def birthday_list(self, interaction: Interaction,
                            user: Member = SlashOption(name='user',
                                                         description='User to list birthdays for.'),):
        birthdays = birthday_helper.list_birthdays(interaction.guild_id, user.id)
        if len(birthdays) == 0:
            embed = messages.info(f'No stored birthdays found for {user.name}. Use `/birthday add` to add a birthday.')
            icon_url = user.avatar.url if user.avatar else None
            embed.set_author(name=user.name, icon_url=icon_url)
            return await interaction.send(embed=embed)
        embed = messages.info(f'Current birthdays stored for {user.name}. Use `/birthday remove` to remove a stored birthday.')
        icon_url = user.avatar.url if user.avatar else None
        embed.set_author(name=user.name, icon_url=icon_url)
        for birthday in birthdays:
            embed.add_field(name=birthday[0].name.title(), value=f'{birthday[0].month}/{birthday[0].day}/{birthday[0].year}')
        await interaction.send(embed=embed)

    @birthday.subcommand(name='remove', description='Remove a birthday')
    async def birthday_remove(self, interaction: Interaction,
                                name: str = SlashOption(name='name', description='Name of birthday to remove')):
        success = birthday_helper.delete_birthday(interaction.guild_id, interaction.user.id, name.lower())
        if not success:
            return await interaction.send(f'An error occurred when deleting birthday {name.title()} associated with user {user.name}.')
        await interaction.send('Successfully deleted birthday!')
