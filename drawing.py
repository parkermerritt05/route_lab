from cmu_graphics import *
from classes import *
from constants import *
import math

def redrawAll(app):
    if app.isField:
        drawFieldScreen(app)
    elif app.isMainMenu:
        drawMainMenu(app)
    elif app.isOffensiveMenu:
        drawOffensiveMenu(app)

def drawFieldScreen(app):
    updateFieldButtonStates(app)
    drawField(app)
    drawSideline(app)
    drawFieldButtons(app)
    app.coverageButton.draw()
    drawCoverageBetaTag(app)
    drawOffense(app)
    drawDefense(app)
    app.exportButton.draw()
    app.ball.drawBall(app)
    drawThrowIndicator(app)
    drawThrowPowerBar(app)
    app.fieldInstructionsButton.draw()
    app.statsButton.draw()
    drawFieldHud(app)
    if fieldInstructionsOpen(app):
        drawFieldInstructions(app)
    if fieldStatsOpen(app):
        drawStatsMenu(app)

def controlsAreLive(app):
    # The field is "settled" (safe to open panels or flip coverage) whenever a
    # play has finished or the sim is paused.
    return app.playResult != '' or app.isPaused

def fieldInstructionsOpen(app):
    return app.fieldInstructionsButton.isInstructions and controlsAreLive(app)

def fieldStatsOpen(app):
    return app.statsButton.isStats and controlsAreLive(app)

def drawCoverageBetaTag(app):
    if app.coverageShell != 'Cover 2':
        return
    button = app.coverageButton
    tagY = button.cy + button.h // 2 + COVERAGE_BETA_GAP
    drawLabel(COVERAGE_BETA_TEXT, button.cx, tagY, size=COVERAGE_BETA_SIZE,
              bold=True, italic=True, fill=COVERAGE_BETA_COLOR)

def updateFieldButtonStates(app):
    app.statsButton.enabled = controlsAreLive(app)
    app.fieldInstructionsButton.enabled = controlsAreLive(app)
    app.coverageButton.enabled = controlsAreLive(app)

def drawThrowIndicator(app):
    if not (app.throwing and app.oFormation['QB'].cy > app.lineOfScrimmage):
        return
    opacityScale = 100 / app.maxBallVelo
    circleScale = 2.5
    drawCircle(app.mouseX, app.mouseY, app.ballVelocity * circleScale,
               fill=rgb(0, 255, 0), opacity=app.ballVelocity * opacityScale)

def drawThrowPowerBar(app):
    if not (app.throwing and app.oFormation['QB'].cy > app.lineOfScrimmage):
        return
    fraction = min(app.ballVelocity / app.maxBallVelo, 1)
    centerX = app.width // 2
    trackY = app.height - POWER_BAR_BOTTOM_MARGIN
    trackLeft = centerX - POWER_BAR_WIDTH // 2
    drawRect(centerX, trackY, POWER_BAR_WIDTH, POWER_BAR_HEIGHT,
             fill=POWER_BAR_TRACK_COLOR, border='black', align='center', opacity=85)
    fillColor = (POWER_BAR_FILL_HIGH if fraction >= POWER_BAR_FULL_THRESHOLD
                 else POWER_BAR_FILL_LOW)
    drawRect(trackLeft, trackY, POWER_BAR_WIDTH * fraction, POWER_BAR_HEIGHT,
             fill=fillColor, align='left')
    drawLabel('POWER', centerX, trackY - POWER_BAR_HEIGHT, size=12, bold=True,
              fill=HUD_TEXT_COLOR)

def drawFieldHud(app):
    drawTopReadout(app)
    drawPauseHint(app)

def drawTopReadout(app):
    if app.playResult != '':
        drawResultBanner(app)
    elif app.playIsActive:
        drawLiveYards(app)

