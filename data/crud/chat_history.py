from ..db_setup import AsyncSessionLocal
from ..models import ChatHistory
from sqlalchemy import delete, select
import time

async def delete_messages_before(timestamp:int) -> int:
    async with AsyncSessionLocal() as session:
        query = delete(ChatHistory).where(ChatHistory.timestamp < timestamp)
        result = await session.execute(query)
        await session.commit()
        return result.rowcount
    
async def add_message_to_history(
        message_id: int,
        channel_id: int,
        guild_id: int | None,
        user_id: int,
        role: str,
        content: str
):
    async with AsyncSessionLocal() as session:
        new_message = ChatHistory(
            message_id=message_id,
            channel_id=channel_id,
            guild_id=guild_id,
            user_id=user_id,
            timestamp=int(time.time()),
            role=role,
            content=content[:2000]
        )
        session.add(new_message)
        await session.commit()

async def get_messages_by_channel_and_user(channel_id: int, user_id: int, limit: int = 20) -> list[ChatHistory]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(ChatHistory).where(ChatHistory.channel_id == channel_id, ChatHistory.user_id == user_id).order_by(ChatHistory.timestamp.desc()).limit(limit)
        )
        return list(result.scalars().all())

async def get_recent_conversation(channel_id: int, limit: int = 10) -> list[ChatHistory]:
    """Get recent conversation from all users in a channel"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(ChatHistory).where(ChatHistory.channel_id == channel_id).order_by(ChatHistory.timestamp.desc()).limit(limit)
        )
        messages = list(result.scalars().all())
        return list(reversed(messages))  # Return in chronological order