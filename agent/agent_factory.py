import re
from typing import Annotated, Sequence, TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph.message import add_messages
import config
from agent.context import get_message
from langchain_core.messages import BaseMessage, SystemMessage, AIMessage, HumanMessage
from langgraph.graph import StateGraph
from data.crud.chat_history import get_recent_conversation
from pydantic import SecretStr
import discord

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

def create_agent():
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-lite",
        api_key=SecretStr(config.GOOGLE_API_KEY) if config.GOOGLE_API_KEY else None,
        temperature=0.7,
        max_output_tokens=1024
    )

    system_prompt = "You are a helpful and concise professional AI assistant with human feelings for a Discord server. Keep answers clear, **detailed, context-aware, under 2000 characters, and conversational visually appealing discord messages (avoid excessive emojis)."

    async def call_model(state: AgentState) -> dict:
        messages = state["messages"]
        user_message = get_message()

        messages_to_send: list[BaseMessage] = [SystemMessage(content=system_prompt)]

        if user_message and isinstance(user_message, discord.Message):
            try:
                recent_conversation = await get_recent_conversation(
                    channel_id=user_message.channel.id,
                    limit=3
                )
                for msg in recent_conversation[:-1]:
                    if msg.role == "user":
                        messages_to_send.append(HumanMessage(content=msg.content))
                    elif msg.role == "ai":
                        messages_to_send.append(AIMessage(content=msg.content))
            except Exception as e:
                print(f"Error getting context: {e}")

        messages_to_send.extend(list(messages))

        response = await llm.ainvoke(messages_to_send)

        if hasattr(response, 'content') and response.content:
            if isinstance(response.content, str) and len(response.content) > 1900:
                response.content = response.content[:1900] + "\n\n*[Response truncated]*"

        return {"messages": [response]}

    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model)
    workflow.set_entry_point("agent")

    return workflow.compile(checkpointer=None, debug=False)
