import sys
import json

command_list = [
    "ready",
    "print",
    "caption"
]

def stdout(command: str, content = ""):
    if command not in command_list:
        stderr("Command not found")
        return
    msg = { "command": command }
    if(command == "print"):
        msg["content"] = content
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()

def stdout_caption(caption):
    sys.stdout.write(json.dumps(caption) + "\n")
    sys.stdout.flush()

def stderr(text: str):
    sys.stderr.write(text + "\n")
    sys.stderr.flush()
