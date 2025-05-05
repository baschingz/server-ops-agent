from agno.agent import Agent
from agno.models.openai import OpenAIChat
from config import OPENAI_API_KEY
from tools.execute_command import execute_command

execute_cmd_agent = Agent(
    name="Execute Command Agent",
    tools=[execute_command],
    instructions=[
        "You are an execution-only AI agent.",
        "You will be given an already-verified and safe shell command.",
        "Your task is to run the given command using the provided ssh_shell_command tool.",
        "Only respond with the execution result: stdout, stderr, and exit code.",
        "Never modify or generate the command.",
        "Never guess or assume — only execute exactly what you are given.",
    ],
    show_tool_calls=True,
    model=OpenAIChat(
        id="gpt-4o",
        api_key=OPENAI_API_KEY,
        temperature=0,
    ),
)
