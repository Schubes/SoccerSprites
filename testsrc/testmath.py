import unittest
from controllers.possessioncontroller import PossessionController
from display.displaymapper import FIELD_LENGTH
from gamevariables import COLOR_TEAM_BLUE, COLOR_TEAM_RED
from grandobserver import GrandObserver
from pitchObjects.ball import Ball
from pitchObjects.fieldplayer import FieldPlayer
from team import Team


__author__ = 'Thomas'

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.team1 = Team(True, COLOR_TEAM_BLUE, "Blue Team")
        self.team2 = Team(False, COLOR_TEAM_RED, "Red Team")

        self.possessionController = PossessionController(self.team1, self.team2)
        self.ball = Ball(self.possessionController)

        #first number is team num, second is player number
        self.player11 = FieldPlayer([1,1], self.team1, self.ball, 30, 0)
        self.player12 = FieldPlayer([2,1], self.team1, self.ball, 70, 30)
        self.player13 = FieldPlayer([2,2], self.team1, self.ball, 50, 50)
        self.player14 = FieldPlayer([1,2], self.team1, self.ball, 5, 75)
        self.player15 = FieldPlayer([1,3], self.team1, self.ball, 30, 80)

        self.team1.players = [self.player11, self.player12, self.player13, self.player14, self.player15]

        self.player21 = FieldPlayer([1,2], self.team2, self.ball, 50, 30)
        self.player22 = FieldPlayer([1,1], self.team2, self.ball, 5+(30-5)/2, 30+(75-30)/2)
        self.player23 = FieldPlayer([1,3], self.team2, self.ball, 30, 40)
        self.player24 = FieldPlayer([4,4], self.team2, self.ball, FIELD_LENGTH,0)

        self.team2.players = [self.player21, self.player22, self.player23]

        self.ball.posX = 30
        self.ball.posY = 30
        self.ball.possessor = self.player11
        #TODO: Make it so I don't have to do this twice everywhere
        self.player11.hasBall = True
        self.team1.hasPossession = True

        self.grandObserver = GrandObserver(self.team1, self.team2, self.ball)

    def tearDown(self):
        pass

    def test_getDistanceToGoalline(self):

        #distance to left goalline should be player's posX
        self.assertEquals(self.player11.getDistanceToGoalline(False), self.player11.posX)

        self.assertEquals(self.player21.getDistanceToGoalline(True), self.player21.posX)

        #distance between goallines should be field length
        self.assertEquals(self.player11.getDistanceToGoalline(True) + self.player11.getDistanceToGoalline(False), FIELD_LENGTH)

        self.assertEquals(self.player21.getDistanceToGoalline(True) + self.player21.getDistanceToGoalline(False), FIELD_LENGTH)

    def test_grandObserverTangentBlocking(self):
        self.grandObserver.analyze()

        assert self.player11 in self.grandObserver.openPlayers
        assert self.player12 not in self.grandObserver.openPlayers
        assert self.player13 in self.grandObserver.openPlayers
        assert self.player14 not in self.grandObserver.openPlayers
        assert self.player22 in self.player14.blockedBy
        assert self.player15 not in self.grandObserver.openPlayers

        self.player11 = FieldPlayer([1,1], self.team1, self.ball, 30, 0)
        self.player12 = FieldPlayer([2,1], self.team1, self.ball, 70, 30)
        self.player13 = FieldPlayer([2,2], self.team1, self.ball, 50, 50)
        self.player14 = FieldPlayer([1,2], self.team1, self.ball, 5, 75)
        self.player15 = FieldPlayer([1,3], self.team1, self.ball, 30, 80)

        self.team1.players = [self.player11, self.player12, self.player13, self.player14, self.player15]

        self.player21 = FieldPlayer([1,2], self.team2, self.ball, 50, 30)

        self.ball.posX = 70
        self.ball.posY = 30


    def test_fieldPlayerChasing(self):
        pass

if __name__ == '__main__':
    unittest.main()