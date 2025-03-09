# pylint: disable=broad-except
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
from threading import Condition, Lock, Thread

class NetworkHandleurThread(Thread):

    def __init__(self, port = 3333) -> None:
        super(NetworkHandleurThread, self).__init__()

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind(('', port))
        self._register_clients = []

        # vvvv TODO NEED to be lock
        self.register_clients_recv = {}
        self.lk_queue = Lock()
        self.cv_queue = Condition(self.lk_queue)
        # ^^^^ TODO NEED to be lock

        self.encoding: str = 'ascii'
        self.running: bool = False
        print('Init on port:', port)

    def _handle_recv_data(self, data, addr) -> None:
        if addr in self._register_clients:
            self._handle_register_client_recv(data, addr)
        else:
            self._handle_client_handcheck(data, addr)

    def _handle_client_handcheck(self, data, addr) -> None:
        handcheck_valid, handcheck_msg = self.is_handcheck_valid(data, addr)
        if (handcheck_valid):
            self._register_clients.append(addr)
        if (handcheck_msg):
            self.send_message(handcheck_msg, addr)

    def _handle_register_client_recv(self, data, addr) -> None:
        # print("from: ", addr, "data: ", data)
        if not self.register_clients_recv.get(addr):
            self.register_clients_recv[addr[1]] = [data]
        else:
            self.register_clients_recv[addr[1]].append(data)

    def clear_register_client_recv(self) -> None:
        self.register_clients_recv = {}

    def run(self) -> None:
        self.running = True
        self._sock.settimeout(1)

        while self.running:
            try:
                data, addr = self._sock.recvfrom(65535)
                self._handle_recv_data(data.decode(self.encoding), addr)
            except TimeoutError:
                pass

    def is_handcheck_valid(self, data, addr) -> tuple[bool, str]:
        return True, f"handcheck: OK;id={addr}"

    def send_to_all_register_client(self, data) -> None:
        for client in self._register_clients:
            self._sock.sendto(data.encode(), client)

    def send_message(self, data, addr) -> None:
        self._sock.sendto(data.encode(), addr)
