from discord.ext import commands
from agent.agent_factory import create_agent
from core.logger import setup_logging
import discord
import platform
import os

class AgentBot(commands.Bot):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.logger = setup_logging()
        self.agent = create_agent()
        
    async def on_ready(self):
        if self.user is not None:
            self.logger.info(f"Logged in as {self.user.name}")

        self.logger.info(f"discord.py API version: {discord.__version__}")
        self.logger.info(f"Python version: {platform.python_version()}")
        self.logger.info(
            f"Running on: {platform.system()} {platform.release()} ({os.name})"
        )
        self.logger.info("-------------------")
