
from importExport import importData, exportData
from cmu_graphics import *
from classes import *
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
            app.isPlayActive = not app.isPlayActive
            if app.isPlayActive:
                app.fieldInstructionsButton.isInstructions = False
    elif key == 'r':
        resetApp(app)
    elif key == 'p':
        app.isPashRush = not app.isPashRush

def onKeyHold(app, keys):
    if app.isField:
        if 'up' in keys and app.ball.carrier != None:
            carrier = app.ball.carrier
            carrier.targetY = carrier.cy-10*app.yardStep
        if 'down' in keys and app.ball.carrier != None:
            carrier = app.ball.carrier
            carrier.targetY = carrier.cy+10*app.yardStep
        if 'right' in keys and app.ball.carrier != None:
            carrier = app.ball.carrier
            carrier.targetX = carrier.cx+10*app.yardStep
        if 'left' in keys and app.ball.carrier != None:
            carrier = app.ball.carrier
            carrier.targetX = carrier.cx-10*app.yardStep
    elif app.isOffensiveMenu:
        if app.selectedPlayer == None:
            return
        speed = 0.11
        moveAmount = speed * app.yardStep
        player = app.oFormation[app.selectedPlayer]
        if 'up' in keys:
            player.startY -= moveAmount
            player.cy = player.startY
            if checkInBoundaryScrimmageLine(app, player, moveAmount) != None:
                return
            newRoute = []
            for (x,y) in player.route:
                newRoute.append((x, y - moveAmount))
            player.route = newRoute
        if 'down' in keys:
            player.startY += moveAmount
            player.cy = player.startY
            if checkInBoundaryScrimmageLine(app, player, moveAmount) != None:
                return
            newRoute = []
            for (x,y) in player.route:
                newRoute.append((x, y + moveAmount))
            player.route = newRoute
        if 'right' in keys:
            player.startX += moveAmount
            player.cx = player.startX
            if checkInBoundaryLR(app, player, moveAmount) != None:
                return
            newRoute = []
            for (x,y) in player.route:
                newRoute.append((x + moveAmount, y))
            player.route = newRoute
        if 'left' in keys:
            player.startX -= moveAmount
            player.cx = player.startX
            if checkInBoundaryLR(app, player, moveAmount) != None:
                return
            newRoute = []
            for (x,y) in player.route:
                newRoute.append((x - moveAmount, y))
            player.route = newRoute
        makeRouteInBounds(app, player)

def onKeyRelease(app, key):
    if key == 'up' and app.ball.carrier != None:
        app.ball.carrier.targetY = app.ball.carrier.cy
    elif key == 'down' and app.ball.carrier != None:
        app.ball.carrier.targetY = app.ball.carrier.cy
    elif key == 'left' and app.ball.carrier != None:
        app.ball.carrier.targetX = app.ball.carrier.cx
    elif key == 'right' and app.ball.carrier != None:
        app.ball.carrier.targetX = app.ball.carrier.cx

