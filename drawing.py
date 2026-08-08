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
    opacityScale = 55 / app.maxBallVelo
    circleScale = 2.5
    drawCircle(app.mouseX, app.mouseY, app.ballVelocity * circleScale,
               fill=THROW_AIM_COLOR, opacity=app.ballVelocity * opacityScale)

def drawThrowPowerBar(app):
    if not (app.throwing and app.oFormation['QB'].cy > app.lineOfScrimmage):
        return
    fraction = min(app.ballVelocity / app.maxBallVelo, 1)
    centerX = app.width // 2
    trackY = app.height - POWER_BAR_BOTTOM_MARGIN
    trackLeft = centerX - POWER_BAR_WIDTH // 2
    drawRect(centerX, trackY, POWER_BAR_WIDTH, POWER_BAR_HEIGHT,
             fill=POWER_BAR_TRACK_COLOR, border=POWER_BAR_BORDER,
             borderWidth=HUD_PANEL_BORDER_WIDTH, align='center',
             opacity=POWER_BAR_TRACK_OPACITY)
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

def drawGlassPanel(cx, cy, width, height, fill, opacity,
                   border=HUD_PANEL_BORDER):
    drawRect(cx, cy, width, height, fill=fill, border=border,
             borderWidth=HUD_PANEL_BORDER_WIDTH, align='center', opacity=opacity)

def drawResultBanner(app):
    gainedYards = app.playResult.startswith('Tackled')
    color = BANNER_GAIN_COLOR if gainedYards else BANNER_LOSS_COLOR
    centerX = app.width // 2
    drawGlassPanel(centerX, HUD_TOP_Y, RESULT_BANNER_WIDTH, RESULT_BANNER_HEIGHT,
                   color, RESULT_BANNER_OPACITY)
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
    drawGlassPanel(centerX, HUD_TOP_Y, LIVE_YARDS_WIDTH, LIVE_YARDS_HEIGHT,
                   HUD_PANEL_COLOR, HUD_PANEL_OPACITY)
    drawLabel(f'{yards} yds', centerX, HUD_TOP_Y, size=20, bold=True,
              fill=HUD_TEXT_COLOR)

def drawPauseHint(app):
    if app.playResult != '' or not app.isPaused or anyFieldModalOpen(app):
        return
    text = 'Press SPACE to hike' if not app.playIsActive else 'Paused - SPACE to resume'
    centerX = app.width // 2
    hintY = app.height - HUD_BOTTOM_MARGIN
    drawGlassPanel(centerX, hintY, PAUSE_HINT_WIDTH, PAUSE_HINT_HEIGHT,
                   HUD_PANEL_COLOR, PAUSE_HINT_OPACITY)
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
    drawGlassPanel(centerX, baseY, STATS_PANEL_WIDTH, STATS_PANEL_HEIGHT,
                   MODAL_PANEL_COLOR, MODAL_PANEL_OPACITY, MODAL_PANEL_BORDER)
    drawPanelCloseButton(centerX, baseY, STATS_PANEL_WIDTH, STATS_PANEL_HEIGHT)
    drawLabel("Stats:", centerX, baseY - 100, size=45, bold=True,
              fill=HUD_TEXT_COLOR)
    drawLabel("Total Yards Gained: " + str(app.totalYards),
              centerX - 200, baseY - 50, size=18, bold=True, align='left',
              fill=HUD_TEXT_COLOR)
    drawLabel("Completions: " + str(app.numCompletions) + " / " + str(app.attempts),
              centerX - 200, baseY - 25, size=18, bold=True, align='left',
              fill=HUD_TEXT_COLOR)
    drawLabel("Interceptions: " + str(app.ints),
              centerX - 200, baseY, size=18, bold=True, align='left',
              fill=HUD_TEXT_COLOR)
    if app.lastPlayResult != "":
        drawLabel(f"Last Play Result: {app.lastPlayResult}",
                  centerX - 200, baseY + 25, size=18, bold=True, align='left',
                  fill=HUD_TEXT_COLOR)
        if app.lastPlayResult != 'Intercepted':
            drawLabel(f"Yards on Last Play: {app.lastYardsRan}",
                      centerX - 200, baseY + 50, size=18, bold=True, align='left',
                      fill=HUD_TEXT_COLOR)
        else:
            drawLabel("Yards on Last Play: N/A",
                      centerX - 200, baseY + 50, size=18, bold=True, align='left',
                      fill=HUD_TEXT_COLOR)

def drawPlayerToken(cx, cy, fill, label=None, labelColor=PLAYER_LABEL_COLOR):
    drawCircle(cx, cy, PLAYER_DRAW_RADIUS, fill=fill)
    if label is not None:
        drawLabel(label, cx, cy, size=PLAYER_LABEL_SIZE, bold=True, fill=labelColor)

