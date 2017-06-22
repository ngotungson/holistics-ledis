import sys
import socket
from thread import *
import traceback
import time
import schedule

from storage import *
import cli
from jobs import auto_expiration, auto_snapshot


class LedisServer(object):
    def __init__(self):
        self.socket = socket.socket()
        self.n_requests = None

    def define_socket(self, port, n_requests=5):
        host = "localhost"
        print "Ledis server is running on... " + str(host) + ":" + str(port)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))
        self.n_requests = n_requests

    def run(self):
        self.run_cron_jobs()

        self.socket.listen(self.n_requests)
        self.handle_commands()
        self.socket.close()

    def handle_commands(self):
        while True:
            connect, address = self.socket.accept()
            prompt = str(address[0]) + ":" + str(address[1]) + "> "
            connect.sendall(prompt)
            start_new_thread(self._command_handler ,(connect, address))

    def _command_handler(self, connect, address):
        while True:
            try:
                command = connect.recv(1024)
                if not command:
                    break
                result = str(cli.run(command)) + "\n"
                connect.sendall(result)
            except Exception as e:
                error = "Error: " + e.message + "\n"
                connect.sendall(error)
                # print(traceback.format_exc())
            finally:
                prompt = str(address[0]) + ":" + str(address[1]) + "> "
                connect.sendall(prompt)
                # print storage
        connect.close()


    def run_cron_jobs(self):
        start_new_thread(self._cron_jobs, ())

    def _cron_jobs(self):
        schedule.every(1).seconds.do(auto_expiration)
        schedule.every(1).days.do(auto_snapshot)
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    server = LedisServer()
    server.define_socket(8888, 5)
    server.run()
