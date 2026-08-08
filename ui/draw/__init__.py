from ui.draw.field import drawField
from ui.draw.hud import (drawCoverageBetaTag, drawFieldHud, drawThrowIndicator,
                         drawThrowPowerBar, fieldInstructionsOpen, fieldStatsOpen,
                         updateFieldButtonStates)
from ui.draw.menus import (drawFieldButtons, drawFieldInstructions, drawMainMenu,
                           drawOffensiveMenu)
from ui.draw.modals import drawStatsMenu
from ui.draw.tokens import drawDefense, drawOffense, drawSideline


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
