import socket
from network import Network
import pygame
import random

colors = {"pink": (148, 0, 211), "white": (255, 255, 255), "blue": (0, 0, 128), "yellow": (255, 255, 0),
          "orange": (210, 105, 30), "black": (0, 0, 0), "red": (255, 0, 0), "green": (0, 128, 0),
          "jocker": "jocker"}

pygame.init()

SCREEN_WIDTH = pygame.display.Info().current_w - 10
SCREEN_HEIGHT = pygame.display.Info().current_h - 20
#window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
window.fill((255, 255, 255))

# ============Create-Surfaces=============
# CardDeckSurf
cardDeckSurf = pygame.Surface((140, 550))
cardDeckSurf.fill((255, 255, 255))

# PlayerCardDeckSurf
playerCardDeckSurf = pygame.Surface((1100, 165))
playerCardDeckSurf.fill((255, 255, 255))

# MapSurf
mapSurf = pygame.Surface((1320, 580))
mapSurf.fill((255, 0, 255))
MAPSURFLOCATION = (220, 70)


def randColor(colors):
    colorKey = random.choice(list(colors))
    return colors[colorKey]


# ============Create-Surfaces-END=============
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

    def click(self):
        x1 = pos[0]
        y1 = pos[1]
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


class Road(Button):
    def __init__(self, color, x, y, width=75, height=25):
        super().__init__(color, x, y, width, height)
        self.jockerSelected = False

    def click(self, pos, player):
        x1 = pos[0]
        y1 = pos[1]
        if self.rect.x + MAPSURFLOCATION[0] <= x1 <= MAPSURFLOCATION[
            0] + self.rect.x + self.rect.width and self.rect.y + MAPSURFLOCATION[1] <= y1 <= MAPSURFLOCATION[
            1] + self.rect.y + self.height:
            if self.clicked:
                for color in colors:
                    if self.jockerSelected:
                        self.clicked = False
                        self.jockerSelected = False
                        playerCardsSum["jocker"] += 1
                        window.fill(colors["white"])
                        self.changeRoadColor(self.color)
                        break
                    elif colors[color] == self.color:
                        self.clicked = False
                        playerCardsSum[color] += 1
                        window.fill(colors["white"])
                        self.changeRoadColor(self.color)
                        break
                        # self.changeRoadColor((0, 255, 0))
            else:
                for color in colors:
                    if colors[color] == self.color:
                        if playerCardsSum[color] > 0:
                            self.clicked = True
                            playerCardsSum[color] -= 1
                            window.fill(colors["white"])
                            pygame.draw.circle(self.surf, player, (5, 5), 7)
                            break
                        elif playerCardsSum["jocker"] > 0:
                            self.clicked = True
                            self.jockerSelected = True
                            playerCardsSum["jocker"] -= 1
                            window.fill(colors["white"])
                            pygame.draw.circle(self.surf, player, (5, 5), 7)
                            break

    def changeRoadColor(self, color):
        self.color = color
        self.surf.fill(self.color)

    def getBottomRight(self):
        return self.rect.x, self.rect.y


class Way:
    def __init__(self, roads):
        self.way = roads
        self.isBuilt = False

    def checkWayBuilding(self):
        clickedCounter = 0
        for road in self.way:
            if road.clicked:
                clickedCounter += 1
        if clickedCounter == len(self.way):
            return True



class cityName:
    def __init__(self, name, x, y):
        self.font = font = pygame.font.SysFont("comicsans", 40)
        self.name = font.render(name, 1, (255, 255, 255))
        self.x = x
        self.y = y


wayAE = Way([Road(colors["green"], 372, 272), Road(colors["green"], 457, 272), Road(colors["green"], 542, 272)])
wayEB = Way([Road(colors["yellow"], 657, 272), Road(colors["yellow"], 742, 272), Road(colors["yellow"], 827, 272)])
wayDE = Way([Road(colors["red"], 625, 185, 25, 75)])
wayCE = Way([Road(colors["white"], 625, 312, 25, 75), Road(colors["white"], 625, 397, 25, 75)])

cities = [cityName("A", 340, 255), cityName("E", 625, 255), cityName("B", 905, 255),
          cityName("D", 625, 133), cityName("C", 625, 465)]
