import socket
from network import Network
from cards import *
import pygame
import random

pygame.init()

SCREEN_WIDTH = pygame.display.Info().current_w - 10
SCREEN_HEIGHT = pygame.display.Info().current_h - 20
# window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
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
                        player.playerCardsSum["jocker"] += 1
                        window.fill(colors["white"])
                        self.changeRoadColor(self.color)
                        break
                    elif colors[color] == self.color:
                        self.clicked = False
                        player.playerCardsSum[color] += 1
                        window.fill(colors["white"])
                        self.changeRoadColor(self.color)
                        break
                        # self.changeRoadColor((0, 255, 0))
            else:
                for color in colors:
                    if colors[color] == self.color:
                        if player.playerCardsSum[color] > 0:
                            self.clicked = True
                            player.playerCardsSum[color] -= 1
                            window.fill(colors["white"])
                            pygame.draw.circle(self.surf, player.color, (5, 5), 7)
                            break
                        elif player.playerCardsSum["jocker"] > 0:
                            self.clicked = True
                            self.jockerSelected = True
                            player.playerCardsSum["jocker"] -= 1
                            window.fill(colors["white"])
                            pygame.draw.circle(self.surf, player.color, (5, 5), 7)
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


class Player():
    def __init__(self, color=colors["blue"]):
        self.id = id
        self.color = color
        self.cards = []
        self.choseCard = None
        self.madeMove = False
        self.deckCardLocation = [190, 282, 374, 466, 558, 650]
        self.playerCards = [Card(colors["pink"], 261, 660, 111, 150), WhiteCard(382, 660, 111, 150),
                            Card(colors["blue"], 503, 660, 111, 150), Card(colors["yellow"], 624, 660, 111, 150),
                            Card(colors["orange"], 745, 660, 111, 150), Card(colors["black"], 866, 660, 111, 150),
                            Card(colors["red"], 987, 660, 111, 150), Card(colors["green"], 1108, 660, 111, 150),
                            JockerCard(1229, 660, 111, 150, r"C:\Users\4emp10n\Downloads\raduga.jpg")]

        self.playerCardsSum = {"pink": 0, "white": 0, "blue": 0, "yellow": 0, "orange": 0, "black": 0, "red": 0,
                               "green": 0,
                               "jocker": 0}

    def addCardsToDeck(self, CardsDeckServer):
        if not len(self.cards):
            self.cards.append(
                CardBack(70, self.deckCardLocation[0], 140, 82, r"C:\Users\4emp10n\Downloads\CardBack.jpg"))
            for i in range(1, 6):
                tempColor = CardsDeckServer[i - 1]
                if tempColor == colors["white"]:
                    self.cards.append(WhiteCard(70, self.deckCardLocation[i], 140, 82))
                elif tempColor == colors["jocker"]:
                    self.cards.append(
                        JockerCard(70, self.deckCardLocation[i], 140, 82, r"C:\Users\4emp10n\Downloads\raduga2.jpg"))
                else:
                    self.cards.append(Card(tempColor, 70, self.deckCardLocation[i], 140, 82))
        else:
            for i in range(1, 6):
                tempColor = CardsDeckServer[i - 1]
                if tempColor == colors["white"]:
                    self.cards[i] = (WhiteCard(70, self.deckCardLocation[i], 140, 82))
                elif tempColor == colors["jocker"]:
                    self.cards[i] = (
                        JockerCard(70, self.deckCardLocation[i], 140, 82, r"C:\Users\4emp10n\Downloads\raduga2.jpg"))
                else:
                    self.cards[i] = (Card(tempColor, 70, self.deckCardLocation[i], 140, 82))

    def chooseCard(self, CardsDeckServer):
        if Card.clickedCounter == 2:
            self.choseCard = True
            for index, card in enumerate(self.cards):
                if card.clicked:
                    if index != 0:
                        for color in self.playerCardsSum:
                            if (colors[color] == colors["white"] and isinstance(card, WhiteCard)) or (
                                    colors[color] == card.color):
                                self.playerCardsSum[color] += 1
                                self.cards[index] = changeCard(card)
                                CardsDeckServer[index - 1] = self.cards[index].color
                                break
                    else:
                        if self.cards[0].deckClickedCounter == 2:
                            self.playerCardsSum[random.choice(list(colors))] += 1
                        self.playerCardsSum[random.choice(list(colors))] += 1
                        self.cards[0] = CardBack(70, self.deckCardLocation[0], 140, 82,
                                                 r"C:\Users\4emp10n\Downloads\CardBack.jpg")
            Card.clickedCounter = 0
            self.addCardsSum()

    # def sendDeckCardsToServer(self, CardsDeckServer):
    #     for i in range(1, 6):
    #         CardsDeckServer[i-1] = self.cards[i]
    #     return CardsDeckServer

    def addCardsSum(self):
        i = 0
        font = pygame.font.SysFont("comicsans", 40)
        for sum in self.playerCardsSum:
            text = font.render("{}".format(self.playerCardsSum[sum]), 1, (0, 0, 0))
            window.blit(text, (self.playerCards[i].rect.x + self.playerCards[i].rect.width / 2 - 15,
                               self.playerCards[i].rect.y + self.playerCards[i].rect.height - 9))

            i += 1