def drawResultBanner(app):
    gainedYards = app.playResult.startswith('Tackled')
    color = BANNER_GAIN_COLOR if gainedYards else BANNER_LOSS_COLOR
    centerX = app.width // 2
    drawRect(centerX, HUD_TOP_Y, RESULT_BANNER_WIDTH, RESULT_BANNER_HEIGHT,
             fill=color, border='black', borderWidth=2, align='center',
             opacity=RESULT_BANNER_OPACITY)
    if gainedYards:
        drawLabel(app.playResult, centerX, HUD_TOP_Y - 11, size=20, bold=True,
                  fill=HUD_TEXT_COLOR)
        drawLabel(f'{app.lastYardsRan:+d} yards', centerX, HUD_TOP_Y + 13,
                  size=15, bold=True, fill=HUD_TEXT_COLOR)
    else:
        drawLabel(app.playResult, centerX, HUD_TOP_Y, size=22, bold=True,
                  fill=HUD_TEXT_COLOR)

def drawLiveYards(app):
    carrier = app.ball.carrier
    if carrier is None or isinstance(carrier, Lineman) or app.ball.beingSnapped:
        return
    yards = int((app.lineOfScrimmage - carrier.cy) / app.yardStep)
    centerX = app.width // 2
    drawRect(centerX, HUD_TOP_Y, LIVE_YARDS_WIDTH, LIVE_YARDS_HEIGHT,
             fill=HUD_PANEL_COLOR, border='black', align='center',
             opacity=HUD_PANEL_OPACITY)
    drawLabel(f'{yards} yds', centerX, HUD_TOP_Y, size=20, bold=True,
              fill=HUD_TEXT_COLOR)

def drawPauseHint(app):
    if app.playResult != '' or not app.isPaused or anyFieldModalOpen(app):
        return
    text = 'Press SPACE to hike' if not app.playIsActive else 'Paused - SPACE to resume'
    centerX = app.width // 2
    hintY = app.height - HUD_BOTTOM_MARGIN
    drawRect(centerX, hintY, PAUSE_HINT_WIDTH, PAUSE_HINT_HEIGHT,
             fill=HUD_PANEL_COLOR, border='black', align='center',
             opacity=PAUSE_HINT_OPACITY)
    drawLabel(text, centerX, hintY, size=15, bold=True, fill=HUD_TEXT_COLOR)

def anyFieldModalOpen(app):
    return fieldInstructionsOpen(app) or fieldStatsOpen(app)

def cameraOffset(app):
    if app.ball.cy <= CAMERA_SCROLL_YARDS * app.yardStep:
        return CAMERA_SCROLL_YARDS * app.yardStep - app.ball.cy
    return 0

def drawModalBackdrop(app):
    drawRect(0, 0, app.width, app.height,
             fill=MODAL_BACKDROP_COLOR, opacity=MODAL_BACKDROP_OPACITY)

def drawPanelCloseButton(panelCx, panelCy, panelW, panelH):
    cx, cy = panelCloseCenter(panelCx, panelCy, panelW, panelH)
    half = PANEL_CLOSE_HALF
    drawRect(cx, cy, PANEL_CLOSE_BOX, PANEL_CLOSE_BOX, fill=PANEL_CLOSE_FILL,
             border=PANEL_CLOSE_LINE, borderWidth=3, align='center',
             opacity=PANEL_CLOSE_BOX_OPACITY)
    drawLine(cx - half, cy - half, cx + half, cy + half,
             fill=PANEL_CLOSE_LINE, lineWidth=2, opacity=PANEL_CLOSE_LINE_OPACITY)
    drawLine(cx - half, cy + half, cx + half, cy - half,
             fill=PANEL_CLOSE_LINE, lineWidth=2, opacity=PANEL_CLOSE_LINE_OPACITY)

