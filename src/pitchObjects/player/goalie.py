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
            # if self.ball.outOfPlay:
            #     self.mustPass()
            #     return
            # elif self.wait():
            #     return
            # else:
            if not self.lookToPass(grandObserver):
                self.mustPass()
                return
        elif self.chargeToBall:
            self.chase(self.ball)
            return
        else:
            if self.getWeightedDistanceToGoal(False) > self.ball.posX/4:
                self.chase(self.team.goal)
                return
            if not self.coverObject(self.ball):
                if self.team.hasPossession:
                    if self.ball.target is self:
                        self.chase(self.ball)
                        return
                    else:
                        self.accelerate(self.relX(1, self.team.isDefendingLeft), 0)
                        return



    def wait(self):
        if self.waitTime < 1:
            self.waitTime = STRAT_GOALIE_WAIT
            return False
        else:
            self.waitTime -= 1
            return True