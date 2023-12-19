from sqlalchemy.orm import Mapped, mapped_column

from db import DB
import datetime as dt


class Quote(DB.Model):
    __tablename__ = 'quotes'

    guild_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    quote: Mapped[str] = mapped_column()
    created_at: Mapped[dt.datetime] = mapped_column()