def drawStatsMenu(app):
    drawModalBackdrop(app)
    centerX = app.width // 2
    baseY = app.height // 2 + STATS_PANEL_OFFSET_Y
    drawRect(centerX, baseY, STATS_PANEL_WIDTH, STATS_PANEL_HEIGHT,
             fill=rgb(60, 100, 60), border='black', opacity=93, align='center')
    drawPanelCloseButton(centerX, baseY, STATS_PANEL_WIDTH, STATS_PANEL_HEIGHT)
    drawLabel("Stats:", centerX, baseY - 100, size=45, bold=True)
    drawLabel("Total Yards Gained: " + str(app.totalYards),
              centerX - 200, baseY - 50, size=18, bold=True, align='left')
    drawLabel("Completions: " + str(app.numCompletions) + " / " + str(app.attempts),
              centerX - 200, baseY - 25, size=18, bold=True, align='left')
    drawLabel("Interceptions: " + str(app.ints),
              centerX - 200, baseY, size=18, bold=True, align='left')
    if app.lastPlayResult != "":
        drawLabel(f"Last Play Result: {app.lastPlayResult}",
                  centerX - 200, baseY + 25, size=18, bold=True, align='left')
        if app.lastPlayResult != 'Intercepted':
            drawLabel(f"Yards on Last Play: {app.lastYardsRan}",
                      centerX - 200, baseY + 50, size=18, bold=True, align='left')
        else:
            drawLabel("Yards on Last Play: N/A",
                      centerX - 200, baseY + 50, size=18, bold=True, align='left')

def drawDefense(app):
    offset = cameraOffset(app)
    for player in app.dFormation.values():
        cy = player.cy + offset
        if cy < 0 or cy > app.height:
            continue
        drawCircle(player.cx, cy, PLAYER_DRAW_RADIUS,
                   fill=DEFENSE_WHITE, border='black')

def drawOffense(app):
    offset = cameraOffset(app)
    for position in app.oFormation:
        player = app.oFormation[position]
        color = OFFENSE_RED
        if app.selectedPlayer == position and app.isOffensiveMenu:
            color = OFFENSE_RED_SELECTED
        cy = player.cy + offset
        if cy < 0 or cy > app.height:
            continue
        drawCircle(player.cx, cy, PLAYER_DRAW_RADIUS, fill=color, border='black')
        if isinstance(player, SkillPlayer) and not app.playIsActive:
            player.drawRoute(app)

def drawSideline(app):
    los = app.lineOfScrimmage
    homeBench = [
        (app.sideLineOffset - 10, los - 50), (app.sideLineOffset - 20, los - 25),
        (app.sideLineOffset - 20, los - 75), (app.sideLineOffset - 25, los - 100),
        (app.sideLineOffset - 25, los - 125),
        (42, 170), (41, 196), (40, 225), (46, 258), (45, 283),
        (43, 355), (47, 381), (46, 419),
        (42, 555), (44, 583), (40, 615), (42, 642),
    ]
    awayBench = [
        (app.width - app.sideLineOffset + 4, los + 8),
        (app.width - app.sideLineOffset + 20, los + 30),
        (app.width - app.sideLineOffset + 20, los - 21),
        (app.width - app.sideLineOffset + 20, los - 50),
        (app.width - app.sideLineOffset + 20, los - 75),
        (app.width - 42, 175), (app.width - 45, 202), (app.width - 41, 229),
        (app.width - 48, 300), (app.width - 43, 331), (app.width - 46, 370),
        (app.width - 41, 405),
        (app.width - 41, 470), (app.width - 41, 504), (app.width - 45, 542),
        (app.width - 40, 642), (app.width - 49, 675), (app.width - 42, 702),
    ]
    for x, y in homeBench:
        drawCircle(x, y, PLAYER_DRAW_RADIUS, fill=OFFENSE_RED, border='black')
    for x, y in awayBench:
        drawCircle(x, y, PLAYER_DRAW_RADIUS, fill=DEFENSE_WHITE, border='black')

