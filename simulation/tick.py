from domain.defense import CoverPlayer, PassRusher
from domain.offense import Lineman, Quarterback, SkillPlayer
from constants import QB_DROPBACK_YARDS
from simulation.cover_two import coordinateCoverTwo


def moveOffense(app):
    for player in app.oFormation.values():
        updateOffensivePlayer(app, player)


def updateOffensivePlayer(app, player):
    if player == app.ball.carrier and not isinstance(player, Lineman):
        player.goToPoint(app)
        player.movePlayer(app)
    elif isinstance(player, Quarterback):
        player.targetX = player.cx
        player.targetY = app.lineOfScrimmage + app.yardStep * QB_DROPBACK_YARDS
        player.goToPoint(app)
        player.cx += player.dx
        player.cy += player.dy
    elif isinstance(player, SkillPlayer):
        updateSkillPlayer(app, player)


def updateSkillPlayer(app, player):
    ball = app.ball
    if ball.targetX is not None and ball.targetY is not None and not ball.beingSnapped:
        player.trackBall(app)
    elif ball.carrier == app.oFormation['QB']:
        player.runRoute(app)
    elif player == ball.carrier:
        player.runWithBall(app)
    else:
        player.block(app)


def moveDefense(app):
    if app.coverageShell == 'Cover 2':
        coordinateCoverTwo(app)
    for player in app.dFormation.values():
        if isinstance(player, CoverPlayer):
            updateCoverPlayer(app, player)
        elif isinstance(player, PassRusher):
            player.rushQB(app)
            if app.ball.carrier == app.oFormation['QB']:
                player.checkTackle(app)


def updateCoverPlayer(app, player):
    ball = app.ball
    qb = app.oFormation['QB']
    if ball.targetX is not None and ball.targetY is not None and not ball.beingSnapped:
        player.trackBall(app)
    elif (ball.carrier == qb and qb.cy > app.lineOfScrimmage) or ball.beingSnapped:
        player.guardMan(app)
    else:
        player.stopPlayer(app, ball.carrier)
        player.checkTackle(app)
