import math
import pygame
from display.displaymapper import FIELD_WIDTH
from gamevariables import STRAT_BLOCKAGE, STRAT_COVERAGE, COLOR_ORANGE

__author__ = 'Thomas'

class GrandObserver:
    def __init__(self, team1, team2, ball):
        self.team1 = team1
        self.team2 = team2

        self.ball = ball

    def analyze(self):
        #TODO: Break this function up
        if self.team1.hasPossession:
            attackingTeam = self.team1
            defendingTeam = self.team2
        else:
            attackingTeam = self.team2
            defendingTeam = self.team1

        closestDefender = defendingTeam.players[0]

        self.openPlayers = []
        lastDefender = defendingTeam.players[0]
        for defendingPlayer in defendingTeam.players:

            defendingPlayer.blocking = []
            defendingPlayer.covering = []
            defendingPlayer.isClosestToBall = False
            defendingPlayer.marking = None

            if defendingPlayer.getDistanceToGoalline(False) < lastDefender.getDistanceToGoalline(False):
                lastDefender = defendingPlayer
            if defendingPlayer.squaredDistanceTo(self.ball) < closestDefender.squaredDistanceTo(self.ball):
                closestDefender = defendingPlayer

        closestDefender.isClosestToBall = True

        self.setCoveredAndBlockedPlayers(attackingTeam, defendingTeam)
        self.setOffsides(attackingTeam, lastDefender)
        self.setOpenPlayers(attackingTeam)

        attackingTeam.players.sort(key=lambda x: x.getWeightedDistanceToGoal(True))
        for attackingPlayer in attackingTeam.players:
            for defendingPlayer in sorted(defendingTeam.players, key=lambda x: abs(x.posX - attackingPlayer.posX) + abs(x.posY - attackingPlayer.posY)):
                if not defendingPlayer.marking and pygame.sprite.collide_rect(attackingPlayer, defendingPlayer.homePosition):
                    defendingPlayer.marking = attackingPlayer
                    break



            # if attackingPlayer.squaredDistanceTo(self.ball) < closestAttacker.squaredDistanceTo(self.ball):
            #     closestAttacker = attackingPlayer

    def setCoveredAndBlockedPlayers(self, attackingTeam, defendingTeam):
        for attackingPlayer in attackingTeam.players:
            attackingPlayer.blockedBy = []
            attackingPlayer.coveredBy = []
            for defendingPlayer in defendingTeam.players:

                #Check blocked players
                #if the defending player is anywhere between the attacker and the ball, run this to save tangent calculations
                #TODO: use player attributes as modifiers
                if self.ball.posX < defendingPlayer.posX < attackingPlayer.posX or self.ball.posX > defendingPlayer.posX > attackingPlayer.posX:
                    #if the defending player might be able to intercept
                    defendingAngle = math.atan2(self.ball.posX - defendingPlayer.posX, self.ball.posY - defendingPlayer.posY)
                    passingAngle = math.atan2(self.ball.posX - attackingPlayer.posX, self.ball.posY - attackingPlayer.posY)
                    angleDif = abs(((defendingAngle - passingAngle + math.pi) % (2*math.pi)) - math.pi)
                    if angleDif < STRAT_BLOCKAGE:
                        attackingPlayer.blockedBy += [defendingPlayer]
                        defendingPlayer.blocking += [attackingPlayer]

                # if the defending player is nearby and closer to the goal
                if (attackingPlayer.posX - defendingPlayer.posX)**2 + (attackingPlayer.posY - defendingPlayer.posY)**2 < STRAT_COVERAGE:
                    if not self.attackerIsCloserToGoalline(attackingPlayer, defendingPlayer):
                        attackingPlayer.coveredBy += [defendingPlayer]
                        defendingPlayer.covering += [attackingPlayer]

    def setOffsides(self, attackingTeam, lastDefender):
        for attackingPlayer in attackingTeam.players:
            if not self.ball.isLoose:
                attackingPlayer.isOffsides = False
                if attackingPlayer.getDistanceToGoalline(True) < FIELD_WIDTH/2:
                    if self.attackerIsCloserToGoalline(attackingPlayer, lastDefender):
                        if self.ball.possessor and attackingPlayer.getDistanceToGoalline(True) < self.ball.possessor.getDistanceToGoalline(True):
                            attackingPlayer.isOffsides = True
                        elif not self.ball.possessor:
                            attackingPlayer.isOffsides = True

    def setOpenPlayers(self, attackingTeam):
        for attackingPlayer in attackingTeam.players:
            if not attackingPlayer.isOffsides and not attackingPlayer.coveredBy and not attackingPlayer.blockedBy:
                self.openPlayers.append(attackingPlayer)

    def attackerIsCloserToGoalline(self, attacker, defender):
        if attacker.getDistanceToGoalline(True) < \
                defender.getDistanceToGoalline(False):
            return True
        else:
            return False