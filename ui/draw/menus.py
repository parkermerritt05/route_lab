import math
from cmu_graphics import (drawCircle, drawImage, drawLabel, drawLine, drawRect,
                          gradient)
from constants import (HOVER_OVERLAY_COLOR, HOVER_OVERLAY_OPACITY, HUD_TEXT_COLOR,
                       MENU_GREEN_DARK, MENU_GREEN_LIGHT, MENU_GREEN_MID,
                       MENU_NODE_BASE_RADIUS, MENU_NODE_PULSE_AMPLITUDE,
                       MENU_NODE_PULSE_SPEED, MENU_RED, MENU_RED_ACCENT)
from ui.draw.field import drawField
from ui.draw.modals import drawInstructionPanelFrame
from ui.draw.tokens import drawOffense


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
