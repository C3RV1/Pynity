import LockedSocket
import utils
import re
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import random, get_random_bytes
import os
import time


class HandshakeError(Exception):
    def __init__(self):
        pass


class EncryptionError(Exception):
    def __init__(self):
        pass


class MissingRSAKey(Exception):
    def __init__(self):
        pass
        

class EncryptedSocket:
    def __init__(self, locked_socket, key_path, is_server=False, key_size=2048):
        self.locked_socket = locked_socket  # type: LockedSocket

        if not os.path.isfile(key_path):
            if is_server:
                EncryptedSocket.generate_keys(key_size, key_path, key_path + ".pk")
            else:
                raise MissingRSAKey

        key_file = open(key_path, "rb")
        key_str = key_file.read()
        key_file.close()

        self.key = RSA.importKey(key_str)
        self.is_server = is_server
        self.handshake_done = False

        self.session_key = ""

    def handshake(self):
        self.handshake_done = True
        try:
            if self.is_server:
                self.server_handshake()
            else:
                self.client_handshake()
        except Exception as e:
            self.close()
            raise e

    def server_handshake(self):
        try:
            handshake_init = self.locked_socket.recv(timeout=10, max_data_size=1024)
        except:
            raise HandshakeError

        handshake_init_re = re.search("^session:(.+)$", handshake_init)

        if not handshake_init_re:
            raise HandshakeError

        session_key_b64 = handshake_init_re.group(1)
        if not utils.isBase64(session_key_b64):
            raise HandshakeError

        session_key_rsa_encrypted = utils.base64_decode(session_key_b64)

        self.session_key = PKCS1_OAEP.new(self.key).decrypt(session_key_rsa_encrypted)
        if len(self.session_key) != 16 and len(self.session_key) != 32 and len(self.session_key) != 24:
            raise HandshakeError

        try:
            handshake_verify = self.send("handshake_verify")
        except LockedSocket.SocketConnectionClosed:
            raise LockedSocket.SocketConnectionClosed
        except EncryptionError:
            raise EncryptionError

        try:
            handshake_client_verify = self.recv(max_data_size=1024, timeout=2)
        except Exception as e:
            raise HandshakeError
        if handshake_client_verify != "handshake_verify2":
            raise HandshakeError

    def client_handshake(self):
        self.session_key = ""
        while not len(self.session_key) == 32:
            self.session_key = get_random_bytes(32)

        session_key_encrypted = PKCS1_OAEP.new(self.key).encrypt(self.session_key)
        session_key_b64 = utils.base64_encode(session_key_encrypted)

        self.locked_socket.send("session:{}".format(session_key_b64))

        try:
            handshake_server_verify = self.recv()
        except Exception as e:
            raise HandshakeError

        if handshake_server_verify != "handshake_verify":
            raise HandshakeError

        try:
            self.send("handshake_verify2")
        except:
            raise HandshakeError

    def send(self, msg):
        if not self.handshake_done:
            raise HandshakeError
        try:
            msg_encrypted = utils.encryptWithPadding(self.session_key, msg)
        except Exception as e:
            raise EncryptionError
        if not msg_encrypted[0]:
            raise EncryptionError
        self.locked_socket.send(msg_encrypted[1])

    def recv(self, max_data_size=1048576, timeout=None):
        if not self.handshake_done:
            raise HandshakeError
        msg_encrypted = self.locked_socket.recv(timeout=timeout,
                                                max_data_size=utils.fromByteToB64Length(max_data_size))
        try:
            msg_decrypted = utils.decryptWithPadding(self.session_key, msg_encrypted)
        except:
            raise EncryptionError
        if not msg_encrypted[0]:
            raise EncryptionError
        return msg_decrypted[1]

    def close(self, closing_message=None):
        if self.socket_open and closing_message is not None:
            self.send(closing_message)
        self.locked_socket.close()

    @property
    def socket_open(self):
        return self.locked_socket.socket_open

    @staticmethod
    def generate_keys(key_size, sk_path, pk_path):
        new_key = RSA.generate(key_size)
        new_skey = new_key.export_key()
        new_pkey = new_key.publickey().export_key()

        sk_file = open(sk_path, "wb")
        sk_file.write(new_skey)
        sk_file.close()
        pk_file = open(pk_path, "wb")
        pk_file.write(new_pkey)
        pk_file.close()
