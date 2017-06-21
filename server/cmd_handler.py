import sys
from storage import *
from cmd_lib import StringCommand, ListCommand

def run(command):
    ins, params = parse_command(command)
    return command_result(ins, params)

def parse_command(command):
    command = command.strip().split(" ")
    ins = command[0] # instructor
    params = command[1:] # intructor parameters
    return (ins, params)

def command_result(ins, params):
    ins = ins.upper()
    cmd = ""
    if ins in ("GET", "SET"):
        cmd = StringCommand(ins, params)
    elif ins in ("LLEN", "RPUSH", "LPOP", "RPOP", "LRANGE"):
        cmd = ListCommand(ins, params)
    else:
        return "Not found command"
            
    if cmd: return cmd.run()
