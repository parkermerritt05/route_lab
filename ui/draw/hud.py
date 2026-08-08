from cmu_graphics import drawCircle, drawLabel, drawRect
from constants import (BANNER_GAIN_COLOR, BANNER_LOSS_COLOR, COVERAGE_BETA_COLOR,
                       COVERAGE_BETA_GAP, COVERAGE_BETA_SIZE, COVERAGE_BETA_TEXT,
                       HUD_BOTTOM_MARGIN, HUD_PANEL_COLOR, HUD_PANEL_OPACITY,
                       HUD_TEXT_COLOR, HUD_TOP_Y, PAUSE_HINT_HEIGHT,
                       PAUSE_HINT_OPACITY, PAUSE_HINT_WIDTH, POWER_BAR_BORDER,
                       POWER_BAR_BOTTOM_MARGIN, POWER_BAR_FILL_HIGH,
                       POWER_BAR_FILL_LOW, POWER_BAR_FULL_THRESHOLD,
                       POWER_BAR_HEIGHT, POWER_BAR_TRACK_COLOR,
                       POWER_BAR_TRACK_OPACITY, POWER_BAR_WIDTH,
                       RESULT_BANNER_HEIGHT, RESULT_BANNER_OPACITY,
                       RESULT_BANNER_WIDTH, THROW_AIM_COLOR,
                       HUD_PANEL_BORDER_WIDTH)
from ui.draw.modals import drawGlassPanel


def controlsAreLive(app):
    return app.playResult != '' or app.isPaused


def fieldInstructionsOpen(app):
    return app.fieldInstructionsButton.isInstructions and controlsAreLive(app)


def fieldStatsOpen(app):
    return app.statsButton.isStats and controlsAreLive(app)


def anyFieldModalOpen(app):
    return fieldInstructionsOpen(app) or fieldStatsOpen(app)


def updateFieldButtonStates(app):
    app.statsButton.enabled = controlsAreLive(app)
    app.fieldInstructionsButton.enabled = controlsAreLive(app)
    app.coverageButton.enabled = controlsAreLive(app)


def drawCoverageBetaTag(app):
    if app.coverageShell != 'Cover 2':
        return
    button = app.coverageButton
    tagY = button.cy + button.h // 2 + COVERAGE_BETA_GAP
    drawLabel(COVERAGE_BETA_TEXT, button.cx, tagY, size=COVERAGE_BETA_SIZE,
              bold=True, italic=True, fill=COVERAGE_BETA_COLOR)


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


def drawPauseHint(app):
    if app.playResult != '' or not app.isPaused or anyFieldModalOpen(app):
        return
    text = 'Press SPACE to hike' if not app.playIsActive else 'Paused - SPACE to resume'
    centerX = app.width // 2
    hintY = app.height - HUD_BOTTOM_MARGIN
    drawGlassPanel(centerX, hintY, PAUSE_HINT_WIDTH, PAUSE_HINT_HEIGHT,
                   HUD_PANEL_COLOR, PAUSE_HINT_OPACITY)
    drawLabel(text, centerX, hintY, size=15, bold=True, fill=HUD_TEXT_COLOR)
