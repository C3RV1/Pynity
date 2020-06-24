import threading
import LockedSocket


class TwoWaySocket:
    def __init__(self, two_way_socket):
        self.two_way_socket = two_way_socket
        self.on_data = lambda message: None
        self.on_close = lambda: None
        self.on_timeout = lambda: None

        self.timeout = None
        self.max_recv_size = 1048576

        self.recv_thread = None

        self.close_done = False

    def start(self):
        self.recv_thread = threading.Thread(target=self.recv_loop)
        self.recv_thread.start()

    def recv_loop(self):
        while self.socket_open:
            try:
                data = self.two_way_socket.recv(timeout=self.timeout, max_data_size=self.max_recv_size)
            except LockedSocket.SocketConnectionClosed:
                break
            except LockedSocket.SocketTimeoutReached:
                self.on_timeout()
                break
            except:
                break
            try:
                self.on_data(data)
            except Exception as e:
                print "Except: {}".format(repr(e))
                break
        self.close()

    def send(self, data):
        try:
            self.two_way_socket.send(data)
        except LockedSocket.SocketConnectionClosed:
            self.close()

    @property
    def socket_open(self):
        return self.two_way_socket.socket_open

    def close(self, closing_message=None):
        if self.close_done:
            return
        self.close_done = True
        self.two_way_socket.close(closing_message=closing_message)
        self.on_close()
    

