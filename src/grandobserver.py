import math
from gamevariables import STRAT_BLOCKAGE, STRAT_COVERAGE

__author__ = 'Thomas'

class GrandObserver:
    def __init__(self, team1, team2, ball):
        self.team1 = team1
        self.team2 = team2
        self.ball = ball

        self.openPlayers = []

    def analyze(self):
        if self.team1.hasPossession:
            attackingTeam = self.team1
            defendingTeam = self.team2
        else:
            attackingTeam = self.team2
            defendingTeam = self.team1


        self.openPlayers = []
        lastDefender = defendingTeam.players[0]
        for defendingPlayer in defendingTeam.players:
            if defendingPlayer.getDistanceToGoalline(False) < lastDefender.getDistanceToGoalline(False):
                lastDefender = defendingPlayer
                defendingPlayer.blocking = []
                defendingPlayer.covering = []

        for attackingPlayer in attackingTeam.players:

            attackingPlayer.blockedBy = []
            attackingPlayer.coveredBy = []
            for defendingPlayer in defendingTeam.players:

                #Check blocked players
                #if the defending player is anywhere between the attacker and the ball, run this to save tangent calculations
                #TODO: use player attributes as modifiers
                if self.ball.posX < defendingPlayer.posX < attackingPlayer.posX or self.ball.posX > defendingPlayer.posX > attackingPlayer.posX:
                    #if the defending player might be able to intercept
                    if (math.atan2(self.ball.posX - defendingPlayer.posX, self.ball.posY - defendingPlayer.posY) -
                            math.atan2(self.ball.posX - attackingPlayer.posX, self.ball.posY - attackingPlayer.posY)) % (2*math.pi) < STRAT_BLOCKAGE:
                        attackingPlayer.blockedBy += [defendingPlayer]
                        defendingPlayer.blocking += [attackingPlayer]

                # if the defending player is nearby and closer to the goal
                if (attackingPlayer.posX - defendingPlayer.posX)**2 + (attackingPlayer.posY - defendingPlayer.posY)**2 < STRAT_COVERAGE:
                    if not self.attackerIsCloserToGoalline(attackingPlayer, defendingPlayer):
                        attackingPlayer.coveredBy += [defendingPlayer]
                        defendingPlayer.covering += [attackingPlayer]

        #check offsides
        for attackingPlayer in attackingTeam.players:
            if self.attackerIsCloserToGoalline(attackingPlayer, lastDefender) and not self.ball.isLoose:
                attackingPlayer.isOffsides = True
            elif self.ball.isLoose:
                attackingPlayer.isOffsides = False
            if not attackingPlayer.isOffsides:
                self.openPlayers.append(attackingPlayer)


    def attackerIsCloserToGoalline(self, attacker, defender):
        if attacker.getDistanceToGoalline(True) < \
                defender.getDistanceToGoalline(False):
            return True
        else:
            return False