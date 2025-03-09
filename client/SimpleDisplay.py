import pygame

from threading import Thread

PLAYER_SPEED = 2
class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.color = color
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.change_y = 0
        self.change_x = 0

    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    def move(self):
        self.rect.x = self.rect.x + self.change_x
        self.rect.y = self.rect.y + self.change_y

    def get_data(self) -> str:
        return "{x: " + str(self.rect.x) + ", y: " + str(self.rect.y) + "}"


class SimpleDisplay(Thread):
    def __init__(self) -> None:
        super(SimpleDisplay, self).__init__()

        my_player = Player(100, 100, (255, 0, 0))
        self.done = False
        self.entities = [my_player]
        self.map_entities = {0: my_player}
        self.screen = None

    def run(self):
        # pygame.init()
        clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode([825, 615])
        pygame.display.set_caption('Game')

        while self.done != True :
            self._event_handler()

            self.entities[0].move()
            self.entities[0].changespeed(0, 0)

            self._update_display()
            clock.tick(60)

        pygame.quit()

    def _event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.entities[0].changespeed(-PLAYER_SPEED, 0)
                if event.key == pygame.K_RIGHT:
                    self.entities[0].changespeed(PLAYER_SPEED, 0)
                if event.key == pygame.K_UP:
                    self.entities[0].changespeed(0, -PLAYER_SPEED)
                if event.key == pygame.K_DOWN:
                    self.entities[0].changespeed(0, PLAYER_SPEED)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.entities[0].changespeed(PLAYER_SPEED, 0)
                if event.key == pygame.K_RIGHT:
                    self.entities[0].changespeed(-PLAYER_SPEED, 0)
                if event.key == pygame.K_UP:
                    self.entities[0].changespeed(0, PLAYER_SPEED)
                if event.key == pygame.K_DOWN:
                    self.entities[0].changespeed(0, -PLAYER_SPEED)

    def _update_display(self):
        self.screen.fill((0,0,0))
        for truc in self.entities :
            self.screen.blit(truc.image, (truc.rect.x, truc.rect.y))
        pygame.display.flip()

    def upd_entitie(self, key, action):
        data = {
            'x': int(action.split("x: ")[1].split(",")[0]),
            'y': int(action.split("y: ")[1].split("}")[0]),
        }

        if (key in self.map_entities.keys()):
            self.map_entities[key].rect.x = data['x']
            self.map_entities[key].rect.y = data['y']
        else:
            new_p = Player(data['x'], data['y'], (0,0, 255))
            self.entities.append(new_p)
            self.map_entities[key] = new_p