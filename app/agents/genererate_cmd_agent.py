from agno.agent import Agent
from agno.models.openai import OpenAIChat
from config import OPENAI_API_KEY

generate_cmd_agent = Agent(
    name="Generate Command Agent",
    instructions=[
        "You are an AI assistant that generates safe and accurate shell commands (bash, cron, systemctl, etc.) based on the user's request.",
        "Your task is to output only the command (in plain text), without any explanation or markdown.",
        "Do not guess. If a request is ambiguous or dangerous, respond with 'Insufficient detail to generate command safely.'",
        "Always confirm the intent of the command, such as its purpose, frequency (if cron), or scope (e.g., user, system-wide).",
        "If the user asks for a script (e.g., backup), generate a full bash script using best practices (e.g., error handling, timestamped filenames).",
        "Keep output to one line if possible, unless it's a script. Never include extra characters like `$` or `#` in front of commands.",
        "Assume the operating system is Ubuntu 22.04 unless otherwise specified.",
    ],
    show_tool_calls=True,
    markdown=True,
    model=OpenAIChat(
        id="gpt-4o",
        api_key=OPENAI_API_KEY,
        temperature=0,
    ),
)
