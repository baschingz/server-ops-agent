from agno.agent import Agent
from agno.team import Team
from agno.tools import tool
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
from linebot.models import TextSendMessage
from config import LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET
from agno.utils.log import log_error
import time
from linebot.webhook import WebhookParser


class SendMessage:
    def __init__(self):
        self.line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
        self.parser = WebhookParser(LINE_CHANNEL_SECRET)

    def call(
        self, message: str, uid: str, retries: int = 3, retry_delay: float = 1.0
    ) -> bool:
        for attempt in range(retries):
            try:
                self.line_bot_api.push_message(uid, TextSendMessage(text=message))
                return True
            except LineBotApiError as e:
                log_error(
                    f"[Attempt {attempt + 1}] Error sending message to {uid}: {e}"
                )
                time.sleep(retry_delay)
        return False


@tool(
    name="send_message",
    description="Send a message to a user to update progress, result, or error with safe mode fallback.",
    show_result=True,
    stop_after_tool_call=False,
)
def send_message(agent: Agent, message: str) -> str:
    uid = agent.team_session_state.get("uid")
    if not uid:
        log_error("UID not found in session state.")
        return "Failed to send message: UID not found."

    print("Try to send message: ", message, "to uid: ", uid)

    success = SendMessage().call(message, uid)
    if success:
        return "Message sent successfully"
    else:
        # ✅ Safe mode fallback
        log_error(f"SafeMode: Could not send message to {uid}. Message was: {message}")
        return "Failed to send message after multiple attempts (SafeMode engaged)."


@tool(
    name="team_send_message",
    description="Send a message to a user to update progress, result, or error with safe mode fallback.",
    show_result=True,
    stop_after_tool_call=False,
)
def team_send_message(team: Team, message: str) -> str:
    uid = team.session_state.get("uid")
    if not uid:
        log_error("UID not found in session state.")
        return "Failed to send message: UID not found."

    print("Try to send message: ", message, "to uid: ", uid)

    success = SendMessage().call(message, uid)
    if success:
        return "Message sent successfully"
    else:
        # ✅ Safe mode fallback
        log_error(f"SafeMode: Could not send message to {uid}. Message was: {message}")
        return "Failed to send message after multiple attempts (SafeMode engaged)."
