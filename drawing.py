from cmu_graphics import *
from classes import *

def redrawAll(app):
    if app.isField:
        drawField(app)
        drawSideline(app)
        drawFieldButtons(app)
        app.coverageButton.draw()
        drawOffense(app)
        drawDefense(app)
        app.exportButton.draw()
        app.ball.drawBall(app)
        if app.throwing and app.oFormation['QB'].cy > app.lineOfScrimmage:
            opactiyScale = 100/app.maxBallVelo
            circleScale = 2.5
            drawCircle(app.mouseX, app.mouseY, app.ballVelocity*circleScale, 
                        fill=rgb(0,255,0), opacity=app.ballVelocity*opactiyScale)
        app.fieldInstructionsButton.draw()
        app.statsButton.draw()
        if (app.fieldInstructionsButton.isInstructions 
            and (app.playResult != '' or app.isPaused)):
            drawFieldInstructions(app)
        if app.statsButton.isStats and (app.playResult != "" or app.isPaused):
            drawStatsMenu(app)
    elif app.isMainMenu:
        drawMainMenu(app)
    elif app.isOffensiveMenu:
        drawOffensiveMenu(app)

def drawStatsMenu(app):
    offset = 200
    drawRect(app.width//2, app.height//2+offset, 500, 270, 
                fill=rgb(60, 100, 60), border='black', 
                opacity = 93,align='center')

    drawLabel("Stats:", app.width//2, app.height//2+offset - 100, 
                size=45, bold=True)
    
    drawLabel("Total Yards Gained: " + str(app.totalYards), 
                app.width//2-200, app.height//2+offset - 50, 
                size=18, bold=True, align='left')

    drawLabel("Completions: " + str(app.numCompletions) + " / " + 
                str(app.attempts), 
                app.width//2-200, app.height//2+offset - 25, 
                size=18, bold=True, align='left')

    drawLabel("Interceptions: " + str(app.ints),
                app.width//2-200, app.height//2+offset, 
                size=18, bold=True, align='left')
    if app.lastPlayResult != "":
        drawLabel(f"Last Play Result: {app.lastPlayResult}",
                app.width//2-200, app.height//2+offset + 25, 
                size=18, bold=True, align='left')
        if app.lastPlayResult != 'Intercepted':
            drawLabel(f"Yards on Last Play: {app.lastYardsRan}",
                    app.width//2-200, app.height//2+offset + 50, 
                    size=18, bold=True, align='left')
        else:
            drawLabel(f"Yards on Last Play: N/A",
                    app.width//2-200, app.height//2+offset + 50, 
                    size=18, bold=True, align='left')

def drawDefense(app):
    offset = 0
    if app.ball.cy <= 10*app.yardStep:
        offset = 10*app.yardStep - app.ball.cy
    for position in app.dFormation:
        player = app.dFormation[position]
        cy = player.cy + offset
        if cy<0 or cy > app.height:
            continue
        drawCircle(player.cx, cy, 13,
                    fill='white', border='black')
        # Debugging Display
        # if hasattr(player, 'callout') and player.callout != '':
            # drawLabel(player.callout, player.cx, cy - 16, size=9, fill='black')

def drawOffense(app):
    offset = 0
    customComplimentRed = rgb(215, 80, 75)
    deepRed = rgb(180, 30, 50)
    if app.ball.cy <= 10*app.yardStep:
        offset = 10*app.yardStep - app.ball.cy
    for position in app.oFormation:
        player = app.oFormation[position]
        color = customComplimentRed
        if app.selectedPlayer == position and app.isOffensiveMenu:
            color = deepRed
        cy = player.cy + offset
        if cy<0 or cy > app.height:
            continue
        drawCircle(player.cx, cy, 13,
                    fill=color, border='black')
        # velo = (player.dx**2 + player.dy**2)**0.5
        # drawLabel(f"{(velo)}", player.cx, player.cy, size=10)
        if isinstance(player, SkillPlayer):
            #player.drawVelocity(app)
            if not app.playIsActive:
                player.drawRoute(app)


