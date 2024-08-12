from networkHandleur import NetworkHandleurThread
import time

nertwork = NetworkHandleurThread()
nertwork.start()

game_tick = 1
while True:
    time.sleep(1/game_tick)
    print("tick, tack")
    nertwork.send_to_all_register_client(str(nertwork.register_clients_recv))
    nertwork.register_clients_recv = {}
