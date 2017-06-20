import sys
import socket
from thread import *

from storage import *
import cmd_handler

class LedisServer(object):
    def __init__(self):
        self.socket = socket.socket()
        self.n_requests = None

    def define_socket(self, port, n_requests=5):
        host = "localhost"
        print "Host name is: %s" % str(host)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # for reusable address
        self.socket.bind((host, port))
        self.n_requests = n_requests

    def handle_command_thread(self, connect):
        while True:
            try:
                command = connect.recv(1024)
                if not command:
                    connect.sendall("No command")
                    break
                result = "OK\n"
                result += str(cmd_handler.run(command)) + "\n"
                connect.sendall(result)
            except Exception as e:
                print e
                connect.sendall("Error: " + e.message + "\n")
            finally:
                print storage
        connect.close()

    def handle_commands(self):
        self.socket.listen(self.n_requests)
        while True: # blocking call pattern like Apache
            # TO-DO: Move to non-block call like Nginx
            connect, address = self.socket.accept()
            print 'Connected with ' + address[0] + ':' + str(address[1])
            start_new_thread(self.handle_command_thread ,(connect, ))
        self.socket.close()

if __name__ == "__main__":
    server = LedisServer()
    server.define_socket(915, 5)
    server.handle_commands()