ways = [wayAE, wayEB, wayDE, wayCE]
# cards = [Card((randColor(colors)), 70, 190, 140, 82), Card((randColor(colors)), 70, 282, 140, 82),
#          Card((randColor(colors)), 70, 374, 140, 82),
#          Card((randColor(colors)), 70, 466, 140, 82), Card((randColor(colors)), 70, 558, 140, 82),
#          Card((randColor(colors)), 70, 650, 140, 82)]

cards = []
deckCardLocation = [190, 282, 374, 466, 558, 650]

cards.append(CardBack(70, deckCardLocation[0], 140, 82, r"C:\Users\4emp10n\Downloads\CardBack.jpg"))
for i in range(1, 6):
    tempColor = randColor(colors)
    if tempColor == colors["white"]:
        cards.append(WhiteCard(70, deckCardLocation[i], 140, 82))
    elif tempColor == colors["jocker"]:
        cards.append(JockerCard(70, deckCardLocation[i], 140, 82, r"C:\Users\4emp10n\Downloads\raduga2.jpg"))
    else:
        cards.append(Card(tempColor, 70, deckCardLocation[i], 140, 82))


def changeCard(card):
    tempColor = randColor(colors)
    if tempColor == colors["white"]:
        card = WhiteCard(70, card.rect.y, 140, 82)
    elif tempColor == colors["jocker"]:
        card = JockerCard(70, card.rect.y, 140, 82, r"C:\Users\4emp10n\Downloads\raduga2.jpg")
    else:
        card = Card(tempColor, 70, card.rect.y, 140, 82)
    return card


playerCards = [Card(colors["pink"], 261, 660, 111, 150), WhiteCard(382, 660, 111, 150),
               Card(colors["blue"], 503, 660, 111, 150), Card(colors["yellow"], 624, 660, 111, 150),
               Card(colors["orange"], 745, 660, 111, 150), Card(colors["black"], 866, 660, 111, 150),
               Card(colors["red"], 987, 660, 111, 150), Card(colors["green"], 1108, 660, 111, 150),
               JockerCard(1229, 660, 111, 150, r"C:\Users\4emp10n\Downloads\raduga.jpg")]

playerCardsSum = {"pink": 0, "white": 0, "blue": 0, "yellow": 0, "orange": 0, "black": 0, "red": 0, "green": 0,
                  "jocker": 0}

btns = [Button((255, 255, 0), 70, 70, 140, 65, "Exit"), Button((255, 255, 0), 1359, 662, 180, 78, "Make Move"),
        Button((255, 255, 0), 1359, 746, 180, 78, "Scip Move"), Button((255, 255, 0), 70, 746, 180, 78, "Choose card")]


def addCardsSum(playerCards, playerCardsSum):
    i = 0
    for sum in playerCardsSum:
        text = font.render("{}".format(playerCardsSum[sum]), 1, (0, 0, 0))
        window.blit(text, (playerCards[i].rect.x + playerCards[i].rect.width / 2 - 15,
                           playerCards[i].rect.y + playerCards[i].rect.height - 9))

        i += 1


def drawCircles():
    circle_pos = [25, 25]
    while True:  # To draw cicrles from left to right
        pygame.draw.circle(window, (0, 0, 255), circle_pos, 20)
        circle_pos[0] += 50
        if circle_pos[0] >= 1600:
            circle_pos[0] -= 50
            break

    while True:  # To draw cicrles from right to down
        pygame.draw.circle(window, (0, 0, 255), circle_pos, 20)
        circle_pos[1] += 50
        if circle_pos[1] >= 900:
            circle_pos[1] -= 50
            break

    while True:  # To draw cicrles from right to left
        pygame.draw.circle(window, (0, 0, 255), circle_pos, 20)
        circle_pos[0] -= 50
        if circle_pos[0] <= 0:
            circle_pos[0] += 50
            break

    while True:  # To draw cicrles from left to up
        pygame.draw.circle(window, (0, 0, 255), circle_pos, 20)
        circle_pos[1] -= 50
        if circle_pos[1] <= 0:
            circle_pos[1] += 50
            break