def drawInstructionPanelFrame(app):
    drawModalBackdrop(app)
    panelCy = app.height // 2 - INSTR_PANEL_OFFSET_Y
    drawRect(app.width // 2, panelCy, INSTR_PANEL_WIDTH, INSTR_PANEL_HEIGHT,
             fill=rgb(60, 100, 60), border='black', opacity=88, align='center')
    drawLabel("Instructions:", app.width // 2, panelCy - 130, size=45, bold=True)
    drawPanelCloseButton(app.width // 2, panelCy, INSTR_PANEL_WIDTH, INSTR_PANEL_HEIGHT)

def drawFieldInstructions(app):
    offset = 175
    left = app.width // 2 - 200
    top = app.height // 2 - offset
    drawInstructionPanelFrame(app)
    drawLabel("- Press the spacebar to pause/resume",
              left, top - 70, size=18, bold=True, align='left')
    drawLabel("- Click and hold to throw the ball",
              left, top - 40, size=18, bold=True, align='left')
    drawLabel("Hold longer for a faster throw",
              app.width // 2 - 150, top - 15, size=18, bold=True, align='left')
    drawLabel("- Use arrow keys to move ball carrier",
              left, top + 15, size=18, bold=True, align='left')
    drawLabel("- Press 'S' to step by one frame when paused",
              left, top + 45, size=18, bold=True, align='left')
    drawLabel("- Press 'R' to reset the play",
              left, top + 75, size=18, bold=True, align='left')
    drawLabel("- Press 'P' to toggle pass rushers",
              left, top + 105, size=18, bold=True, align='left')

def drawMainMenu(app):
    drawRect(0, 0, app.width, app.height,
             fill=gradient(MENU_GREEN_LIGHT, MENU_GREEN_MID, MENU_GREEN_DARK,
                           start='left-top'))
    drawLine(-6, 60, 200, app.height + 6, fill=MENU_RED, lineWidth=6)
    drawLine(50, -6, 50, app.height + 6, fill=MENU_RED_ACCENT, lineWidth=6)
    drawImage("routeLabLogo.png", app.width // 2, 150, align='center',
              width=750, height=300)
    drawLabel("Create your own football", app.width // 2, 270,
              size=35, bold=True, font='monospace')
    drawLabel("routes and dominate the game.", app.width // 2, 310,
              size=35, bold=True, font='monospace')
    drawStartCreatingButton(app)
    drawMainMenuRoutes(app)

def drawStartCreatingButton(app):
    centerX = app.width // 2
    centerY = app.height // 2 + 45
    if app.isMainMenuLabelHovering:
        drawRect(centerX, centerY, 510, 156, fill=MENU_RED,
                 border=MENU_RED, borderWidth=3, align='center')
        drawRect(centerX, centerY, 500, 150, fill=MENU_GREEN_MID,
                 border='black', borderWidth=3, align='center')
        drawRect(centerX, centerY, 500, 150, fill=HOVER_OVERLAY_COLOR,
                 opacity=HOVER_OVERLAY_OPACITY, align='center')
        drawLabel("Start Creating Plays ", centerX, centerY,
                  size=35, bold=True, font='monospace')
    else:
        drawRect(centerX, centerY, 506, 153, fill=MENU_RED,
                 border=MENU_RED, borderWidth=3, align='center')
        drawRect(centerX, centerY, 500, 150, fill=MENU_GREEN_MID,
                 border='black', borderWidth=3, align='center')
        drawLabel("Start Creating Plays ", centerX, centerY,
                  size=33, bold=False, font='monospace')

def drawMainMenuRoutes(app):
    nodeRadius = menuNodeRadius(app)

    drawLine(270, app.height - 60, 270, app.height - 225, lineWidth=7, arrowEnd=True)
    drawCircle(270, app.height - 60, nodeRadius, fill=MENU_RED, border='black')

    drawLine(340, app.height - 60, 340, app.height - 130, lineWidth=7)
    drawLine(340, app.height - 130, 450, app.height - 130, lineWidth=7, arrowEnd=True)
    drawRect(340, app.height - 130, 7, 7, fill='black', align='center')
    drawCircle(340, app.height - 60, nodeRadius, fill=MENU_RED, border='black')

    drawLine(app.width - 190, app.height - 60, app.width - 190,
             app.height - 150, lineWidth=7)
    drawLine(app.width - 190, app.height - 150, app.width - 270,
             app.height - 220, lineWidth=7, arrowEnd=True)
    drawRect(app.width - 190, app.height - 150, 7, 7, fill='black', align='center')
    drawCircle(app.width - 190, app.height - 60, nodeRadius, fill=MENU_RED, border='black')

def menuNodeRadius(app):
    pulse = math.sin(app.animationTicks * MENU_NODE_PULSE_SPEED)
    return MENU_NODE_BASE_RADIUS + MENU_NODE_PULSE_AMPLITUDE * pulse

def drawFieldButtons(app):
    for button in app.fieldButtons:
        button.draw()

def drawOffensiveMenu(app):
    drawField(app, scrimmageLine=False)
    drawLabel("Select Formation", app.sideLineOffset // 2, 17, size=20, bold=True)
    drawLabel("Select Route", app.width - app.sideLineOffset // 2, 17,
              size=20, bold=True)

    for button in app.offensiveFormationButtons:
        button.draw()
    drawRouteButtons(app)
    app.startGameButton.draw()
    app.importButton.draw()
    app.exportButton.draw()
    app.menuInstructionsButton.draw()
    drawOffense(app)
    if app.menuInstructionsButton.isInstructions:
        drawMenuInstructionsMenu(app)

def drawRouteButtons(app):
    activeName = selectedRouteName(app)
    routeButtons = (app.offensiveWRRouteButtons if app.isWRMenu
                    else app.offensiveRBRouteButtons)
    for button in routeButtons:
        button.active = button.text == activeName
        button.draw()

def selectedRouteName(app):
    if app.selectedPlayer is None:
        return None
    return getattr(app.oFormation[app.selectedPlayer], 'routeName', None)

def drawMenuInstructionsMenu(app):
    offset = 175
    left = app.width // 2 - 200
    top = app.height // 2 - offset
    drawInstructionPanelFrame(app)
    drawLabel("- Click a formation button to select formation",
              left, top - 70, size=18, bold=True, align='left')
    drawLabel("- Click a player then a route to select route",
              left, top - 40, size=18, bold=True, align='left')
    drawLabel("- Use arrow keys to move selected players",
              left, top - 10, size=18, bold=True, align='left')
    drawLabel("- Click a player and drag to create custom route",
              left, top + 20, size=18, bold=True, align='left')
    drawLabel("- Only import plays with exported file structure",
              left, top + 50, size=18, bold=True, align='left')
    drawLabel("to avoid failed imports",
              app.width // 2 - 150, top + 75, size=18, bold=True, align='left')

def drawField(app, scrimmageLine=True):
    drawRect(0, 0, app.width, app.height, fill=FIELD_GREEN)
    drawYardLines(app)
    if scrimmageLine and not app.isPlayActive:
        drawLine(BOUNDARY_OFFSET + app.sideLineOffset, app.lineOfScrimmage,
                 app.width - BOUNDARY_OFFSET - app.sideLineOffset,
                 app.lineOfScrimmage, fill='blue')
    drawSidelines(app)

def drawYardLines(app):
    yardMarkerCount = 1
    lineCount = 0
    leftEdge = 30 + app.sideLineOffset
    rightEdge = app.width - 30 - app.sideLineOffset
    for y in range(app.height, 0, -app.yardStep):
        lineCount += 1
        if lineCount % 5 == 0:
            drawLine(leftEdge, y, rightEdge, y, fill='white')
            if lineCount % 10 == 0:
                drawLabel(f'{yardMarkerCount} 0', 60 + app.sideLineOffset, y,
                          size=20, fill='white', rotateAngle=90)
                drawLabel(f'{yardMarkerCount} 0', app.width - 60 - app.sideLineOffset, y,
                          size=20, fill='white', rotateAngle=270)
                yardMarkerCount += 1
        else:
            drawLine(leftEdge, y, 40 + app.sideLineOffset, y, fill='white')
            drawLine(rightEdge, y, app.width - 40 - app.sideLineOffset, y, fill='white')
            drawLine(leftHashX(app), y, leftHashX(app) + 10, y, fill='white')
            drawLine(rightHashX(app), y, rightHashX(app) + 10, y, fill='white')

def drawSidelines(app):
    leftX = app.sideLineOffset + BOUNDARY_OFFSET
    rightX = app.width - BOUNDARY_OFFSET - app.sideLineOffset
    drawLine(leftX, 0, leftX, app.height, fill='white', lineWidth=4)
    drawLine(rightX, 0, rightX, app.height, fill='white', lineWidth=4)
