import sys
import json

command_list = [
    "ready",
    "print"
]

def stdout(command: str, content = ""):
    if command not in command_list:
        stderr("Command not found")
        return
    msg = {
        "command": command,
        "content": content
    }
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()

def stderr(text: str):
    sys.stderr.write(text + "\n")
    sys.stderr.flush()
