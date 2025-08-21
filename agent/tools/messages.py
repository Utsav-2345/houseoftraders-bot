from langchain_core.tools import tool
import discord
from agent.context import get_bot
from pydantic import BaseModel, Field
from typing import Optional, List
import datetime

class EmbedField(BaseModel):
    name: str = Field(..., description="The name of the field")
    value: str = Field(..., description="The value of the field")
    inline: bool = Field(False, description="Whether the field should be displayed inline")

class DiscordEmbed(BaseModel):
    title: str = Field(..., description="The title of the embed")
    author: Optional[str] = Field(None, description="The author of the embed")
    author_icon: Optional[str] = Field(None, description="The author's icon URL")
    thumbnail: Optional[str] = Field(None, description="The thumbnail image URL of the embed")
    image: Optional[str] = Field(None, description="The image URL of the embed")
    footer: Optional[str] = Field(None, description="The footer text of the embed")
    footer_icon: Optional[str] = Field(None, description="The footer icon URL of the embed")
    timestamp: Optional[datetime.datetime] = Field(None, description="The timestamp of the embed")
    description: str = Field(..., description="The description of the embed")
    url: Optional[str] = Field(None, description="The URL of the embed")
    color: Optional[int] = Field(0x5865F2, description="The color of the embed (default Discord blurple)")
    fields: Optional[List[EmbedField]] = Field(None, description="A list of fields for the embed")

@tool
async def send_message(
    channelId: str,
    content: Optional[str] = None,
    embed: Optional[DiscordEmbed] = None,
    embeds: Optional[List[DiscordEmbed]] = None
) -> str:
    """
    Send a message or embed in a channel.
    
    Args:
        channelId: The ID of the channel to send the message to
        content: The text content of the message (optional)
        embed: A Discord embed to send (optional)
        embeds: List of Discord embeds to send (optional)
    
    Returns:
        str: Confirmation message with the sent message ID
    """
    bot = get_bot()
    if not bot or not bot.is_ready():
        raise ConnectionError("Bot is not initialized, connected, or ready.")

    channel = bot.get_channel(int(channelId))
    if not channel or not isinstance(channel, discord.abc.Messageable):
        raise ValueError(f"Channel with ID {channelId} not found or is not messageable.")

    final_embeds = []
    embeds = embeds or ([embed] if embed else [])
    if embeds:
        for embed_data in embeds:
            new_embed = discord.Embed(
                title=embed_data.title,
                description=embed_data.description,
                url=embed_data.url,
                timestamp=embed_data.timestamp,
                color=embed_data.color
            )

            if embed_data.author:
                new_embed.set_author(
                    name=embed_data.author,
                    icon_url=embed_data.author_icon
                )

            if embed_data.thumbnail:
                new_embed.set_thumbnail(url=embed_data.thumbnail)

            if embed_data.image:
                new_embed.set_image(url=embed_data.image)
            
            if embed_data.footer:
                new_embed.set_footer(
                    text=embed_data.footer,
                    icon_url=embed_data.footer_icon
                )
            
            if embed_data.fields:
                for field in embed_data.fields:
                    new_embed.add_field(
                        name=field.name,
                        value=field.value,
                        inline=field.inline
                    )

            final_embeds.append(new_embed)
            
    try:
        sent_message = await channel.send(
            content=content,
            embeds=final_embeds
        )
        return f"Message sent successfully with ID: {sent_message.id}"
    except Exception as e:
        print(e)
        raise RuntimeError(f"Failed to send message: {e}")