def offenseFill(selected):
    return OFFENSE_RED_SELECTED if selected else OFFENSE_RED

def skillPositionLabel(position, player):
    if isinstance(player, Lineman):
        return None
    if isinstance(player, Quarterback) or position == 'QB':
        return 'QB'
    if isinstance(player, RunningBack) or position == 'RB':
        return 'RB'
    if isinstance(player, TightEnd) or position == 'TE':
        return 'TE'
    if isinstance(player, WideReceiver) or position.startswith('WR'):
        return 'WR'
    return None

def routeColorForPosition(position):
    return ROUTE_COLORS_BY_POSITION.get(position, ROUTE_COLOR_DEFAULT)

def drawDefense(app):
    offset = cameraOffset(app)
    for player in app.dFormation.values():
        cy = player.cy + offset
        if cy < 0 or cy > app.height:
            continue
        drawPlayerToken(player.cx, cy, DEFENSE_FILL)

def drawOffense(app):
    offset = cameraOffset(app)
    showLabels = not app.playIsActive
    for position in app.oFormation:
        player = app.oFormation[position]
        selected = app.selectedPlayer == position and app.isOffensiveMenu
        cy = player.cy + offset
        if cy < 0 or cy > app.height:
            continue
        label = skillPositionLabel(position, player) if showLabels else None
        drawPlayerToken(player.cx, cy, offenseFill(selected), label)
        if isinstance(player, SkillPlayer) and not app.playIsActive:
            player.drawRoute(app, routeColorForPosition(position))

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
        drawPlayerToken(x, y, OFFENSE_RED)
    for x, y in awayBench:
        drawPlayerToken(x, y, DEFENSE_FILL)

def drawInstructionPanelFrame(app):
    drawModalBackdrop(app)
    panelCy = app.height // 2 - INSTR_PANEL_OFFSET_Y
    drawGlassPanel(app.width // 2, panelCy, INSTR_PANEL_WIDTH, INSTR_PANEL_HEIGHT,
                   MODAL_PANEL_COLOR, MODAL_PANEL_OPACITY, MODAL_PANEL_BORDER)
    drawLabel("Instructions:", app.width // 2, panelCy - 130, size=45, bold=True,
              fill=HUD_TEXT_COLOR)
    drawPanelCloseButton(app.width // 2, panelCy, INSTR_PANEL_WIDTH, INSTR_PANEL_HEIGHT)

def drawFieldInstructions(app):
    offset = 175
    left = app.width // 2 - 200
    top = app.height // 2 - offset
    drawInstructionPanelFrame(app)
    drawLabel("- Press the spacebar to pause/resume",
              left, top - 70, size=18, bold=True, align='left', fill=HUD_TEXT_COLOR)
    drawLabel("- Click and hold to throw the ball",
              left, top - 40, size=18, bold=True, align='left', fill=HUD_TEXT_COLOR)
    drawLabel("Hold longer for a faster throw",
              app.width // 2 - 150, top - 15, size=18, bold=True, align='left',
              fill=HUD_TEXT_COLOR)
    drawLabel("- Use arrow keys to move ball carrier",
              left, top + 15, size=18, bold=True, align='left', fill=HUD_TEXT_COLOR)
    drawLabel("- Press 'S' to step by one frame when paused",
              left, top + 45, size=18, bold=True, align='left', fill=HUD_TEXT_COLOR)
    drawLabel("- Press 'R' to reset the play",
              left, top + 75, size=18, bold=True, align='left', fill=HUD_TEXT_COLOR)
    drawLabel("- Press 'P' to toggle pass rushers",
              left, top + 105, size=18, bold=True, align='left', fill=HUD_TEXT_COLOR)

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
    drawLabel("Select Formation", app.sideLineOffset // 2, 17, size=20, bold=True,
              fill=HUD_TEXT_COLOR)
    drawLabel("Select Route", app.width - app.sideLineOffset // 2, 17,
              size=20, bold=True, fill=HUD_TEXT_COLOR)

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
              left, top - 70, size=18, bold=True, align='left', fill=HUD_TEXT_COLOR)
    drawLabel("- Click a player then a route to select route",
              left, top - 40, size=18, bold=True, align='left', fill=HUD_TEXT_COLOR)
    drawLabel("- Use arrow keys to move selected players",
              left, top - 10, size=18, bold=True, align='left', fill=HUD_TEXT_COLOR)
    drawLabel("- Click a player and drag to create custom route",
              left, top + 20, size=18, bold=True, align='left', fill=HUD_TEXT_COLOR)
    drawLabel("- Only import plays with exported file structure",
              left, top + 50, size=18, bold=True, align='left', fill=HUD_TEXT_COLOR)
    drawLabel("to avoid failed imports",
              app.width // 2 - 150, top + 75, size=18, bold=True, align='left',
              fill=HUD_TEXT_COLOR)

