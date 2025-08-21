import discord
from discord.ext import commands
from agent.agent_factory import create_agent
from agent.context import DiscordContext
from core.bot_class import AgentBot
from data import crud
from langchain_core.messages import HumanMessage
from agent.agent_factory import AgentState

class AgentListenerCog(commands.Cog):
    def __init__(self, bot: AgentBot):
        self.bot = bot
        self.agent = create_agent()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        
        if not self.bot.is_ready() or self.bot.user is None:
            return

        is_reply_to_bot = (
            message.reference and
            message.reference.resolved and
            isinstance(message.reference.resolved, discord.Message) and
            message.reference.resolved.author == self.bot.user
        )

        if self.bot.user not in message.mentions and not is_reply_to_bot:
            return
        
        user_content = message.content.replace(f'<@{self.bot.user.id}>', '').strip()
        await crud.add_message_to_history(
            message_id=message.id,
            channel_id=message.channel.id,
            guild_id=message.guild.id if message.guild else None,
            user_id=message.author.id,
            role="user",
            content=user_content
        )


        async with message.channel.typing():
            thinking_message = await message.channel.send("<a:thinking:1407841048755175546> Thinking...")

            try:
                with DiscordContext(self.bot, message, thinking_message):
                    initial_state: AgentState = {
                        "messages": [HumanMessage(content=user_content)]
                    }

                    result = await self.agent.ainvoke(initial_state)
                    final_message = result["messages"][-1]
                    
                    ai_response = ""
                    for _ in range(2):
                        ai_response = final_message.content if hasattr(final_message, "content") else str(final_message)
                        if ai_response.strip():
                            break
                        else:
                            continue
                

                    if len(ai_response) > 2000:
                        ai_response = ai_response[:1900] + "\n\n*[Response truncated due to length limit]*"

                    await thinking_message.edit(content=ai_response)
                    await crud.add_message_to_history(
                        message_id=thinking_message.id,
                        guild_id=message.guild.id if message.guild else None,
                        channel_id=message.channel.id,
                        user_id=self.bot.user.id,
                        role="ai",
                        content=ai_response
                    )
            except Exception as e:
                error_message = f"❌ Error: {str(e)}"
                await thinking_message.edit(content=error_message)        

async def setup(bot: AgentBot):
    await bot.add_cog(AgentListenerCog(bot))