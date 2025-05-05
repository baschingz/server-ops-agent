from fastapi import FastAPI, Request
import uvicorn
from agents.orchestrator_agent import orchestrator_agent
from agno.team import Team
from agno.models.openai import OpenAIChat
from config import OPENAI_API_KEY
from agents.genererate_cmd_agent import generate_cmd_agent
from agents.execute_cmd_agent import execute_cmd_agent
from tools.send_message import team_send_message
from agents.progress_agent import progress_update_agent

app = FastAPI()


# ====== LINE WEBHOOK ENDPOINT ======
@app.post("/")
async def line_webhook(request: Request):
    body = await request.json()
    print("🔔 LINE Webhook received")

    try:
        events = body.get("events", [])
        if not events:
            return {"status": "no events"}

        msg = events[0].get("message", {}).get("text", "")
        uid = events[0].get("source", {}).get("userId", "")
        if not msg:
            return {"status": "no message"}

        print("User input: ", msg)

        task = await orchestrator_agent.arun(msg)
        team_multi_agent = Team(
            model=OpenAIChat(
                id="gpt-4o",
                api_key=OPENAI_API_KEY,
                temperature=0,
            ),
            name="team_multi_agent",
            tools=[team_send_message],
            members=[
                generate_cmd_agent,
                execute_cmd_agent,
                progress_update_agent,
            ],
            mode="coordinate",
            instructions=[
                "You are a multi-agent assistant team responsible for automating server operations and managing infrastructure tasks.",
                "The user will describe a goal, such as monitoring CPU, deploying an app, or modifying system config.",
                "Your job is to coordinate the steps required to complete the task using available agents and tools.",
                "All responses to the user should be short, friendly, human-like, and in the user's own language.",
                "Do not use overly technical terms unless the user explicitly requests it.",
                "When a step fails, retry with adjustments or ask the user politely for clarification.",
                "Only finish the task when the system confirms the outcome has been achieved or clearly failed.",
                "Reponse nice pattern for chat conversation with pretty space and emoji and no markdown.",
                "Don't forget to use progress_update_agent to update the user about the progress of a task. (only important progress update)",
                "Final response use team_send_message tool to send result to the user clearly and kindly about the result.",
            ],
            session_state={"uid": uid},
            success_criteria="All steps have been completed and the user has been informed of the outcome in simple, friendly language.",
            markdown=True,
            show_tool_calls=True,
        )
        team_multi_agent.print_response(task.content, stream=True, final_response=True)
        return {"status": "ok"}

    except Exception as e:
        print("Error: ", str(e))
        return {"error": str(e)}


# ====== LOCAL TEST ======
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
