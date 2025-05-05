import paramiko
from agno.tools import tool
from config import HOST, USERNAME, PASSWORD


@tool(
    name="ssh_shell_command",  # Custom name for the tool (otherwise the function name is used)
    description="Run a shell command from received command",  # Custom description (otherwise the function docstring is used)
    show_result=True,  # Show result after function call
    stop_after_tool_call=False,  # Return the result immediately after the tool call and stop the agent
)
def execute_command(command: str) -> str:
    """Run a shell command on a remote server over SSH using IP, username, and password."""
    try:
        print(
            "Try to execute command: ",
            command,
            "with host: ",
            HOST,
            "username: ",
            USERNAME,
            "password: ",
            PASSWORD,
        )
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(HOST, username=USERNAME, password=PASSWORD, timeout=10)

        stdin, stdout, stderr = ssh.exec_command(command)

        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        ssh.close()

        if error:
            return f"Error: {error}"
        return output or "Command executed with no output (blank)"
    except Exception as e:
        return f"SSH Exception: {str(e)}"
