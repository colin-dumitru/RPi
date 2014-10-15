import BaseHTTPServer
import RPi.GPIO as GPIO
import urllib

from modules.light1 import *
# from modules.notification import *
from modules.ir import *
from modules.mail import *
from modules.notification2 import *

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
            return module.process(params)


class Server(BaseHTTPServer.BaseHTTPRequestHandler):       

    def do_GET(self):
        global app

        message = urllib.unquote( self.path[1:] )
        response = None

        print "\n--------------------\n message:\n   {}".format(message)

        if message.startswith('command/'):
            response = app.send(message[8:])       

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(response)


def register_module(module):
    module.init(app)
    modules[module.name] = module

def start_server():
    HOST, PORT = "192.168.0.150", 80

    print "Listenting on port %d" % PORT

    server = BaseHTTPServer.HTTPServer((HOST, PORT), Server)
    server.serve_forever()

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)

    app = App()

    register_module ( Light1() )
    # register_module ( Notify() )
    register_module ( IR() )
    register_module ( Notify2() )
    # register_module ( Email() )

    start_server()
