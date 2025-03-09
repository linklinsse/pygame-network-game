
from threading import Thread

class InputHandleurThread(Thread):

    def __init__(self):
        super(InputHandleurThread, self).__init__()

        self.running: bool = False

    def run(self) -> None:
        self.running = True

        commands = {
            "help": self.print_help,
            "stop": self.stop,
        }

        while self.running:
            cmd = input('> ').lower()
            if cmd in commands.keys():
                commands[cmd]()
            else:
                print('Unknow command, type [help] to see all commands')

    def print_help(self):
        print("[help] to see all commands")
        print("[stop] to stop the server")

    def stop(self):
        print("STOPPING")
        self.running = False