class Game():
    def __init__(self):
        self.player1 = Player(1)
        self.player2 = Player(2)


def randColor(colors):
    colorKey = random.choice(list(colors))
    return colors[colorKey]


# ============Create-Surfaces-END=============


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


def changeCard(card):
    tempColor = randColor(colors)
    if tempColor == colors["white"]:
        card = WhiteCard(70, card.rect.y, 140, 82)
    elif tempColor == colors["jocker"]:
        card = JockerCard(70, card.rect.y, 140, 82, r"C:\Users\4emp10n\Downloads\raduga2.jpg")
    else:
        card = Card(tempColor, 70, card.rect.y, 140, 82)
    return card


btns = [Button((255, 255, 0), 70, 70, 140, 65, "Exit"), Button((255, 255, 0), 1359, 662, 180, 78, "Make Move"),
        Button((255, 255, 0), 1359, 746, 180, 78, "Scip Move"), Button((255, 255, 0), 70, 746, 180, 78, "Choose card")]


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


def compareWithServerDeck(CardsDeckServer, Player):
    for i in range(1, 5):
        if CardsDeckServer[i - 1] != Player.cards[i].color:
            return False
    return True


def client_program():
    players_moves = [0, 0]
    # TIMER Design
    TIMER = pygame.USEREVENT + 1
    pygame.time.set_timer(TIMER, 1000)
    font = pygame.font.SysFont("comicsans", 40)
    timer_time = 60
    timer_text = font.render("00:{x}".format(x=timer_time), 1, (0, 0, 0))
    # TIMER DESIGN-END
    # Network initialize
    net = Network()
    player = Player()
    player.id = net.getPlayer()

    # Network initialize-END
    net.send("GetCards")
    CardsDeckServer = net.recv()  # get deck cards from server

    # players_moves = net.recv()
    # =========Init player==============
    player.addCardsToDeck(CardsDeckServer)

    # if player.id == 1:
    #     player.choseCard = False
    #     player.color = colors["blue"]
    # else:
    #     player.choseCard = True
    #     player.color = colors["orange"]
    # =========Init player-END=========

    running = True
    while running:
        isNew = True
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
                    if btn.click(pos) == "Exit":
                        running = False
                    if btn.click(pos) == "Choose card":
                        window.fill(colors["white"])
                        net.send("Choose card")
                        playersTurn = net.recv()
                        if playersTurn == player.id:
                            player.chooseCard(CardsDeckServer)
                            isNew = False
                            net.send("OK")
                            net.send(CardsDeckServer)
                        else:
                            net.send("NO")

                    if btn.click(pos) == "Make Move":
                        makeMove()

                selectWay(pos)

                for card in player.cards:
                    card.click(pos)
                # wayAB.checkWayBuilding()
                # wayAB.testFunc()

        # ===========Add-Surfaces=============
        # Add timer wo window
        window.blit(timer_text, (90, 133))
        # Add cardDeckSurf
        # window.blit(cardDeckSurf, (70, 190))
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
        # Add deck cards

        net.send("GetTurn")
        playersTurn = net.recv()
        if playersTurn == player.id:
            net.send("GetCards")
            CardsDeckServer = net.recv()
            if not compareWithServerDeck(CardsDeckServer, player):
                player.addCardsToDeck(CardsDeckServer)
                for card in player.cards:
                    window.blit(card.surf, card.rect)
            else:
                for card in player.cards:
                    window.blit(card.surf, card.rect)
        else:
            for card in player.cards:
                window.blit(card.surf, card.rect)

        # Add cards sum
        player.addCardsSum()

        drawCircles()

        # Add player cards
        for card in player.playerCards:
            window.blit(card.surf, card.rect)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    client_program()
