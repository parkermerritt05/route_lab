from constants import (INSTR_PANEL_HEIGHT, INSTR_PANEL_OFFSET_Y, INSTR_PANEL_WIDTH,
                       PLAYER_DRAW_RADIUS, STATS_PANEL_HEIGHT,
                       STATS_PANEL_OFFSET_Y, STATS_PANEL_WIDTH)
from coverage.setup import initializeDefense
from play_io.import_export import exportData, importData
from simulation.geometry import distance
from ui.buttons import panelCloseCenter, panelCloseContains


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
        app.pendingDeselect = position
    else:
        app.pendingDeselect = None
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
