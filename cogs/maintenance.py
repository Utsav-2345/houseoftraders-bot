from discord.ext import commands,tasks
from core.bot_class import AgentBot
import datetime
from data import crud

class MaintenanceCog(commands.Cog):
    def __init__(self, bot: AgentBot):
        self.bot = bot
        self.logger = bot.logger
    
    async def cog_unload(self):
        self.purge_old_messages.cancel()

    @tasks.loop(hours=6)
    async def purge_old_messages(self):
        try:
            cutoff_dt = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=20)
            cutoff_timestamp = int(cutoff_dt.timestamp())
            self.logger.info("Running scheduled task: Purging messages older than %s", cutoff_dt.isoformat())
            deleted_count = await crud.delete_messages_before(cutoff_timestamp)
            self.logger.info(f"Deleted {deleted_count} messages.")
            pass
        except Exception as e:
            self.logger.error("An error occurred in the purge_old_messages task.", exc_info=e)

    @purge_old_messages.before_loop
    async def before_purge_old_messages(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(MaintenanceCog(bot))