import sys
import socket
from thread import *
import traceback
import time
import schedule

from storage import *
import cmd_handler
from jobs.auto_expiration import *

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

    def handle_commands(self):

        def command_thread(connect):
            while True:
                try:
                    command = connect.recv(1024)
                    if not command:
                        connect.sendall("No command")
                        break
                    result = str(cmd_handler.run(command)) + "\n"
                    connect.sendall(result)
                except Exception as e:
                    print(traceback.format_exc())
                    connect.sendall("Error: " + e.message + "\n")
                finally:
                    print storage
            connect.close()

        self.socket.listen(self.n_requests)
        while True:
            connect, address = self.socket.accept()
            print 'Connected with ' + address[0] + ':' + str(address[1])
            start_new_thread(command_thread ,(connect, ))

            self.run_cron_jobs()
        self.socket.close()


    def run_cron_jobs(self):
        schedule.every(1).seconds.do(auto_expiration)
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    server = LedisServer()
    server.define_socket(915, 5)
    server.handle_commands()
