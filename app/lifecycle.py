from constants import DESIGN_HEIGHT, DESIGN_WIDTH
from content.formations import loadOffensiveFormations
from content.routes import loadOffensiveRoutes
from coverage.setup import loadDefensiveFormations
from domain import Ball, SkillPlayer
from app.menu_buttons import loadFieldButtons, loadOffensiveMenuButtons, loadStats
from ui.layout import applyWindowMetrics, placeButtons


def onAppStart(app):
    app.width = DESIGN_WIDTH
    app.height = DESIGN_HEIGHT
    app.prevWidth = app.width
    app.prevHeight = app.height
    app.yardLine = 0
    app.totalYards = 0
    app.score = 0
    app.stepsPerSecond = 40
    app.yardsPerSecond = 5
    applyWindowMetrics(app)
    app.maxBallVelo = 6
    app.mouseX = 0
    app.mouseY = 0
    app.isPassRush = True
    app.lastPlayResult = ''
    app.lastYardsRan = 0
    app.indexExport = 0
    app.coverageShell = 'Cover 1'
    app.animationTicks = 0
    app.pressedButton = None

    loadOffensiveRoutes(app)
    loadOffensiveFormations(app, firstTime=True)
    loadStats(app)
    loadFieldButtons(app)
    loadOffensiveMenuButtons(app)
    placeButtons(app)
    resetApp(app)

    app.isField = False
    app.isMainMenu = True
    app.isOffensiveMenu = False
    app.isMainMenuLabelHovering = False
    app.isWRMenu = True


def resetApp(app, isField=True):
    for player in app.oFormation.values():
        player.cx = player.startX
        player.cy = player.startY
        player.dx = 0
        player.dy = 0
        if isinstance(player, SkillPlayer):
            player.targetX = player.startX
            player.targetY = player.startY
    app.playIsActive = False
    app.exportButton.text = "Export Play"
    app.selectedPlayer = None
    app.isDefensiveMenu = False
    app.isOffensiveMenu = False
    app.isField = isField
    if not isField:
        app.isOffensiveMenu = True
    app.isRouteCombination = False
    app.isPaused = True
    app.steps = 0
    app.playResult = ''
    app.yardsRan = 0
    app.isPlayActive = False
    app.ballVelocity = 0
    app.throwing = False
    app.qbRun = True
    app.ballCarrier = None
    app.statsButton.isStats = False
    app.ball = Ball(app.oFormation['C'].cx, app.oFormation['C'].cy, app.oFormation['C'])
    if hasattr(app, 'coverageButton'):
        app.coverageButton.text = f"Coverage: {'C2' if app.coverageShell == 'Cover 2' else 'C1'}"
    loadDefensiveFormations(app)
