import math

import pygame

from display.displaymapper import FIELD_WIDTH
from gamevariables import STRAT_BLOCKAGE, STRAT_COVERAGE, STRAT_MIN_PASS


__author__ = 'Thomas'


class GrandObserver:
    def __init__(self, team1, team2, ball):
        self.team1 = team1
        self.team2 = team2

        self.ball = ball

    def analyze(self):
        # TODO: optimize these functions to reduce repeated looping
        if self.team1.hasPossession:
            attackingTeam = self.team1
            defendingTeam = self.team2
        else:
            attackingTeam = self.team2
            defendingTeam = self.team1

        attackingTeam.players.sort(key=lambda x: x.getDistanceToGoalline(True))
        defendingTeam.players.sort(key=lambda x: x.getDistanceToGoalline(False))

        self.findClosestandLastDefenders(defendingTeam)
        self.setCoveredAndBlockedPlayers(attackingTeam, defendingTeam)
        self.setOffsides(attackingTeam)
        self.setOpenPlayers(attackingTeam)
        self.setMarkingsAndClosestAttacker(attackingTeam, defendingTeam)

    def setMarkingsAndClosestAttacker(self, attackingTeam, defendingTeam):
        closestAttacker = attackingTeam.players[0]
        for attackingPlayer in attackingTeam.players:
            for defendingPlayer in sorted(defendingTeam.players, key=lambda x: abs(x.posX - attackingPlayer.posX) + abs(
                            x.posY - attackingPlayer.posY)):
                if not defendingPlayer.marking and pygame.sprite.collide_rect(attackingPlayer,
                                                                              defendingPlayer.homePosition):
                    defendingPlayer.marking = attackingPlayer
                    break

            attackingPlayer.chargeToBall = False
            if attackingPlayer.getDistanceTo(self.ball) < closestAttacker.getDistanceTo(self.ball):
                closestAttacker = attackingPlayer

        closestAttacker.chargeToBall = True

    def findClosestandLastDefenders(self, defendingTeam):
        closestDefender = defendingTeam.players[0]
        stoppingPlayer = defendingTeam.players[0]
        self.openPlayers = []
        self.lastDefender = defendingTeam.players[0]  # This works because it has been sorted earlier
        for defendingPlayer in defendingTeam.players:
            defendingPlayer.blocking = []
            defendingPlayer.covering = []
            defendingPlayer.chargeToBall = False
            defendingPlayer.marking = None

            if defendingPlayer.getDistanceTo(self.ball) < closestDefender.getDistanceTo(self.ball):
                closestDefender = defendingPlayer
            if defendingPlayer.getDistanceToGoalline(False) < self.ball.getDistanceToGoalline(False,
                                                                                              defendingPlayer.team.isDefendingLeft):
                if defendingPlayer.getDistanceTo(self.ball) < closestDefender.getDistanceTo(self.ball):
                    stoppingPlayer = defendingPlayer

        closestDefender.chargeToBall = True
        stoppingPlayer.chargeToBall = True


    def setCoveredAndBlockedPlayers(self, attackingTeam, defendingTeam):
        for attackingPlayer in attackingTeam.players:
            attackingPlayer.blockedBy = []
            attackingPlayer.coveredBy = []
            for defendingPlayer in defendingTeam.players:
                # Check blocked players
                #TODO: use player attributes as modifiers
                if attackingPlayer.getDistanceTo(self.ball) > defendingPlayer.getDistanceTo(self.ball):
                    defendingAngle = math.atan2(self.ball.posX - defendingPlayer.posX,
                                                self.ball.posY - defendingPlayer.posY)
                    passingAngle = math.atan2(self.ball.posX - attackingPlayer.posX,
                                              self.ball.posY - attackingPlayer.posY)
                    angleDif = abs(((defendingAngle - passingAngle + math.pi) % (2 * math.pi)) - math.pi)
                    stratBlockage = STRAT_BLOCKAGE
                    if self.ball.possessor:
                        if defendingPlayer.getDistanceTo(self.ball) < STRAT_MIN_PASS:
                            stratBlockage = math.radians(60)
                    if angleDif < stratBlockage:
                        attackingPlayer.blockedBy += [defendingPlayer]
                        defendingPlayer.blocking += [attackingPlayer]

                # if the defending player is nearby and closer to the goal
                if (attackingPlayer.posX - defendingPlayer.posX) ** 2 + (
                            attackingPlayer.posY - defendingPlayer.posY) ** 2 < STRAT_COVERAGE:
                    if not self.attackerIsCloserToGoalline(attackingPlayer, defendingPlayer):
                        attackingPlayer.coveredBy += [defendingPlayer]
                        defendingPlayer.covering += [attackingPlayer]

    def setOffsides(self, attackingTeam):
        for attackingPlayer in attackingTeam.players:
            if not self.ball.isLoose:
                attackingPlayer.isOffsides = False
                if attackingPlayer.getDistanceToGoalline(True) < FIELD_WIDTH / 2:
                    if self.attackerIsCloserToGoalline(attackingPlayer, self.lastDefender):
                        if self.ball.possessor and attackingPlayer.getDistanceToGoalline(
                                True) < self.ball.possessor.getDistanceToGoalline(True):
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