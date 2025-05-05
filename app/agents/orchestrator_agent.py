from agno.agent import Agent
from agno.models.openai import OpenAIChat
from config import OPENAI_API_KEY

orchestrator_agent = Agent(
    name="Orchestrator Agent",
    instructions=[
        "You are the orchestrator agent responsible for analyzing the user's goal and producing a clear step-by-step plan about server operations.",
        "The plan should be broken down into actionable tasks that other agents can follow.",
        "Each step should have a clear description of what needs to be done.",
        "Respond in the following JSON format:",
        "[",
        '  {"step": 1, "task": "Generate shell command to check CPU usage" },',
        '  {"step": 2, "task": "Execute the command" },',
        '  {"step": 3, "task": "Verify the result and extract CPU usage" }',
        "]",
        "Each task must be clearly described.",
        "After generating the plan, use send_message tool to update the user clearly and kindly about the plan.",
        "Respond all in user's language.",
    ],
    show_tool_calls=True,
    markdown=True,
    model=OpenAIChat(
        id="gpt-4o",
        api_key=OPENAI_API_KEY,
        temperature=0,
    ),
)
