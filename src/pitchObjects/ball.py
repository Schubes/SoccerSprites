import pygame
import math
from display.displaymapper import FIELD_LENGTH, FIELD_WIDTH
from gamevariables import COLOR_BALL, GAME_FPS, MECH_TURNS_UNTOUCHABLE, GRAPH_BALL_SIZE, MECH_BALL_SPEED
from pitchObjects.pitchobject import PitchObject

__author__ = 'Thomas'

class Ball(PitchObject):
    def __init__(self):
        PitchObject.__init__(self, COLOR_BALL, self.getStartingPosX(), self.getStartingPosY(), GRAPH_BALL_SIZE)
        self.image.set_alpha(255)

        self.possessor = None
        self.attackingTeam = None
        self.isLoose = True
        self.target = True
        self.turnsUntouchable = 0

    def getStartingPosX(self):
        return FIELD_LENGTH/2

    def getStartingPosY(self):
        return FIELD_WIDTH/2

    def simShot(self, rightGoal):
        print "Shot Fired!"

        self.possessor.team.hasPossession = False
        self.possessor.hasBall = False
        self.possessor = None
        self.isLoose = True
        self.turnsUntouchable = 0

        goalY = FIELD_WIDTH/2
        if rightGoal:
            goalX = FIELD_LENGTH
        else:
            goalX = 0

        self.velX = (goalX - self.posX)/(abs(goalY - self.posY) + abs(goalX - self.posX)) * MECH_BALL_SPEED
        self.velY = (goalY - self.posY)/(abs(goalY - self.posY) + abs(goalX - self.posX)) * MECH_BALL_SPEED

    def passTo(self, player):
        assert self.possessor is not None
        assert self.possessor.hasBall
        assert self.possessor.team.hasPossession

        self.possessor.hasBall = False
        self.possessor = None
        self.isLoose = True
        self.target = player

        distanceToPlayer = math.sqrt((player.posX - self.posX)**2 + (player.posY - self.posY)**2)
        #the idea is that you kick the ball faster if it is going further, but it's not linear
        self.velX = (player.posX - self.posX)/(abs(player.posY - self.posY) + abs(player.posX - self.posX)) * MECH_BALL_SPEED
        self.velY = (player.posY - self.posY)/(abs(player.posY - self.posY) + abs(player.posX - self.posX)) * MECH_BALL_SPEED

    def update(self, players):
        self.moveBall()
        self.checkOutOfBounds()
        self.evaluateControl(players)
        PitchObject.update(self)

    def moveBall(self):
        #if there is a player controlling the ball, the ball should move with that player
        if self.possessor is not None:
            self.posX = self.possessor.posX
            self.posY = self.possessor.posY
            self.velX = 0
            self.velY = 0
        else:
            PitchObject.move(self)

    def evaluateControl(self, players):
        if self.turnsUntouchable > 0:
            self.turnsUntouchable -= 1
        else:
            players = pygame.sprite.spritecollide(self, players, False)
            if players:
                controlVal = 0
                for player in players:
                    if player.team.isDefendingLeft:
                        controlVal += 1
                    else:
                        controlVal -= 1
                if len(players) > 1:
                    for player in players:
                        if player != self.possessor:
                            if self.possessor:
                                if controlVal == 0:
                                    winningPlayer = player
                                    break
                                elif controlVal > 0 and self.possessor.team.isDefendingLeft:
                                    winningPlayer = self.possessor
                                    break
                                elif controlVal > 0:
                                    if player.team.isDefendingLeft:
                                        winningPlayer = player
                                        break
                                elif controlVal < 0 and not self.possessor.team.isDefendingLeft:
                                    winningPlayer = self.possessor
                                    break
                                else:
                                    if not player.team.isDefendingLeft:
                                        winningPlayer = player
                                        break
                            else:
                                if controlVal == 0:
                                    winningPlayer = player
                                elif controlVal > 0:
                                    if player.team.isDefendingLeft:
                                        winningPlayer = player
                                        break
                                else:
                                    if not player.team.isDefendingLeft:
                                        winningPlayer = player
                                        break


                else:
                    winningPlayer = players[0]

                #remove possesion from previous team
                if self.attackingTeam:
                    self.attackingTeam.hasPossession = False
                    if self.possessor:
                        self.possessor.hasBall = False
                self.target = None

                #select the first player who touched the ball
                self.possessor = winningPlayer
                #set new possesion
                self.isLoose = False
                self.attackingTeam = players[0].team
                self.possessor.hasBall = True
                self.attackingTeam.hasPossession = True
                self.turnsUntouchable = MECH_TURNS_UNTOUCHABLE

    def checkOutOfBounds(self):
        """keep players from running out of bounds"""
        if self.posX > FIELD_LENGTH + self.rect.width:
            self.posX = FIELD_LENGTH + self.rect.width/2
            self.outOfBounds()
        if self.posX < 0 - self.rect.width:
            self.posX = 0 - self.rect.width/2
            self.outOfBounds()
        if self.posY > FIELD_WIDTH + self.rect.height:
            self.posY = FIELD_WIDTH + self.rect.height/2
            self.outOfBounds()
        if self.posY < 0 - self.rect.height:
            self.posY = 0 - self.rect.height/2
            self.outOfBounds()

    def outOfBounds(self):
        self.velX = 0
        self.velY = 0
