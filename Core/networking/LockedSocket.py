import socket
import threading


class SocketConnectionClosed(Exception):
    pass


class SocketTimeoutReached(Exception):
    pass


class LockedSocket:
    def __init__(self, sock, recv_size=4096):
        self.recv_lock = threading.Lock()
        self.send_lock = threading.Lock()
        self.locked_socket = sock  # type: socket.socket
        self.recv_size = recv_size

        self.retained_data = ""

        self.socket_open = True

    def send(self, data, separator="\n\n"):
        if not self.socket_open:
            raise SocketConnectionClosed

        self.send_lock.acquire()

        data += separator

        while data != b"":
            try:
                bytes_send = self.locked_socket.send(data)
            except:
                self.retained_data = ""
                self.locked_socket.close()
                self.socket_open = False
                self.send_lock.release()
                raise SocketConnectionClosed

            if bytes_send == 0:
                self.locked_socket.close()
                self.socket_open = False
                self.send_lock.release()
                raise SocketConnectionClosed

            data = data[bytes_send:]

        self.send_lock.release()

    def recv(self, separator="\n\n", max_data_size=1048576, timeout=None):
        if not self.socket_open:
            raise SocketConnectionClosed

        self.recv_lock.acquire()

        self.locked_socket.settimeout(timeout)

        max_data_size += len(separator)

        data = self.retained_data  # type: str

        while True:
            if separator in data:
                break
                
            try:
                received_data = self.locked_socket.recv(self.recv_size)
            except socket.error:
                self.retained_data = ""
                self.locked_socket.close()
                self.socket_open = False
                self.recv_lock.release()
                raise SocketConnectionClosed
            except socket.timeout:
                self.retained_data = ""
                self.recv_lock.release()
                raise SocketTimeoutReached

            if len(received_data) == 0:
                self.retained_data = ""
                self.locked_socket.close()
                self.socket_open = False
                self.recv_lock.release()
                raise SocketConnectionClosed

            data += received_data

            if len(data) > max_data_size:
                break

        data_split = data.split(separator)
        self.retained_data = separator.join(data_message for data_message in data_split[1:])

        self.recv_lock.release()

        return data_split[0]

    def close(self, closing_message=None):
        if closing_message is not None and self.socket_open:
            self.send(closing_message)

        self.locked_socket.close()
        self.socket_open = False