def drawField(app, scrimmageLine=True):
    drawMowStripes(app)
    drawFieldApron(app)
    drawYardLines(app)
    if scrimmageLine and not app.isPlayActive:
        drawLineOfScrimmage(app)
    drawSidelines(app)

def drawMowStripes(app):
    # Yard line n is at height - (n - 1) * yardStep, so yard 0 is one
    # step below the screen bottom. Stripes flip on 0, 5, 10, ...
    offset = cameraOffset(app)
    stripeHeight = app.yardStep * MOW_STRIPE_YARDS
    yardZeroY = app.height + app.yardStep
    index = 0
    while yardZeroY - index * stripeHeight + offset < app.height:
        index -= 1
    while yardZeroY - index * stripeHeight + offset > 0:
        worldTop = yardZeroY - (index + 1) * stripeHeight
        color = FIELD_GREEN if index % 2 == 0 else FIELD_GREEN_STRIPE
        drawRect(0, worldTop + offset, app.width, stripeHeight, fill=color)
        index += 1

def drawFieldApron(app):
    leftX = app.sideLineOffset + BOUNDARY_OFFSET
    rightX = app.width - BOUNDARY_OFFSET - app.sideLineOffset
    drawRect(0, 0, leftX, app.height, fill=FIELD_APRON)
    drawRect(rightX, 0, app.width - rightX, app.height, fill=FIELD_APRON)

def drawLineOfScrimmage(app):
    offset = cameraOffset(app)
    losY = app.lineOfScrimmage + offset
    left = BOUNDARY_OFFSET + app.sideLineOffset
    right = app.width - BOUNDARY_OFFSET - app.sideLineOffset
    drawLine(left, losY, right, losY, fill=LOS_COLOR, lineWidth=LOS_WIDTH)
    tick = LOS_TICK_HALF
    for hashX in (leftHashX(app), rightHashX(app)):
        drawLine(hashX, losY - tick, hashX, losY + tick,
                 fill=LOS_COLOR, lineWidth=LOS_WIDTH)

def drawYardLines(app):
    offset = cameraOffset(app)
    yardMarkerCount = 1
    lineCount = 0
    leftEdge = 30 + app.sideLineOffset
    rightEdge = app.width - 30 - app.sideLineOffset
    yardStep = app.yardStep
    if yardStep <= 0:
        return
    # Walk by float yardStep so 5-/10-yard lines stay on true yard
    # boundaries after resize (int(yardStep) drifts when height changes).
    worldY = float(app.height)
    while worldY > 0:
        lineCount += 1
        y = worldY + offset
        if lineCount % 5 == 0:
            drawMajorYardLine(app, leftEdge, rightEdge, y, lineCount,
                              yardMarkerCount)
            if lineCount % 10 == 0:
                yardMarkerCount += 1
        else:
            drawHashMarks(app, leftEdge, rightEdge, y)
        worldY -= yardStep

def drawMajorYardLine(app, leftEdge, rightEdge, y, lineCount, yardMarkerCount):
    isTenYard = lineCount % 10 == 0
    color = YARD_LINE_MAJOR if isTenYard else YARD_LINE_MINOR
    width = YARD_LINE_MAJOR_WIDTH if isTenYard else YARD_LINE_MINOR_WIDTH
    drawLine(leftEdge, y, rightEdge, y, fill=color, lineWidth=width)
    if not isTenYard:
        return
    drawLabel(f'{yardMarkerCount} 0', 60 + app.sideLineOffset, y,
              size=YARD_NUMBER_SIZE, fill=YARD_NUMBER_COLOR, rotateAngle=90)
    drawLabel(f'{yardMarkerCount} 0', app.width - 60 - app.sideLineOffset, y,
              size=YARD_NUMBER_SIZE, fill=YARD_NUMBER_COLOR, rotateAngle=270)

def drawHashMarks(app, leftEdge, rightEdge, y):
    mark = HASH_MARK_LENGTH
    drawLine(leftEdge, y, leftEdge + mark, y, fill=HASH_MARK_COLOR)
    drawLine(rightEdge, y, rightEdge - mark, y, fill=HASH_MARK_COLOR)
    drawLine(leftHashX(app), y, leftHashX(app) + mark, y, fill=HASH_MARK_COLOR)
    drawLine(rightHashX(app), y, rightHashX(app) + mark, y, fill=HASH_MARK_COLOR)

def drawSidelines(app):
    leftX = app.sideLineOffset + BOUNDARY_OFFSET
    rightX = app.width - BOUNDARY_OFFSET - app.sideLineOffset
    drawLine(leftX, 0, leftX, app.height, fill='white', lineWidth=SIDELINE_WIDTH)
    drawLine(rightX, 0, rightX, app.height, fill='white', lineWidth=SIDELINE_WIDTH)
