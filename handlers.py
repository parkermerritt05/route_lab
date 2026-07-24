from importExport import importData, exportData
from cmu_graphics import *
from classes import *
from constants import *
from init import initializeDefense, resetApp
import copy

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
    # Returns True when the move pushed the player out of bounds (and was
    # reverted), signaling the caller to stop before shifting the route.
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

def onMouseMove(app, mx, my):
    if app.isMainMenu:
        app.isMainMenuLabelHovering = inStartButton(app, mx, my)
        return
    for button in visibleButtons(app):
        button.updateHover(mx, my)

def onMousePress(app, mx, my):
    app.exportButton.text = "Export Play"
    app.importButton.text = "Import Play"
    pressButtonUnderCursor(app, mx, my)
    if app.isMainMenu:
        handleMainMenuClick(app, mx, my)
    elif app.isField:
        handleFieldClick(app, mx, my)
    elif app.isOffensiveMenu:
        handleMenuClick(app, mx, my)

def pressButtonUnderCursor(app, mx, my):
    for button in visibleButtons(app):
        if button.enabled and button.contains(mx, my):
            button.pressed = True
            app.pressedButton = button
            return

def releasePressedButton(app):
    if app.pressedButton is not None:
        app.pressedButton.pressed = False
        app.pressedButton = None

def handleMainMenuClick(app, mx, my):
    if inStartButton(app, mx, my):
        app.isMainMenuLabelHovering = False
        app.isMainMenu = False
        app.isOffensiveMenu = True

def handleFieldClick(app, mx, my):
    if app.coverageButton.isClicked(mx, my):
        toggleCoverage(app)
        return
    checkFieldButtons(app, mx, my)
    if app.statsButton.isClicked(mx, my) and (app.playResult != '' or app.isPaused):
        app.statsButton.isStats = not app.statsButton.isStats
        return
    if clickedStatsClose(app, mx, my):
        app.statsButton.isStats = False
        return
    if (app.fieldInstructionsButton.isClicked(mx, my)
            and (app.playResult != '' or app.isPaused)):
        app.fieldInstructionsButton.isInstructions = not app.fieldInstructionsButton.isInstructions
        return
    if (app.playIsActive and app.ball.carrier == app.oFormation['QB']
            and app.playResult == ''):
        startThrow(app, mx, my)
    if clickedInstructionClose(app, mx, my, app.fieldInstructionsButton):
        app.fieldInstructionsButton.isInstructions = not app.fieldInstructionsButton.isInstructions
        return

def toggleCoverage(app):
    if app.playIsActive and app.playResult == '' and not app.isPaused:
        return
    app.coverageShell = 'Cover 2' if app.coverageShell == 'Cover 1' else 'Cover 1'
    app.coverageButton.text = f"Coverage: {'C2' if app.coverageShell == 'Cover 2' else 'C1'}"
    app.dFormation = initializeDefense(app)
    app.statsButton.isStats = False
    app.fieldInstructionsButton.isInstructions = False

def startThrow(app, mx, my):
    app.ballVelocity = 1
    app.qbRun = False
    app.throwing = True
    app.mouseX = mx
    app.mouseY = my

def handleMenuClick(app, mx, my):
    if clickedInstructionClose(app, mx, my, app.menuInstructionsButton):
        app.menuInstructionsButton.isInstructions = not app.menuInstructionsButton.isInstructions
        return
    if app.importButton.isClicked(mx, my):
        importData(app)
    elif app.exportButton.isClicked(mx, my):
        exportData(app, isField=False)
    if handleFormationButtons(app, mx, my):
        return
    if handleRouteButtons(app, mx, my):
        return
    selectSkillPlayer(app, mx, my)
    if app.startGameButton.isClicked(mx, my):
        startGame(app)

def handleFormationButtons(app, mx, my):
    for button in app.offensiveFormationButtons:
        if button.isClicked(mx, my):
            app.oFormation = button.formation
            app.selectedPlayer = None
            return True
    return False

def handleRouteButtons(app, mx, my):
    buttons = (app.offensiveWRRouteButtons if app.isWRMenu
               else app.offensiveRBRouteButtons)
    for button in buttons:
        if button.isClicked(mx, my):
            if app.selectedPlayer is None:
                return True
            player = app.oFormation[app.selectedPlayer]
            route = button.leftRoute if player.cx <= app.width // 2 else button.rightRoute
            player.route = player.translateRoute(app, route)
            player.routeName = button.text
            return True
    return False

