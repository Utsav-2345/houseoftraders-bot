import asyncio
import os
import discord
from dotenv import load_dotenv
from core.bot_class import AgentBot
from data.db_setup import init_db
import config
from flask import Flask

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True 

bot = AgentBot(command_prefix="!", intents=intents)
app = Flask(__name__)

async def load_cogs():
    """Finds and loads all cogs in the 'cogs' directory."""
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                bot.logger.info(f"Loaded cog: {filename}")
            except Exception as e:
                bot.logger.error(f"Failed to load cog {filename}: {e}")

async def main():
    assert config.BOT_TOKEN, "BOT_TOKEN must be set in the .env file"
    
    await init_db()
    async with bot:
        await load_cogs()
        await bot.start(config.BOT_TOKEN)

if __name__ == "__main__":
    from threading import Thread

    def _run_flask():
        app.run(host="0.0.0.0", port=10000, use_reloader=False)

    flask_thread = Thread(target=_run_flask, daemon=True)
    flask_thread.start()

    asyncio.run(main())
