from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger, String, Text

class Base(DeclarativeBase):
    pass

class ChatHistory(Base):
    __tablename__ = 'chat_history'

    message_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    channel_id: Mapped[int] = mapped_column(BigInteger, index=True)
    guild_id: Mapped[int | None] = mapped_column(BigInteger, index=True, nullable=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    role: Mapped[str] = mapped_column(String(10))
    timestamp: Mapped[int] = mapped_column(BigInteger)
    content: Mapped[str] = mapped_column(Text)