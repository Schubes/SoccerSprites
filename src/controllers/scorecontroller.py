__author__ = 'Thomas'


class ScoreController:
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2

    def newGoal(self, leftGoal, possessionController):
        if self.team1.isDefendingLeft is not leftGoal:
            self.team1.score += 1
            possessionController.setPossession(self.team2)
        elif self.team2.isDefendingLeft is not leftGoal:
            self.team2.score += 1
            possessionController.setPossession(self.team1)

