from constants import *


def applyWindowMetrics(app):
    app.sideLineOffset = round(app.width * DESIGN_SIDELINE / DESIGN_WIDTH)
    app.yardStep = app.height * DESIGN_YARD_STEP / DESIGN_HEIGHT
    app.lineOfScrimmage = (
        app.height - (app.yardStep * SCRIMMAGE_YARDS_FROM_BOTTOM))
    app.velocity = app.yardsPerSecond * (app.yardStep / app.stepsPerSecond)
    app.maxSpeed = app.velocity
    app.acceleration = 0.2 * app.yardStep / app.stepsPerSecond
    app.fieldSides = [30, app.width - 30]


def midX(app, designDx):
    return app.width // 2 + designDx * app.width / DESIGN_WIDTH


def losY(app, designDy):
    return app.lineOfScrimmage + designDy * app.height / DESIGN_HEIGHT


def designY(app, designYCoord):
    return designYCoord * app.height / DESIGN_HEIGHT


def onResize(app):
    from init import loadDefensiveFormations

    oldW = getattr(app, 'prevWidth', 0)
    oldH = getattr(app, 'prevHeight', 0)
    applyWindowMetrics(app)
    if oldW <= 0 or oldH <= 0:
        app.prevWidth, app.prevHeight = app.width, app.height
        return
    if not hasattr(app, 'offensiveFormationButtons'):
        app.prevWidth, app.prevHeight = app.width, app.height
        return
    placeButtons(app)
    rescalePlayState(app, oldW, oldH)
    if getattr(app, 'isPlayActive', False):
        scaleZones(app, app.width / oldW, app.height / oldH)
    elif hasattr(app, 'oFormation'):
        loadDefensiveFormations(app)
    app.prevWidth, app.prevHeight = app.width, app.height


def rescalePlayState(app, oldW, oldH):
    sx = app.width / oldW
    sy = app.height / oldH
    for formation in allFormations(app):
        for player in formation.values():
            scalePlayer(player, sx, sy)
    if hasattr(app, 'dFormation'):
        for player in app.dFormation.values():
            scalePlayer(player, sx, sy)
    if hasattr(app, 'ball') and app.ball is not None:
        scaleBall(app.ball, sx, sy)


def allFormations(app):
    names = ('singleBack', 'shotgun', 'spread', 'bunch', 'custom')
    seen = set()
    formations = []
    for name in names:
        formation = getattr(app, name, None)
        if formation is None or id(formation) in seen:
            continue
        seen.add(id(formation))
        formations.append(formation)
    oFormation = getattr(app, 'oFormation', None)
    if oFormation is not None and id(oFormation) not in seen:
        formations.append(oFormation)
    return formations


def scalePlayer(player, sx, sy):
    player.cx *= sx
    player.cy *= sy
    player.startX *= sx
    player.startY *= sy
    if player.targetX is not None:
        player.targetX *= sx
    if player.targetY is not None:
        player.targetY *= sy
    # Routes are absolute pixel polylines baked at assign-time.
    if getattr(player, 'route', None):
        player.route = [(x * sx, y * sy) for (x, y) in player.route]


def scaleBall(ball, sx, sy):
    ball.cx *= sx
    ball.cy *= sy
    if ball.targetX is not None:
        ball.targetX *= sx
    if ball.targetY is not None:
        ball.targetY *= sy


def scaleZones(app, sx, sy):
    if not hasattr(app, 'zones'):
        return
    for zone in app.zones.values():
        zone.left *= sx
        zone.right *= sx
        zone.top *= sy
        zone.bottom *= sy
        zone.cx *= sx
        zone.cy *= sy


def placeButtons(app):
    placeMenuButtons(app)
    placeFieldButtons(app)
    placeStatsButton(app)


def placeMenuButtons(app):
    leftCol = 95 * app.width / DESIGN_WIDTH
    formationYs = (80, 170, 260, 350, 440)
    for button, y in zip(app.offensiveFormationButtons, formationYs):
        button.cx = leftCol
        button.cy = designY(app, y)

    app.menuInstructionsButton.cx = 105 * app.width / DESIGN_WIDTH
    app.menuInstructionsButton.cy = designY(app, 538)

    rightCol = app.width - 95 * app.width / DESIGN_WIDTH
    routeYs = (50, 110, 170, 230, 290, 350, 410, 470, 530, 590, 650, 710)
    for button, y in zip(app.offensiveWRRouteButtons, routeYs):
        button.cx = rightCol
        button.cy = designY(app, y)

    rbYs = (50, 110)
    for button, y in zip(app.offensiveRBRouteButtons, rbYs):
        button.cx = rightCol
        button.cy = designY(app, y)

    app.fieldInstructionsButton.cx = app.width - 100 * app.width / DESIGN_WIDTH
    app.fieldInstructionsButton.cy = designY(app, 50)
    app.startGameButton.cx = app.width // 2
    app.startGameButton.cy = designY(app, 650)

    gutter = app.sideLineOffset // 2
    app.importButton.cx = gutter
    app.importButton.cy = app.height - designY(app, 120)
    app.exportButton.cx = gutter
    app.exportButton.cy = app.height - designY(app, 45)


def placeFieldButtons(app):
    gutter = app.sideLineOffset // 2
    app.fieldButtons[0].cx = gutter
    app.fieldButtons[0].cy = designY(app, 40)
    app.fieldButtons[1].cx = gutter
    app.fieldButtons[1].cy = designY(app, 110)
    app.coverageButton.cx = gutter
    app.coverageButton.cy = designY(app, 500)


def placeStatsButton(app):
    app.statsButton.cx = app.width - 100 * app.width / DESIGN_WIDTH
    app.statsButton.cy = designY(app, 130)
