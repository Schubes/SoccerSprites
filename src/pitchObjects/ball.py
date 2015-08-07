import random
import pygame
import math
from display.displaymapper import FIELD_LENGTH, FIELD_WIDTH
from gamevariables import COLOR_BALL, GRAPH_BALL_SIZE, MECH_BALL_SPEED, MECH_BALL_SIZE, MECH_TURNS_RECOVERING, \
    MECH_PASS_VEL_MODIFIER, MECH_GRASS_FRICTION
from pitchObjects.pitchobject import PitchObject
from pitchObjects.player.goalie import Goalie

__author__ = 'Thomas'

class Ball(PitchObject):
    def __init__(self, possessionController, scoreController, leftGoal, rightGoal):
        PitchObject.__init__(self, COLOR_BALL, self.getStartingPosX(), self.getStartingPosY(), GRAPH_BALL_SIZE)
        self.image.set_alpha(255)

        self.possessionController = possessionController
        self.scoreController = scoreController
        self.leftGoal = leftGoal
        self.rightGoal = rightGoal

        self.possessor = None
        self.prevPossessor = None
        self.isLoose = True
        self.target = None
        self.shot = False
        self.outOfPlay = "Kickoff"

    def update(self, players):
        """ method called by matchturn using existing pygame.sprite implementation"""
        self.move()
        self.checkOutOfBounds()
        PitchObject.update(self)
        self.evaluateControl(players)


    def move(self):
        """ Rolls the ball according to its own velocity or its possessor's, and applies friction coefficient"""
        # if there is a player controlling the ball, the ball should move with that player
        if self.possessor is not None:
            # Put the ball in front of the player
            self.posX = self.possessor.posX
            self.posY = self.possessor.posY
            self.velX = self.possessor.velX
            self.velY = self.possessor.velY
            # I don't really like calling PitchObject.move() twice in one turn, but it puts the ball where I want it
            PitchObject.move(self)
        else:
            speed = (math.sqrt(self.velX**2 + self.velY**2))
            if speed > 0:
                self.velX -= self.velX * MECH_GRASS_FRICTION
                self.velY -= self.velY * MECH_GRASS_FRICTION
        PitchObject.move(self)

    def evaluateControl(self, players):
        """ Checks if anyone is touching the ball, and determines who has won possession """
        players = pygame.sprite.spritecollide(self, players, False)
        if players:
            winningPlayer = self.determinePossessionWinningPlayer(players)
            if winningPlayer:
                self.setPropertiesForPossessionWinningPlayer(winningPlayer)

    def determinePossessionWinningPlayer(self, players):
        """ If there are multiple players touching the ball, the team with the most people touching the ball wins possession.
        If and only if the possessor's team has more players and the possessor is touching the ball,
        the possessor keeps control of the ball.
        """
        winningPlayer = None

        controlVal = 0
        for player in players:
            if self.outOfPlay:
                if not player.team.hasPossession:
                    break
            if not player.recovering:
                if self.possessor:
                    if player.team is self.possessor.team:
                        controlVal += 1
                    else:
                        controlVal -= 1

                    for player in players:
                        if not player.recovering:
                            if controlVal > 0:
                                winningPlayer = self.possessor
                                break
                            elif controlVal <= 0:
                                if player.team is not self.possessor.team:
                                    winningPlayer = player
                                    break
                else:
                    if not player.recovering:
                        winningPlayer = random.choice(players)
                        break

        if type(winningPlayer) is Goalie and len(players) == 1:
            if self.shot:
                if random.random() > .5:
                    winningPlayer = None
                    print "The goalie couldn't stop it"

        return winningPlayer

    def setPropertiesForPossessionWinningPlayer(self, winningPlayer):
        assert winningPlayer

        if not self.possessor is winningPlayer:
            if self.possessor:
                self.possessor.recovering = MECH_TURNS_RECOVERING
                self.possessor.hasBall = False
                self.prevPossessor = self.possessor
            if not winningPlayer.team.hasPossession:
                self.possessionController.setPossession(winningPlayer.team)
            self.possessor = winningPlayer


            self.target = None
            self.isLoose = False
            self.possessor.hasBall = True
            self.shot = False


            if winningPlayer.isOffsides and self.isLoose and not self.outOfPlay:
                print "OFFSIDES!!!!"
                self.linesPersonRuling("SetPiece")

    def shoot(self, targetGoal):
        """ Sends the ball towards the center of the opposing goal."""
        print "Shot Fired!"

        self.shot = True

        self.kicked()
        self.possessionController.noPossession()

        goalY = FIELD_WIDTH/2
        if targetGoal:
            goalX = FIELD_LENGTH
        else:
            goalX = 0

        self.velX = (goalX - self.posX)/(math.sqrt((goalY - self.posY)**2 + (goalX - self.posX)**2)) * MECH_BALL_SPEED
        self.velY = (goalY - self.posY)/(math.sqrt((goalY - self.posY)**2 + (goalX - self.posX)**2)) * MECH_BALL_SPEED

    def passTo(self, player, throughPass):
        """ Sends the ball towards a player, or slightly in front of a player if throughPass is True"""
        assert player is not self
        print "Passed"
        self.kicked()
        self.target = player
        if throughPass:
            difX = player.posX - self.posX + player.velX * self.getDistanceTo(player) * MECH_PASS_VEL_MODIFIER
            difY = player.posY - self.posY + player.velY * self.getDistanceTo(player) * MECH_PASS_VEL_MODIFIER
        else:
            difX = player.posX - self.posX
            difY = player.posY - self.posY
        difMag = math.sqrt(difX**2 + difY**2)
        if difMag > 0:
            self.velX = difX/difMag * MECH_BALL_SPEED
            self.velY = difY/difMag * MECH_BALL_SPEED

    def kicked(self):
        """sets properties when ball is willingly given up"""
        assert self.possessor is not None
        assert self.possessor.hasBall
        assert self.possessor.team.hasPossession

        self.possessor.hasBall = False
        self.possessor.recovering = MECH_TURNS_RECOVERING
        self.prevPossessor = self.possessor
        self.possessor = None
        self.isLoose = True
        self.outOfPlay = None

    def checkOutOfBounds(self):

        if pygame.sprite.collide_rect(self, self.leftGoal):
            self.scoreController.newGoal(True, self.possessionController)
            self.kickOff()
        elif pygame.sprite.collide_rect(self, self.rightGoal):
            self.scoreController.newGoal(False, self.possessionController)
            self.kickOff()


        if self.posX > FIELD_LENGTH + MECH_BALL_SIZE:
            self.posX = FIELD_LENGTH + MECH_BALL_SIZE
            if self.blameTeam():
                self.posX = FIELD_LENGTH - 6
                self.linesPersonRuling("GoalKick")
            else:
                self.posX = FIELD_LENGTH
                self.linesPersonRuling("CornerKick")

        if self.posX < 0 - MECH_BALL_SIZE:
            if self.blameTeam():
                self.posX = 0
                self.linesPersonRuling("CornerKick")
            else:
                self.posX = 6
                self.linesPersonRuling("GoalKick")

        if self.posY > FIELD_WIDTH + MECH_BALL_SIZE:
            self.posY = FIELD_WIDTH + MECH_BALL_SIZE
            self.linesPersonRuling("ThrowIn")

        if self.posY < 0 - MECH_BALL_SIZE:
            self.posY = 0 - MECH_BALL_SIZE
            self.linesPersonRuling("ThrowIn")

    def blameTeam(self):
        """returns whether the last person who touched the ball was defending left"""
        assert self.possessor or self.prevPossessor
        if self.possessor:
            return self.possessor.team.isDefendingLeft
        if self.prevPossessor:
            return self.prevPossessor.team.isDefendingLeft

    def linesPersonRuling(self, typeOfPlay):
        print typeOfPlay
        if typeOfPlay is "CornerKick":
            if self.posY > FIELD_WIDTH/2:
                self.posY = FIELD_WIDTH
            else:
                self.posY = 0
        elif typeOfPlay is "GoalKick":
            if self.posY > FIELD_WIDTH/2:
                self.posY = FIELD_WIDTH/2 + 10
            else:
                self.posY = FIELD_WIDTH/2 - 10

        self.velX = 0
        self.velY = 0

        self.outOfPlay = typeOfPlay
        if self.possessor:
            self.possessor.hasBall = False
        self.possessionController.switchPossession(self)
        self.prevPossessor = self.possessor
        self.possessor = None

        self.target = None
        self.shot = False

    def kickOff(self):
        self.possessor = None
        self.prevPossessor = None
        self.isLoose = True
        self.target = None
        self.shot = False
        self.outOfPlay = "Kickoff"
        self.posX = self.getStartingPosX()
        self.posY = self.getStartingPosY()
        self.velX = 0
        self.velY = 0

    def getStartingPosX(self):
        return FIELD_LENGTH/2

    def getStartingPosY(self):
        return FIELD_WIDTH/2