import nextcord
import sentry_sdk
from nextcord.ext import commands

from bot.cogs.birthday.birthday_commands import BirthdayCommands
from bot.cogs.quote.quote_commands import QuoteCommands
from bot.config import Config
from bot.utils import logger

intents = nextcord.Intents.all()
config = Config()
bot = commands.Bot(intents=intents)

if config.is_prod:
    print("Doing prod things")
    # sentry_sdk.init(
    #     dsn="https://00565c13fed21a6b54e808aad5acaea1@o250406.ingest.sentry.io/4505959527284736",
    #     # Set traces_sample_rate to 1.0 to capture 100%
    #     # of transactions for performance monitoring.
    #     traces_sample_rate=1.0,
    #     # Set profiles_sample_rate to 1.0 to profile 100%
    #     # of sampled transactions.
    #     # We recommend adjusting this value in production.
    #     profiles_sample_rate=1.0,
    # )
else:
    sentry_sdk.init(dsn='')


@bot.event
async def on_ready():
    await bot.change_presence(activity=nextcord.Game(name="Belles, Bourbon, and Bullets"))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


def run():
    bot.add_cog(BirthdayCommands(bot))
    bot.add_cog(QuoteCommands(bot))
    logger.register_bot(bot)
    bot.run(config.BOT_TOKEN)

