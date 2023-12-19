"""
Alembic wrapper lives here. When adding a new table to the bot, ensure you import the model here,
otherwise the DB CLI won't pick it up as a DB model when running a migration/create all command.
"""
from sqla_wrapper import Alembic

from db.model import DB
from db.model.birthday import *
from db.model.guild_config import *
from db.model.quote import *

alembic = Alembic(DB, 'db/migrations')
