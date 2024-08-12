# pylint: disable=broad-except
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
from threading import Condition, Lock, Thread


class NetworkHandleurThread(Thread):

    def __init__(self, port=3333) -> None:
        super(NetworkHandleurThread, self).__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', port))
        self.register_clients = []

        # NEED to be lock
        self.register_clients_recv = {}

        self.lk_queue = Lock()
        self.cv_queue = Condition(self.lk_queue)

        self.running = False
        print('Init on port:', port)

    def run(self) -> None:
        self.running = True
        while self.running:
            data, addr = self.sock.recvfrom(65535)
            self.handle_recv_data(data, addr)

    def handle_recv_data(self, data, addr) -> None:
        if addr in self.register_clients:
            self.handle_register_client_recv(data, addr)
        else:
            self.handle_client_handcheck(data, addr)

    def handle_client_handcheck(self, data, addr) -> None:
        if (data.decode("ascii").find('a') != -1):
            self.register_clients.append(addr)
            print("handcheck: ", addr)
            self.sock.sendto(f"handcheck: OK;id={addr}".encode(), addr)
        else:
            self.sock.sendto("handcheck: KO;".encode(), addr)

    def handle_register_client_recv(self, data, addr) -> None:
        print("from: ", addr, "data: ", data)
        if not self.register_clients_recv.get(addr):
            self.register_clients_recv[addr] = [data.decode("ascii")]
        else:
            self.register_clients_recv[addr].append(data.decode("ascii"))

    def send_to_all_register_client(self, data) -> None:
        for client in self.register_clients:
            self.sock.sendto(data.encode(), client)
