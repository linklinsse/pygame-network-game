
from NetworkHandleurThread import NetworkHandleurThread
from SimpleDisplay import SimpleDisplay
from GameHandleur import GameHandleur


network = NetworkHandleurThread()
display = SimpleDisplay()
game = GameHandleur(display, network)

network.start()
display.start()
game.start()

network.join()
display.join()
game.join()