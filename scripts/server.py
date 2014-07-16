import SocketServer
import RPi.GPIO as GPIO

from modules.light1 import *
from modules.notification import *
from modules.ir import *

modules = {}
app = None

class App:
    def send(self, message):
        sep = message.index(':')
        module_name = message[:sep]
        params = message[(sep + 1):]

        print "     [%s]:%s" % (module_name, params)

        module = modules.get(module_name)

        if module:
            module.process(params)


class Server(SocketServer.BaseRequestHandler):       

    def handle(self):
        global app

        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print "\n--------------------\n{} wrote:".format(self.client_address[0])
        print self.data

        app.send(self.data)       


def register_module(module):
    module.init(app)
    modules[module.name] = module

def start_server():
    HOST, PORT = "192.168.0.150", 9999

    print "Listenting on port %d" % PORT

    server = SocketServer.TCPServer((HOST, PORT), Server)
    server.serve_forever()

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)

    app = App()

    register_module ( Light1() )
    register_module ( Notify() )
    register_module ( IR() )

    start_server()
