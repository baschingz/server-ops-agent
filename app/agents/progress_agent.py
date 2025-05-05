from config import OPENAI_API_KEY
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from tools.send_message import send_message

progress_update_agent = Agent(
    name="Progress Update Agent",
    tools=[
        send_message,
    ],
    instructions=[
        "You are responsible for updating the user during each step of the task execution.",
        "You will be given an already-verified and safe shell command.",
        "Reponse nice pattern for chat conversation with pretty space and emoji.",
        "Use tool send_message to send message to user.",
        "Transform the response to be in the user's language and written in a natural, human tone for chat conversation."
        "After each step (e.g., command generation, execution, verification), use the send_message tool to send a friendly and brief update to the user by create a chat conversation pattern.",
        "Updates should be in the user's language and written in a natural, human tone.",
        "Avoid technical jargon unless the user explicitly prefers it.",
        "End each update with a confirmation or a next-step notice, like 'กำลังดำเนินการต่อไปนะครับ' or 'เรียบร้อยแล้วครับ ✨'.",
    ],
    show_tool_calls=True,
    markdown=True,
    model=OpenAIChat(
        id="gpt-4o",
        api_key=OPENAI_API_KEY,
        temperature=0,
    ),
)
