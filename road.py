from cards import *

pygame.init()

MAPSURFLOCATION = (220, 70)


class Road(Button):
    def __init__(self, color, x, y, width=75, height=25):
        super().__init__(color, x, y, width, height)
        self.jockerSelected = False


    def click(self, window, pos, player):
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
    def __init__(self, roads, wayName):
        self.way = roads
        self.wayName = wayName
        self.isBuilt = False
        self.buildBy = None

    def checkWayBuilding(self):
        clickedCounter = 0
        for road in self.way:
            if road.clicked:
                clickedCounter += 1
        if clickedCounter == len(self.way):
            return True