def selectSkillPlayer(app, mx, my):
    for position in app.oFormation:
        player = app.oFormation[position]
        if distance(player.cx, player.cy, mx, my) > PLAYER_DRAW_RADIUS:
            continue
        if 'WR' in position or 'TE' in position:
            toggleSelection(app, position, wrMenu=True)
        elif 'RB' in position:
            toggleSelection(app, position, wrMenu=False)

def toggleSelection(app, position, wrMenu):
    if app.selectedPlayer == position:
        app.selectedPlayer = None
    else:
        app.selectedPlayer = position
        app.isWRMenu = wrMenu

def startGame(app):
    app.isField = True
    app.isOffensiveMenu = False
    app.selectedPlayer = None
    app.coverageButton.text = f"Coverage: {'C2' if app.coverageShell == 'Cover 2' else 'C1'}"
    app.dFormation = initializeDefense(app)
    app.isPlayActive = False

def inStartButton(app, mx, my):
    return ((app.width // 2) - 250 <= mx <= (app.width // 2) + 250 and
            (app.height // 2 + 45) - 75 <= my <= (app.height // 2 + 45) + 75)

def clickedInstructionClose(app, mx, my, button):
    closeCx, closeCy = panelCloseCenter(app.width // 2,
                                        app.height // 2 - INSTR_PANEL_OFFSET_Y,
                                        INSTR_PANEL_WIDTH, INSTR_PANEL_HEIGHT)
    inClose = panelCloseContains(mx, my, closeCx, closeCy)
    return button.isClicked(mx, my) or (button.isInstructions and inClose)

def clickedStatsClose(app, mx, my):
    if not app.statsButton.isStats:
        return False
    closeCx, closeCy = panelCloseCenter(app.width // 2,
                                        app.height // 2 + STATS_PANEL_OFFSET_Y,
                                        STATS_PANEL_WIDTH, STATS_PANEL_HEIGHT)
    return panelCloseContains(mx, my, closeCx, closeCy)

def onMouseDrag(app, mouseX, mouseY):
    if (app.isOffensiveMenu and app.selectedPlayer is not None and
            app.sideLineOffset + BOUNDARY_OFFSET <= mouseX
            <= app.width - app.sideLineOffset - BOUNDARY_OFFSET):
        player = app.oFormation[app.selectedPlayer]
        player.route += [(mouseX, mouseY)]
        player.routeName = None
        if player.clickInPlayer(mouseX, mouseY):
            player.route = [(player.startX, player.startY), (mouseX, mouseY)]
    if app.isField and app.throwing:
        app.mouseX = mouseX
        app.mouseY = mouseY

def onMouseRelease(app, mouseX, mouseY):
    releasePressedButton(app)
    if app.throwing and app.oFormation['QB'].cy >= app.lineOfScrimmage:
        app.throwing = False
        app.ball.throwToTarget(mouseX, mouseY, app)

########################
### Keyboard Helpers ###
########################

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

def checkFieldButtons(app, mx, my):
    if (app.exportButton.text == "Export Play" and
            app.exportButton.isClicked(mx, my)):
        exportData(app)
    for button in app.fieldButtons:
        if button.isClicked(mx, my):
            if button.text == 'Reset':
                app.isPlayActive = False
                app.statsButton.isStats = False
                app.fieldInstructionsButton.isInstructions = False
                resetApp(app)
                return
            else:
                app.importButton.text = "Import Play"
                app.isPlayActive = False
                app.menuInstructionsButton.isInstructions = False
                resetApp(app)
                app.isField = False
                app.isOffensiveMenu = True
                return

##################
### Step Logic ###
##################

def onStep(app):
    app.animationTicks += 1
    if app.isPaused:
        return
    elif app.isField:
        takeStep(app)

def takeStep(app):
    app.steps += 1
    app.playIsActive = True
    if app.throwing:
        app.ballVelocity += 0.3
        if app.ballVelocity >= app.maxBallVelo:
            app.ballVelocity = app.maxBallVelo
    app.yardsRan = (app.velocity * app.steps) / app.yardStep
    if app.playResult == '':
        moveDefense(app)
        moveOffense(app)
        handleCollisions(app)
    else:
        app.throwing = False
    app.ball.updateBallPosition(app)
