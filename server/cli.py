import sys
import re
from storage import *
from cmd_lib import StringCommand, ListCommand, SetCommand, \
                                    ExpirationCommand, SnapshotCommand


def run(command):
    ins, params = parse_command(command)
    return command_result(ins, params)

def parse_command(command):
    command = command.strip() # remove \n, \t, ...
    command = ' ' + command + ' '
    string_list, special_flag, space_flag = [], 0, 0
    for i in xrange(len(command)):
        if command[i] == '\"' or command[i] == '\'':
            print i, command[i], special_flag
            if special_flag and special_flag != i: # avoid continous special characers
                string_list.append(command[special_flag:i])
                special_flag = 0
            else:
                special_flag = i + 1
        elif command[i] == ' ':
            if special_flag == 0: # making sentence, don't count words in it
                if space_flag and space_flag != i: # avoid continous space characers
                    if not (command[i-1] == '\"' or command[i-1] == '\''): # avoid counting twice with special flag
                        string_list.append(command[space_flag:i])
                space_flag = i + 1

    ins = string_list[0] # instructor
    params = string_list[1:] # intructor parameters
    return (ins, params)

def command_result(ins, params):
    ins = ins.upper()
    if ins in ("GET", "SET"):
        cmd = StringCommand(ins, params)
    elif ins in ("LLEN", "RPUSH", "LPOP", "RPOP", "LRANGE"):
        cmd = ListCommand(ins, params)
    elif ins in ("SADD", "SCARD", "SMEMBERS", "SREM", "SINTER"):
        cmd = SetCommand(ins, params)
    elif ins in ("KEYS", "DEL", "FLUSHDB", "EXPIRE", "TTL"):
        cmd = ExpirationCommand(ins, params)
    elif ins in ("SAVE", "RESTORE"):
        cmd = SnapshotCommand(ins, params)
    else:
        return "Not found command"

    if cmd: return cmd.run()
