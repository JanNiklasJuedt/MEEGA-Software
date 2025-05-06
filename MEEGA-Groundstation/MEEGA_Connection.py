import socket

class Connection:
    ESRANGE_IP = "10.10.13.locadr"
    ESRANGE_PORT = 8000

    TEST_IP = "192.168.178.31"
    TEST_PORT = 8000

    BUFFERSIZE = 64

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, testing = False):
        if testing:
            ip, port = self.TEST_IP, self.TEST_PORT
        else:
            ip, port = self.ESRANGE_IP, self.ESRANGE_PORT
        try:
            self.socket.connect((ip, port))
        except OSError:
            return False
        return True

    def disconnect(self):
        self.socket.close()

    def get(self):
        try:
            self.data = self.socket.recv(self.BUFFERSIZE)
        except OSError:
            return False
        return self.data is not None