def drawSideline(app):
    customComplimentRed = rgb(215, 80, 75)
    drawCircle(app.sideLineOffset - 10, app.lineOfScrimmage-50, 13,
                    fill=customComplimentRed, border='black')
    drawCircle(app.sideLineOffset - 20, app.lineOfScrimmage -25, 13,
                    fill=customComplimentRed, border='black')
    drawCircle(app.sideLineOffset - 20, app.lineOfScrimmage - 75, 13,
                    fill=customComplimentRed, border='black')
    drawCircle(app.sideLineOffset - 25, app.lineOfScrimmage - 100, 13,
                    fill=customComplimentRed, border='black')
    drawCircle(app.sideLineOffset - 25, app.lineOfScrimmage - 125, 13,
                    fill=customComplimentRed, border='black')
    
    drawCircle(42, 170, 13, fill=customComplimentRed, border='black')
    drawCircle(41, 196, 13, fill=customComplimentRed, border='black')
    drawCircle(40, 225, 13, fill=customComplimentRed, border='black')
    drawCircle(46, 258, 13, fill=customComplimentRed, border='black')
    drawCircle(45, 283, 13, fill=customComplimentRed, border='black')

    drawCircle(43, 355, 13, fill=customComplimentRed, border='black')
    drawCircle(47, 381, 13, fill=customComplimentRed, border='black')
    drawCircle(46, 419, 13, fill=customComplimentRed, border='black')

    drawCircle(42, 555, 13, fill=customComplimentRed, border='black')
    drawCircle(44, 583, 13, fill=customComplimentRed, border='black')
    drawCircle(40, 615, 13, fill=customComplimentRed, border='black')
    drawCircle(42, 642, 13, fill=customComplimentRed, border='black')

    drawCircle(app.width - app.sideLineOffset + 4, 
                    app.lineOfScrimmage + 8, 13, fill='white', border='black')
    drawCircle(app.width - app.sideLineOffset + 20, 
                    app.lineOfScrimmage + 30, 13, fill='white', border='black')
    drawCircle(app.width - app.sideLineOffset + 20, 
                    app.lineOfScrimmage - 21, 13, fill='white', border='black')
    drawCircle(app.width - app.sideLineOffset + 20, 
                    app.lineOfScrimmage - 50, 13, fill='white', border='black')
    drawCircle(app.width - app.sideLineOffset + 20, 
                    app.lineOfScrimmage - 75, 13, fill='white', border='black')

    drawCircle(app.width-42, 175, 13, fill='white', border='black')
    drawCircle(app.width-45, 202, 13, fill='white', border='black')
    drawCircle(app.width-41, 229, 13, fill='white', border='black')

    drawCircle(app.width-48, 300, 13, fill='white', border='black')
    drawCircle(app.width-43, 331, 13, fill='white', border='black')
    drawCircle(app.width-46, 370, 13, fill='white', border='black')
    drawCircle(app.width-41, 405, 13, fill='white', border='black')

    drawCircle(app.width-41, 470, 13, fill='white', border='black')
    drawCircle(app.width-41, 504, 13, fill='white', border='black')
    drawCircle(app.width-45, 542, 13, fill='white', border='black')

    drawCircle(app.width-40, 642, 13, fill='white', border='black')
    drawCircle(app.width-49, 675, 13, fill='white', border='black')
    drawCircle(app.width-42, 702, 13, fill='white', border='black')

def drawFieldInstructions(app):
    offset = 175
    drawRect(app.width//2, app.height//2-offset, 500, 350, 
                fill=rgb(60, 100, 60), border='black', 
                opacity = 88,align='center')
    drawLabel("Instructions:", app.width//2, app.height//2 - offset - 130, 
                size=45, bold=True)

    drawLabel("- Press the spacebar to pause/resume", 
                app.width//2-200, app.height//2 - offset - 70, 
                size=18, bold=True, align='left')

    drawLabel("- Click and hold to throw the ball", 
                app.width//2-200, app.height//2 - offset - 40, 
                size=18, bold=True, align='left')

    drawLabel("Hold longer for a faster throw", 
                app.width//2-150, app.height//2 - offset - 15, 
                size=18, bold=True, align='left')
    
    drawLabel("- Use arrow keys to move ball carrier",
                app.width//2-200, app.height//2 - offset + 15, 
                size=18, bold=True, align='left')

    drawLabel("- Press 'S' to step by one frame when paused", 
                app.width//2-200, app.height//2 - offset + 45, 
                size=18, bold=True, align='left')

    drawLabel("- Press 'R' to reset the play", 
                app.width//2-200, app.height//2 - offset + 75, 
                size=18, bold=True, align='left')

    drawLabel("- Press 'P' to toggle pash rushers", 
                app.width//2-200, app.height//2 - offset + 105, 
                size=18, bold=True, align='left')

    closingRectCX = app.width//2 + 220
    closingRectCY = app.height//2 - offset*1.85

    drawRect(closingRectCX, closingRectCY, 20, 20, fill=rgb(60, 60, 60), border=rgb(40, 40, 40), 
                borderWidth=3, align='center', opacity=50)
    
    drawLine((closingRectCX-10), (closingRectCY-10), (closingRectCX+10), (closingRectCY+10), 
                fill=rgb(40, 40, 40), lineWidth=2, opacity=70)
    drawLine((closingRectCX-10), (closingRectCY+10), (closingRectCX+10), (closingRectCY-10), 
                fill=rgb(40, 40, 40), lineWidth=2, opacity=70)

