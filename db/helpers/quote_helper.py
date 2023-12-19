from db import DB

import sqlalchemy as sa
import datetime as dt

from db.model.quote import Quote


def add_quote(guild_id: int, user_id: int, name: str, quote: str):
    try:
        # Get most recent quote number for guild
        number = DB.s.execute(
            sa.select(Quote.number)
            .where(Quote.guild_id == guild_id)
            .order_by(Quote.number.desc())
            .limit(1)
        ).scalar_one_or_none()
        next_number = 1 if number is None else number + 1
        DB.s.add(Quote(guild_id=guild_id, user_id=user_id, number=next_number, name=name, created_at=dt.datetime.utcnow(), quote=quote))
        DB.s.commit()
        return True
    except sa.exc.IntegrityError:
        DB.s.rollback()
        return False

def list_quotes(guild_id:int):
    return DB.s.execute(
        sa.select(Quote)
        .where(Quote.guild_id == guild_id)
        .order_by(Quote.number.asc())
    ).all()

def list_quotes_by_name(guild_id:int, name:str):
    return DB.s.execute(
        sa.select(Quote)
        .where(Quote.guild_id == guild_id)
        .where(Quote.name == name)
        .order_by(Quote.number.asc())
    ).all()