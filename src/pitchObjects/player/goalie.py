from display.displaymapper import FIELD_WIDTH
from gamevariables import STRAT_GOALIE_WAIT, GRAPH_PLAYER_SIZE, COLOR_ORANGE
from pitchObjects.player.abstractPlayer import AbstractPlayer

__author__ = 'Thomas'

class Goalie(AbstractPlayer):

    def __init__(self, team, ball):

        self.ball = ball
        self.team = team

        self.posX = self.relX(5, self.team.isDefendingLeft)
        self.posY = FIELD_WIDTH/2

        self.waitTime = STRAT_GOALIE_WAIT

        AbstractPlayer.__init__(self, COLOR_ORANGE, self.posX, self.posY, GRAPH_PLAYER_SIZE)


    def update(self, grandObserver):
        self.makeAction(grandObserver)
        AbstractPlayer.update(self)


    def makeAction(self, grandObserver):
        if self.hasBall:
            # if self.wait():
            #     return
            # else:
            self.mustPass()
            return
        elif self.chargeToBall and self.nearBall():
            self.chase(self.ball)
            return
        else:
            if self.cover(self.ball):
                self.accelerate(0,0)
            return

    def wait(self):
        if self.waitTime < 1:
            self.waitTime = STRAT_GOALIE_WAIT
            return False
        else:
            self.waitTime -= 1
            return True