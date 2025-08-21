import discord
from typing import Optional
from contextvars import ContextVar

_bot_context: ContextVar[Optional[discord.Client]] = ContextVar('bot_context', default=None)
_message_context: ContextVar[Optional[discord.Message]] = ContextVar('message_context', default=None)
_status_message_context: ContextVar[Optional[discord.Message]] = ContextVar('status_message_context', default=None)

class DiscordContext:    
    def __init__(self, bot: discord.Client, message: discord.Message, status_message: Optional[discord.Message] = None):
        self.bot = bot
        self.message = message
        self.status_message = status_message
        self._bot_token = None
        self._message_token = None
        self._status_token = None
    
    def __enter__(self):
        self._bot_token = _bot_context.set(self.bot)
        self._message_token = _message_context.set(self.message)
        if self.status_message:
            self._status_token = _status_message_context.set(self.status_message)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._bot_token:
            _bot_context.reset(self._bot_token)
        if self._message_token:
            _message_context.reset(self._message_token)
        if self._status_token:
            _status_message_context.reset(self._status_token)

def get_bot() -> Optional[discord.Client]:
    return _bot_context.get()

def get_message() -> Optional[discord.Message]:
    return _message_context.get()

def get_status_message() -> Optional[discord.Message]:
    return _status_message_context.get()