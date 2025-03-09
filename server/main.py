from network.NetworkHandleurThread import NetworkHandleurThread
from network.NetworkHandcheckHandleur import NetworkHandcheckHandleur
from InputHandleurThread import InputHandleurThread

import time
import sys

nertwork = NetworkHandleurThread()
nertwork_handcheck = NetworkHandcheckHandleur()
nertwork.is_handcheck_valid = nertwork_handcheck.is_handcheck_valid

input = InputHandleurThread()

nertwork.start()
input.start()

pulling_rate = 120
alternateur = False

LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'
SAVE =  '\033[s'
RESTORE =  '\033[u'
END =  '\033[99C'

while input.running:
    time.sleep(1/pulling_rate)
    # alternateur = not alternateur
    # print(SAVE, end="")
    # if (alternateur):
    #     print("tick, ....")
        # print(f"\033[F\033[{1}tick, ....")
    # else:
        # print(f"\033[F\033[{1}...., tack")
    #     print("...., tack")
    # print(LINE_UP, end=LINE_CLEAR)
    # print(RESTORE, end="")

    nertwork.send_to_all_register_client(str(nertwork.register_clients_recv) + ";")
    nertwork.clear_register_client_recv()

nertwork.running = False

input.join()
nertwork.join()