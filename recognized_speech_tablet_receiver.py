

import qi
import sys
import os
import time
import socket

class NaoqiTabletSocketReceiver:

    def __init__(self, ip, port):

        try:
            connection_url = "tcp://{}:{}".format(ip, port)
            self.app = qi.Application(url=connection_url)
            self.app.start()
        except RuntimeError:
            print("Can't connect to Naoqi.")
            sys.exit(1)

        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #avoid bugs with closed sockets
            self.s.bind((socket.gethostname(), 1620))
            self.s.listen(5)
            print("Socket Receiver initialized!")
        except Exception, e:
            "Failed to initialize socket receiver with error: ", e

    def run(self):
        try:
            session = self.app.session
            tabletService = session.service("ALTabletService")
            dir_path = "/opt/aldebaran/www/apps/"
            clientsocket, address = self.s.accept()
            self.s.setblocking(False)
            while True:
                recognized_speech = clientsocket.recv(4096)
                print(recognized_speech)
                with open(os.path.join(dir_path, "temp.html"), "wb") as f:
                    f.write('<html><meta name="viewport" content="width=1280, user-scalable=no" /><body bgcolor="#E6E6FA"><center><h1><font size="7"><br><br><br><br>' + recognized_speech + '</font></h1></center></html>')
                tabletService.showWebview("http://198.18.0.1/apps/temp.html")
            clientsocket.close()
        except Exception, e:
                print "Error was: ", e

if __name__ == "__main__":
    ip = "192.168.1.100" # IP of the robot
    port = 9559
    NaoqiTabletSocketReceiver(ip, port).run()