def checkMouse():
    if pygame.mouse.get_pos()[0] > SCREEN_WIDTH:
        pygame.mouse.set_pos((SCREEN_WIDTH, pygame.mouse.get_pos()[1]))
    elif pygame.mouse.get_pos()[1] > SCREEN_HEIGHT:
        pygame.mouse.set_pos((pygame.mouse.get_pos()[0], SCREEN_HEIGHT))


def chooseCard():
    if Card.clickedCounter == 2:
        for index, card in enumerate(cards):
            if card.clicked:
                if index != 0:
                    for color in playerCardsSum:
                        if (colors[color] == colors["white"] and isinstance(card, WhiteCard)) or (
                                colors[color] == card.color):
                            playerCardsSum[color] += 1
                            cards[index] = changeCard(card)
                            break
                else:
                    if cards[0].deckClickedCounter == 2:
                        playerCardsSum[random.choice(list(colors))] += 1
                    playerCardsSum[random.choice(list(colors))] += 1
                    cards[0] = CardBack(70, deckCardLocation[0], 140, 82, r"C:\Users\4emp10n\Downloads\CardBack.jpg")
        Card.clickedCounter = 0
        addCardsSum(playerCards, playerCardsSum)


def makeMove():
    for way in ways:
        if not way.isBuilt and way.checkWayBuilding():
            way.isBuilt = True

def selectWay(pos):
    selectedWay = None
    isRoadSelected = False
    for wayName in ways:
        if not wayName.isBuilt:
            for road in wayName.way:
                if road.clicked:
                    isRoadSelected = True
                    selectedWay = wayName
                    break

    if not isRoadSelected:
        for wayName in ways:
            if not wayName.isBuilt:
                for road in wayName.way:
                    road.click(pos, colors["blue"])
    elif isRoadSelected:
        for road in selectedWay.way:
            road.click(pos, colors["blue"])



# TIMER Design
TIMER = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER, 1000)
font = pygame.font.SysFont("comicsans", 40)
timer_time = 60
timer_text = font.render("00:{x}".format(x=timer_time), 1, (0, 0, 0))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == TIMER:
            timer_time -= 1
            timer_text = font.render("00:{x}".format(x=timer_time), 1, (0, 0, 0))
            window.fill(colors["white"])
            window.blit(timer_text, (90, 133))
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for btn in btns:
                if btn.click() == "Exit":
                    running = False
                if btn.click() == "Choose card":
                    window.fill(colors["white"])
                    chooseCard()
                if btn.click() == "Make Move":
                    makeMove()

            selectWay(pos)

            for card in cards:
                card.click(pos)
            # wayAB.checkWayBuilding()
            # wayAB.testFunc()

    # ===========Add-Surfaces=============
    # Add timer wo window
    window.blit(timer_text, (90, 133))
    # Add cardDeckSurf
    window.blit(cardDeckSurf, (70, 190))
    # Add playerCardDeckSurf
    window.blit(playerCardDeckSurf, (250, 660))
    # Add mapSurf
    window.blit(mapSurf, MAPSURFLOCATION)
    # ===========Add-Surfaces-END=============

    # Add roads
    for wayName in ways:
        for road in wayName.way:
            mapSurf.blit(road.surf, road.rect)

    # Add cities
    for city in cities:
        mapSurf.blit(city.name, (city.x, city.y))

    # Add btns
    for btn in btns:
        if btn.text == "Exit":
            btn.surf.fill(btn.color)
            btn.addText(20, -5, 50)

        if btn.text == "Choose card":
            btn.surf.fill(btn.color)
            btn.addText(6, 15, 30)
        window.blit(btn.surf, btn.rect)
    # Add cards
    for card in cards:
        window.blit(card.surf, card.rect)

    # Add cards sum
    addCardsSum(playerCards, playerCardsSum)

    drawCircles()

    # Add player cards
    for card in playerCards:
        window.blit(card.surf, card.rect)
    pygame.display.flip()
pygame.quit()







def client_program():

    net = Network()
    net.connect()

    while True:
        net.send()
        #client_socket.send(message.encode())  # send message
        #data = client_socket.recv(1024).decode()  # receive response
        data = net.recv()
        print('Received from server: ' + data)  # show in terminal
        net.send()
    net.close()

if __name__ == '__main__':
    client_program()