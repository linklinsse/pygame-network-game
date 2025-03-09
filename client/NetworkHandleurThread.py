# pylint: disable=broad-except
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
from threading import Condition, Lock, Thread

class NetworkHandleurThread(Thread):
    def __init__(self, ip = '127.0.0.1', port = 3333) -> None:
        super(NetworkHandleurThread, self).__init__()

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.running: bool = False
        self.encoding: str = 'ascii'

        self.ip = ip
        self.port = port
        self.recv_data = ""

    def run(self) -> None:
        self.running = True
        self._sock.settimeout(1)

        while self.running:
            try:
                data, addr = self._sock.recvfrom(65535)
                self.recv_data += data.decode(self.encoding)
            except TimeoutError:
                pass

    def send_message(self, msg: str):
        self._sock.sendto(msg.encode(), (self.ip, self.port))