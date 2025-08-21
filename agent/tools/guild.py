from langchain_core.tools import tool
from ..context import get_message
from pydantic import BaseModel, Field
class GuildInfo(BaseModel):
    id: str = Field(..., description="The ID of the guild")
    name: str = Field(..., description="The name of the guild")
    owner_id: str = Field(..., description="The ID of the guild owner")
    owner_name: str = Field(..., description="The name of the guild owner")
    member_count: int = Field(..., description="The number of members in the guild")
    iconImage: str = Field(..., description="The icon URL of the guild")
    channels: list[str] = Field(..., description="The list of channels in the guild in format <channel_id>: <channel_name>")

@tool
async def get_guild_info() -> GuildInfo | None:
    """
    Get information about the current guild.
    """

    message = get_message()
    if not message or not message.guild:
        return None
    guild = message.guild
    print(str(guild.icon) if guild.icon else "")
    print(GuildInfo(
        id=str(guild.id),
        name=guild.name,
        owner_id=str(guild.owner.id if guild.owner else ""),
        owner_name=str(guild.owner.name if guild.owner else ""),
        member_count=guild.member_count or 0,
        iconImage=str(guild.icon) if guild.icon else "",
        channels=[f"{channel.id}: {channel.name}" for channel in guild.channels]
    ))
    return GuildInfo(
        id=str(guild.id),
        name=guild.name,
        owner_id=str(guild.owner.id if guild.owner else ""),
        owner_name=str(guild.owner.name if guild.owner else ""),
        member_count=guild.member_count or 0,
        iconImage=str(guild.icon) if guild.icon else "",
        channels=[f"{channel.id}: {channel.name}" for channel in guild.channels]
    )
