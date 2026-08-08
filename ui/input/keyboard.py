import copy
from app.lifecycle import resetApp
from constants import BOUNDARY_OFFSET
from ui.input.step import takeStep


def onKeyPress(app, key):
    if not app.isField:
        return
    if key == 'space':
        app.isPaused = not app.isPaused
        if not app.isPlayActive:
            app.isPlayActive = True
            app.lastPlayResult = ''
            app.lastYardsRan = 0
            app.fieldInstructionsButton.isInstructions = False
    elif key == 's':
        takeStep(app)
        if not app.isPlayActive:
            app.isPlayActive = True
            app.fieldInstructionsButton.isInstructions = False
    elif key == 'r':
        resetApp(app)
    elif key == 'p':
        app.isPassRush = not app.isPassRush


def onKeyHold(app, keys):
    if app.isField:
        moveBallCarrier(app, keys)
    elif app.isOffensiveMenu:
        moveSelectedPlayer(app, keys)


def moveBallCarrier(app, keys):
    carrier = app.ball.carrier
    if carrier is None:
        return
    reach = 10 * app.yardStep
    if 'up' in keys:
        carrier.targetY = carrier.cy - reach
    if 'down' in keys:
        carrier.targetY = carrier.cy + reach
    if 'right' in keys:
        carrier.targetX = carrier.cx + reach
    if 'left' in keys:
        carrier.targetX = carrier.cx - reach


def moveSelectedPlayer(app, keys):
    if app.selectedPlayer is None:
        return
    moveAmount = 0.11 * app.yardStep
    player = app.oFormation[app.selectedPlayer]
    if 'up' in keys and nudgePlayer(app, player, 0, -moveAmount, moveAmount,
                                    checkInBoundaryScrimmageLine):
        return
    if 'down' in keys and nudgePlayer(app, player, 0, moveAmount, moveAmount,
                                      checkInBoundaryScrimmageLine):
        return
    if 'right' in keys and nudgePlayer(app, player, moveAmount, 0, moveAmount,
                                       checkInBoundaryLR):
        return
    if 'left' in keys and nudgePlayer(app, player, -moveAmount, 0, moveAmount,
                                      checkInBoundaryLR):
        return
    makeRouteInBounds(app, player)


def nudgePlayer(app, player, dx, dy, moveAmount, boundaryCheck):
    player.startX += dx
    player.startY += dy
    player.cx = player.startX
    player.cy = player.startY
    if boundaryCheck(app, player, moveAmount) is not None:
        return True
    player.route = [(rx + dx, ry + dy) for (rx, ry) in player.route]
    return False


def onKeyRelease(app, key):
    carrier = app.ball.carrier
    if carrier is None:
        return
    if key in ('up', 'down'):
        carrier.targetY = carrier.cy
    elif key in ('left', 'right'):
        carrier.targetX = carrier.cx


def checkInBoundaryLR(app, player, moveAmount):
    if player.cx <= BOUNDARY_OFFSET + app.sideLineOffset:
        player.startX += moveAmount
        player.cx = player.startX
        return "Too Far Left"
    elif player.cx >= app.width - BOUNDARY_OFFSET - app.sideLineOffset:
        player.startX -= moveAmount
        player.cx = player.startX
        return "Too Far Right"
    return None


def checkInBoundaryScrimmageLine(app, player, moveAmount):
    scrimmageLineOffset = 13
    lowerScreenOffset = 15
    if player.cy <= app.lineOfScrimmage + scrimmageLineOffset:
        player.startY += moveAmount
        player.cy = player.startY
        return "Too Far Up"
    elif player.cy >= app.height - lowerScreenOffset:
        player.startY -= moveAmount
        player.cy = player.startY
        return "Too Far Down"
    return None


def makeRouteInBounds(app, player):
    newRoute = copy.deepcopy(player.route)
    for i in range(len(player.route)):
        x, y = player.route[i]
        if x <= app.sideLineOffset + BOUNDARY_OFFSET:
            newRoute[i] = (app.sideLineOffset + BOUNDARY_OFFSET, y)
        if x >= app.width - app.sideLineOffset - BOUNDARY_OFFSET:
            newRoute[i] = (app.width - app.sideLineOffset - BOUNDARY_OFFSET, y)
    player.route = newRoute
