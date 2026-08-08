from cmu_graphics import drawCircle, drawLabel
from constants import (DEFENSE_FILL, OFFENSE_RED, OFFENSE_RED_SELECTED,
                       PLAYER_DRAW_RADIUS, PLAYER_LABEL_COLOR, PLAYER_LABEL_SIZE,
                       ROUTE_COLOR_DEFAULT, ROUTE_COLORS_BY_POSITION)
from domain import (Lineman, Quarterback, RunningBack, SkillPlayer, TightEnd,
                    WideReceiver)
from ui.draw.field import cameraOffset


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
