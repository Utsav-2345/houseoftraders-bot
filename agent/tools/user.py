from agent.context import get_message
from langchain_core.tools import tool

@tool
async def get_user_info():
    """
    Get information about the current user.
    """
    current_message = get_message()
    if not current_message:
        raise ValueError("No current message found in context.")
    user = current_message.author
    return {
        "id": user.id,
        "name": user.name,
        "discriminator": user.discriminator,
        "bot": user.bot,
        "avatar": user.avatar.url if user.avatar else None
    }