def drawMainMenu(app):
    customGreen = rgb(27, 150, 85)
    customGreen1 = rgb(19, 130, 60)
    customGreen2 = rgb(10, 110, 30)
    customComplimentRed = rgb(215, 80, 75)
    customComplimentRed1 = rgb(190, 90, 70)
    drawRect(0, 0, app.width, app.height, fill=gradient(customGreen, 
                        customGreen1, customGreen2, start='left-top'))
    drawLine(-6, 60, 200, app.height+6, 
                fill=customComplimentRed, lineWidth = 6)
    drawLine(50, -6, 50, app.height+6, 
                fill=customComplimentRed1, lineWidth = 6)
    drawImage( "routeLabLogo.png", app.width//2, 150, align='center',
                width=750, height=300)
    drawLabel("Create your own football", app.width//2, 
                270, size=35, bold=True,font='monospace')
    drawLabel("routes and dominate the game.", app.width//2, 
                310, size=35,bold=True, font='monospace')
    if app.isMainMenuLabelHovering: 
        drawRect(app.width//2, app.height//2+45, 
                    510, 156, fill=customComplimentRed, 
                    border=customComplimentRed, borderWidth=3, align='center')
        bolded = True
        drawRect(app.width//2, app.height//2+45, 
                    500, 150, fill=customGreen1,  
                    border='black', borderWidth=3, align='center')
        drawLabel("Start Creating Plays ", app.width//2, 
                    app.height//2+45, size=35, 
                    bold=bolded, font='monospace')
    else: 
        drawRect(app.width//2, app.height//2+45, 
                    506, 153, fill=customComplimentRed, 
                    border=customComplimentRed, borderWidth=3, 
                    align='center')
        bolded = False
        drawRect(app.width//2, app.height//2+45, 500, 150, fill=customGreen1,  
                    border='black', borderWidth=3, align='center')
        drawLabel("Start Creating Plays ", app.width//2, 
                    app.height//2+45, size=33, 
                    bold=bolded, font='monospace')

    drawLine(270, app.height-60, 270, app.height-225, 
                lineWidth=7, arrowEnd=True)
    drawCircle(270, app.height-60, 18,
                    fill=customComplimentRed, border='black')

    drawLine(340, app.height-60, 340, app.height-130, lineWidth=7)
    drawLine(340, app.height-130, 450, app.height-130, 
                                        lineWidth=7, arrowEnd=True)
    drawRect(340, app.height-130, 7, 7, fill='black', align='center')
    drawCircle(340, app.height-60, 18,
                    fill=customComplimentRed, border='black')
    drawLine(app.width-190, app.height-60, app.width-190, 
                app.height-150, lineWidth=7)
    drawLine(app.width-190, app.height-150, app.width-270, 
                app.height-220, lineWidth=7, arrowEnd=True)
    drawRect(app.width-190, app.height-150, 
                7, 7, fill='black', align='center')
    drawCircle(app.width-190, app.height-60, 18,
                    fill=customComplimentRed, border='black')

def drawFieldButtons(app):
    for button in app.fieldButtons:
        button.draw()

