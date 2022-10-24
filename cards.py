import pygame

pygame.init()

colors = {"pink": (148, 0, 211), "white": (255, 255, 255), "blue": (0, 0, 128), "yellow": (255, 255, 0),
          "orange": (210, 105, 30), "black": (0, 0, 0), "red": (255, 0, 0), "green": (0, 128, 0),
          "jocker": "jocker"}


class Button:
    def __init__(self, color, x, y, width=100, height=40, text=""):
        self.color = color
        self.width = width
        self.height = height
        self.surf = pygame.Surface((self.width, self.height))
        if color != colors["jocker"]:
            self.surf.fill(self.color)
        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
        self.text = text
        self.addText()

    def addText(self, text_x=15, text_y=15, size=30):
        font = pygame.font.SysFont("comicsans", size)
        if self.color == (0, 0, 0):
            text = font.render(self.text, 1, (255, 255, 255))
        else:
            text = font.render(self.text, 1, (0, 0, 0))
        self.surf.blit(text, (text_x, text_y))

    def click(self, pos1):
        x1 = pos1[0]
        y1 = pos1[1]
        if self.rect.x <= x1 <= self.rect.x + self.rect.width and self.rect.y <= y1 <= self.rect.y + self.height:
            return self.text


class Card(Button):
    def __init__(self, color, x, y, width, height):
        super().__init__(color, x, y, width, height)

    clickedCounter = 0

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.rect.x <= x1 <= self.rect.x + self.rect.width and self.rect.y <= y1 <= self.rect.y + self.height:
            if not self.clicked and Card.clickedCounter < 2:
                self.clicked = True
                Card.clickedCounter += 1
                self.text = '.'
                self.addText(65, -8, 50)
            elif self.clicked:
                self.clicked = False
                Card.clickedCounter -= 1
                self.surf.fill(self.color)


class JockerCard(Card):
    def __init__(self, x, y, width, height, imgPath):
        super(JockerCard, self).__init__(colors["jocker"], x, y, width, height)
        self.imgPath = imgPath
        self.surf = pygame.image.load(self.imgPath)
        self.surf = pygame.transform.scale(self.surf, (self.width, self.height))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.rect.x <= x1 <= self.rect.x + self.rect.width and self.rect.y <= y1 <= self.rect.y + self.height:
            if not self.clicked and Card.clickedCounter < 1:
                self.clicked = True
                Card.clickedCounter += 2
                self.text = '.'
                self.addText(65, -8, 50)
            elif self.clicked:
                self.clicked = False
                Card.clickedCounter -= 2
                self.surf = pygame.image.load(self.imgPath)
                self.surf = pygame.transform.scale(self.surf, (self.width, self.height))


class CardBack(JockerCard):
    def __init__(self, x, y, width, height, imgPath):
        super(CardBack, self).__init__(x, y, width, height, imgPath)
        self.deckClickedCounter = 0

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.rect.x <= x1 <= self.rect.x + self.rect.width and self.rect.y <= y1 <= self.rect.y + self.height:
            if Card.clickedCounter == 0:
                self.clicked = True
                Card.clickedCounter += 1
                self.deckClickedCounter += 1
                self.text = '.'
                self.addText(65, -8, 50)
            elif Card.clickedCounter == 1 and self.deckClickedCounter == 0:
                self.clicked = True
                Card.clickedCounter += 1
                self.deckClickedCounter += 1
                self.text = '.'
                self.addText(65, -8, 50)
            elif Card.clickedCounter == 1 and self.deckClickedCounter == 1:
                self.clicked = True
                Card.clickedCounter += 1
                self.deckClickedCounter += 1
                self.text = '..'
                self.addText(65, -8, 50)
            elif Card.clickedCounter == 2 and self.deckClickedCounter == 1:
                self.clicked = False
                Card.clickedCounter -= 1
                self.deckClickedCounter -= 1
                self.surf = pygame.image.load(self.imgPath)
                self.surf = pygame.transform.scale(self.surf, (self.width, self.height))
            elif Card.clickedCounter == 2 and self.deckClickedCounter == 2:
                self.clicked = False
                Card.clickedCounter -= 2
                self.deckClickedCounter -= 2
                self.surf = pygame.image.load(self.imgPath)
                self.surf = pygame.transform.scale(self.surf, (self.width, self.height))


class WhiteCard(Card):
    def __init__(self, x, y, width, height):
        super(WhiteCard, self).__init__(colors["black"], x, y, width, height)
        self.innerSurf = pygame.Surface((width - 10, height - 10))
        self.innerSurf.fill(colors["white"])
        self.surf.blit(self.innerSurf, (5, 5))

    def addTextForWhiteCard(self, text_x=15, text_y=15, size=30):
        font = pygame.font.SysFont("comicsans", size)
        if self.color == (0, 0, 0):
            text = font.render(self.text, 1, (0, 0, 0))
        else:
            text = font.render(self.text, 1, (255, 255, 255))
        self.innerSurf.blit(text, (text_x, text_y))
        self.surf.blit(self.innerSurf, (5, 5))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.rect.x <= x1 <= self.rect.x + self.rect.width and self.rect.y <= y1 <= self.rect.y + self.height:
            if not self.clicked and Card.clickedCounter < 2:
                self.clicked = True
                Card.clickedCounter += 1
                self.text = '.'
                self.addTextForWhiteCard(60, -13, 50)
            elif self.clicked:
                self.clicked = False
                Card.clickedCounter -= 1
                self.innerSurf.fill(colors["white"])
                self.surf.blit(self.innerSurf, (5, 5))
