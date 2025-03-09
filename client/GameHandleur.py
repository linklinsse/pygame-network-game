from threading import Thread
from NetworkHandleurThread import NetworkHandleurThread
from SimpleDisplay import SimpleDisplay
import time
import ast

class GameHandleur(Thread):
    def __init__(self, display: SimpleDisplay, network: NetworkHandleurThread) -> None:
        super(GameHandleur, self).__init__()

        self.display = display
        self.network = network

        self.my_id = 0
        self.game_tick = 120

    def run(self):
        if not self._handcheck():
            return

        while not self.display.done:
            time.sleep(1/self.game_tick)
            data = self.network.recv_data.split(";")[0]
            if len(data) <= 1:
                continue
            data = ast.literal_eval(data.replace("[", "\"").replace("]", "\""))
            for key in data.keys():
                if (str(key) != str(self.my_id)):
                    self.display.upd_entitie(key, data[key])

            if len(self.display.entities) >= 1 :
                self.network.send_message("{x: " + str(self.display.entities[0].rect.x) + ", y: " + str(self.display.entities[0].rect.y) + "}")

            self.network.recv_data = ""

    def _handcheck(self) -> bool:
        handcheck_retry = 3

        self.network.send_message("pass hello!")
        while not self.display.done and handcheck_retry > 0:
            time.sleep(1/self.game_tick)
            if "ok;" in self.network.recv_data:
                self.my_id = self.network.recv_data.split(";")[1]
                print("Me is " + self.my_id)
            else:
                handcheck_retry -= 1
            self.network.recv_data = ""
            return True

        print("no handcheck found")
        self.display.done = True
        return False