def drawOffensiveMenu(app):
    drawField(app, scrimmageLine=False)
    drawLabel("Select Formation", app.sideLineOffset//2, 
                17, size=20, bold=True)
    drawLabel("Select Route", app.width - app.sideLineOffset//2, 
                17, size=20, bold=True)

    for button in app.offensiveFormationButtons:
        button.draw()
    if app.isWRMenu:
        for button in app.offensiveWRRouteButtons:
            button.draw()
    else:
        for button in app.offensiveRBRouteButtons:
            button.draw()
    app.startGameButton.draw()
    app.importButton.draw()
    app.exportButton.draw()
    app.menuInstructionsButton.draw()
    drawOffense(app)
    if app.menuInstructionsButton.isInstructions:
        drawMenuInstructionsMenu(app)

def drawMenuInstructionsMenu(app):
    offset = 175
    drawRect(app.width//2, app.height//2-offset, 500, 350, 
                fill=rgb(60, 100, 60), border='black', 
                opacity = 88,align='center')
    drawLabel("Instructions:", app.width//2, app.height//2 - offset - 130, 
                size=45, bold=True)

    drawLabel("- Click a formation button to select formation", 
                app.width//2-200, app.height//2 - offset - 70, 
                size=18, bold=True, align='left')

    drawLabel("- Click a player then a route to select route", 
                app.width//2-200, app.height//2 - offset - 40, 
                size=18, bold=True, align='left')
    
    drawLabel("- Use arrow keys to move selected players", 
                app.width//2-200, app.height//2 - offset - 10, 
                size=18, bold=True, align='left')

    drawLabel("- Click a player and drag to create custom route", 
                app.width//2-200, app.height//2 - offset + 20, 
                size=18, bold=True, align='left')

    drawLabel("- Only import plays with exported file structure", 
                app.width//2-200, app.height//2 - offset + 50, 
                size=18, bold=True, align='left')
    drawLabel("to avoid failed imports", 
                app.width//2-150, app.height//2 - offset + 75, 
                size=18, bold=True, align='left')

    closingRectCX = app.width//2 + 220
    closingRectCY = app.height//2 - offset*1.85

    drawRect(closingRectCX, closingRectCY, 20, 20, fill=rgb(60, 60, 60), border=rgb(40, 40, 40), 
                borderWidth=3, align='center', opacity=50)
    
    drawLine((closingRectCX-10), (closingRectCY-10), (closingRectCX+10), (closingRectCY+10), 
                fill=rgb(40, 40, 40), lineWidth=2, opacity=70)
    drawLine((closingRectCX-10), (closingRectCY+10), (closingRectCX+10), (closingRectCY-10), 
                fill=rgb(40, 40, 40), lineWidth=2, opacity=70)

def drawField(app, scrimmageLine=True):
    customGreen = rgb(27, 150, 85)
    drawRect(0, 0, app.width, app.height, fill=customGreen)
    tenCount=1
    fiveCount=0
    #Draw Yard Lines
    for i in range(app.height, 0, -app.yardStep):
        fiveCount+=1
        if fiveCount%5==0:
            drawLine(30+app.sideLineOffset, i, 
                        app.width-30-app.sideLineOffset, i, fill='white')
            if fiveCount%10==0:
                drawLabel(f'{tenCount} 0', 60+app.sideLineOffset, i,
                        size=20, fill='white', rotateAngle=90)
                drawLabel(f'{tenCount} 0', app.width-60-app.sideLineOffset, i,
                        size=20, fill='white', rotateAngle=270)
                tenCount+=1
        else:
            drawLine(30+app.sideLineOffset, i, 
                        40+app.sideLineOffset, i, fill='white')
            drawLine(app.width-30-app.sideLineOffset, i, 
                        app.width-40-app.sideLineOffset, i, fill='white')
            drawLine(3*app.width//7, i, 3*app.width//7+10, i, fill='white')
            drawLine(4*app.width//7, i, 4*app.width//7+10, i, fill='white')
    boundaryOffset = 20
    if scrimmageLine and not app.isPlayActive:
        drawLine(boundaryOffset+app.sideLineOffset, 
                    app.height-(app.yardStep*14), 
                    app.width-boundaryOffset-app.sideLineOffset,
                    app.height-(app.yardStep*14), fill='blue')

    drawLine(app.sideLineOffset+boundaryOffset, 0, app.sideLineOffset+boundaryOffset, app.height,
                fill='white', lineWidth=4)
    drawLine(app.width-boundaryOffset-app.sideLineOffset, 0, 
                app.width-boundaryOffset-app.sideLineOffset, app.height,
                fill='white', lineWidth=4)