def onMouseMove(app, mx, my):
    if app.isMainMenu:
        #main button check
        if ((app.width//2)-250<=mx<=(app.width//2)+250 and 
            (app.height//2+45)-75<=my<=(app.height//2+45)+75):
            app.isMainMenuLabelHovering = True
        else: app.isMainMenuLabelHovering = False
    elif app.isOffensiveMenu:
        app.importButton.checkBold(mx, my)
        app.exportButton.checkBold(mx, my)
        for button in app.offensiveFormationButtons:
            button.checkBold(mx, my)
        app.menuInstructionsButton.checkBold(mx, my)
        if app.isWRMenu:
            for button in app.offensiveWRRouteButtons:
                button.checkBold(mx, my)
        else:
            for button in app.offensiveRBRouteButtons:
                button.checkBold(mx, my)
        app.startGameButton.checkBold(mx, my)
    elif app.isField:
        for button in app.fieldButtons:
            button.checkBold(mx, my)
        app.coverageButton.checkBold(mx, my)
        if app.exportButton.text == "Export Play":
            app.exportButton.checkBold(mx, my)
        app.fieldInstructionsButton.checkBold(mx, my)
        app.statsButton.checkBold(mx, my)

def onMousePress(app, mx, my):
    app.exportButton.text = "Export Play"
    app.importButton.text = "Import Play"
    if app.isMainMenu:
        if ((app.width//2)-250<=mx<=(app.width//2)+250 and 
            (app.height//2+45)-75<=my<=(app.height//2+45)+75):
            app.isMainMenuLabelHovering = False
            app.isMainMenu = False
            app.isOffensiveMenu = True
    elif app.isField:
        if app.coverageButton.isClicked(mx, my):
            if app.playIsActive and app.playResult == '' and not app.isPaused:
                return
            app.coverageShell = 'Cover 2' if app.coverageShell == 'Cover 1' else 'Cover 1'
            app.coverageButton.text = f"Coverage: {'C2 (beta)' if app.coverageShell == 'Cover 2' else 'C1'}"
            app.dFormation = initializeDefense(app)
            app.statsButton.isStats = False
            app.fieldInstructionsButton.isInstructions = False
            return
        checkFieldButtons(app, mx, my)
        if app.statsButton.isClicked(mx, my) and (app.playResult != '' or app.isPaused):
            app.statsButton.isStats = not app.statsButton.isStats
            return
        if app.fieldInstructionsButton.isClicked(mx, my) and (app.playResult != '' or app.isPaused):
            app.fieldInstructionsButton.isInstructions = not app.fieldInstructionsButton.isInstructions
            return
        if (app.playIsActive and app.ball.carrier == app.oFormation['QB'] 
            and app.playResult == ''):
            app.ballVelocity = 1
            app.qbRun = False
            app.throwing = True
            app.mouseX = mx
            app.mouseY = my
        offset = 175
        halfXButtonWidthHeight = 10
        closingRectCX = app.width//2 + 220
        closingRectCY = app.height//2 - offset*1.85
        if(app.fieldInstructionsButton.isClicked(mx, my) or 
           (app.fieldInstructionsButton.isInstructions and 
           closingRectCX - halfXButtonWidthHeight <= mx <= closingRectCX + halfXButtonWidthHeight and
            closingRectCY - halfXButtonWidthHeight <= my <= closingRectCY + halfXButtonWidthHeight)):
            app.fieldInstructionsButton.isInstructions = not app.fieldInstructionsButton.isInstructions
            return
    elif app.isOffensiveMenu:
        offset = 175
        halfXButtonWidthHeight = 10
        closingRectCX = app.width//2 + 220
        closingRectCY = app.height//2 - offset*1.85
        if(app.menuInstructionsButton.isClicked(mx, my) or 
           (app.menuInstructionsButton.isInstructions and 
           closingRectCX - halfXButtonWidthHeight <= mx <= closingRectCX + halfXButtonWidthHeight and
            closingRectCY - halfXButtonWidthHeight <= my <= closingRectCY + halfXButtonWidthHeight)):
            app.menuInstructionsButton.isInstructions = not app.menuInstructionsButton.isInstructions
            return
        elif app.importButton.isClicked(mx, my):
            importData(app)
        elif app.exportButton.isClicked(mx, my):
            exportData(app, isField = False)
        for button in app.offensiveFormationButtons:
            if button.isClicked(mx, my):
                app.oFormation = button.formation
                app.selectedPlayer = None
                return
        if app.isWRMenu:
            for button in app.offensiveWRRouteButtons:
                if button.isClicked(mx, my):
                    if app.selectedPlayer==None: return
                    player = app.oFormation[app.selectedPlayer]
                    if player.cx<=app.width//2:
                        player.route = player.translateRoute(app, button.leftRoute)
                    else:
                        player.route = player.translateRoute(app, button.rightRoute)
                    return
        else:
            for button in app.offensiveRBRouteButtons:
                if button.isClicked(mx, my):
                    if app.selectedPlayer==None: return
                    player = app.oFormation[app.selectedPlayer]
                    if player.cx<=app.width//2:
                        player.route = player.translateRoute(app, button.leftRoute)
                    else:
                        player.route = player.translateRoute(app, button.rightRoute)
                    return
        for position in app.oFormation:
            if 'WR' in position or "TE" in position:
                player = app.oFormation[position]
                if distance(player.cx, player.cy, mx, my) <= 13:
                    if app.selectedPlayer == position:
                        app.selectedPlayer = None
                    else:
                        app.selectedPlayer = position
                        app.isWRMenu = True
            elif "RB" in position:
                player = app.oFormation[position]
                if distance(player.cx, player.cy, mx, my) <= 13:
                    if app.selectedPlayer == position:
                        app.selectedPlayer = None
                    else:
                        app.selectedPlayer = position
                        app.isWRMenu = False
        if app.startGameButton.isClicked(mx, my):
            app.isField = True
            app.isOffensiveMenu = False
            app.selectedPlayer = None
            app.coverageButton.text = f"Coverage: {'C2' if app.coverageShell == 'Cover 2' else 'C1'}"
            app.dFormation = initializeDefense(app)
            app.isPlayActive = False

def onMouseDrag(app, mouseX, mouseY):
    boundaryOffset = 20
    if (app.isOffensiveMenu and app.selectedPlayer != None and
       (mouseX >= app.sideLineOffset+boundaryOffset 
       and mouseX <= app.width - app.sideLineOffset-boundaryOffset)):
        player = app.oFormation[app.selectedPlayer]
        player.route += [(mouseX, mouseY)]
        if player.clickInPlayer(mouseX,mouseY):
            startX = player.startX
            startY = player.startY
            player.route = [(startX, startY),(mouseX, mouseY)]
    if app.isField and app.throwing:
        app.mouseX = mouseX
        app.mouseY = mouseY

def onMouseRelease(app, mouseX, mouseY):
    if app.throwing and app.oFormation['QB'].cy >= app.lineOfScrimmage:
        app.throwing = False
        app.ball.throwToTarget(mouseX, mouseY, app)

########################
### Keyboard Helpers ###
########################

def checkInBoundaryLR(app, player, moveAmount):
    boundaryOffset = 20
    if player.cx <= boundaryOffset+app.sideLineOffset:
        player.startX += moveAmount
        player.cx = player.startX
        return "Too Far Left"
    elif player.cx >= app.width-boundaryOffset-app.sideLineOffset:
        player.startX -= moveAmount
        player.cx = player.startX
        print('too far right')
        return "Too Far Right"
    return None

def checkInBoundaryScrimmageLine(app, player, moveAmount):
    scrimmageLineOffset = 13
    lowerScreenOffset = 15
    if player.cy <= app.lineOfScrimmage+scrimmageLineOffset:
        player.startY += moveAmount
        player.cy = player.startY
        return "Too Far Up"
    elif player.cy >= app.height-lowerScreenOffset:
        player.startY -= moveAmount
        player.cy = player.startY
        return "Too Far Down"
    return None

def makeRouteInBounds(app, player):
    newRoute = copy.deepcopy(player.route)
    scrimmageLineOffset = 20
    for i in range(len(player.route)):
        x, y = player.route[i]
        if x <= app.sideLineOffset + scrimmageLineOffset:
            newRoute[i] = (app.sideLineOffset + scrimmageLineOffset, y)
        if x >= app.width - app.sideLineOffset - scrimmageLineOffset:
            newRoute[i] = (app.width - app.sideLineOffset - scrimmageLineOffset, y)
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
    if app.isPaused:
        return
    elif app.isField:
        takeStep(app)

def takeStep(app):
    app.steps+=1
    app.playIsActive = True
    if app.throwing:
        app.ballVelocity += 0.3
        if app.ballVelocity >= app.maxBallVelo:
            app.ballVelocity = app.maxBallVelo
    app.yardsRan = (app.velocity * app.steps)/app.yardStep
    if app.playResult == '':
        moveDefense(app)
        moveOffense(app)
        handleCollisions(app)
    else: 
        app.throwing = False
    app.ball.updateBallPosition(app)
