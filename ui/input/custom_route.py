from constants import BOUNDARY_OFFSET, PLAYER_DRAW_RADIUS
from simulation.geometry import distance
from ui.buttons import releasePressedButton


def onMouseDrag(app, mouseX, mouseY):
    if (app.isOffensiveMenu and app.selectedPlayer is not None and
            app.sideLineOffset + BOUNDARY_OFFSET <= mouseX
            <= app.width - app.sideLineOffset - BOUNDARY_OFFSET):
        extendCustomRoute(app, mouseX, mouseY)
    if app.isField and app.throwing:
        app.mouseX = mouseX
        app.mouseY = mouseY


def extendCustomRoute(app, mouseX, mouseY):
    player = app.oFormation[app.selectedPlayer]
    if not getattr(app, 'routeDragBegan', False):
        beginCustomRouteDrag(app, player, mouseX, mouseY)
        return
    if getattr(app, 'routeAwaitingExit', False):
        if pointInPlayerToken(player, mouseX, mouseY):
            return
        app.routeAwaitingExit = False
        edgeX, edgeY = projectOntoPlayerEdge(player, mouseX, mouseY)
        player.route = [(player.startX, player.startY), (edgeX, edgeY)]
        player.routeName = None
        return
    if pointInPlayerToken(player, mouseX, mouseY):
        return
    player.route += [(mouseX, mouseY)]
    player.routeName = None


def beginCustomRouteDrag(app, player, mouseX, mouseY):
    app.routeDragBegan = True
    app.pendingDeselect = None
    if pointInPlayerToken(player, mouseX, mouseY):
        player.route = [(player.startX, player.startY)]
        player.routeName = None
        app.routeAwaitingExit = True
        return
    app.routeAwaitingExit = False
    player.route += [(mouseX, mouseY)]
    player.routeName = None


def pointInPlayerToken(player, x, y):
    return distance(player.cx, player.cy, x, y) <= PLAYER_DRAW_RADIUS


def projectOntoPlayerEdge(player, x, y):
    dx = x - player.cx
    dy = y - player.cy
    dist = distance(player.cx, player.cy, x, y)
    if dist == 0:
        return player.cx, player.cy - PLAYER_DRAW_RADIUS
    scale = PLAYER_DRAW_RADIUS / dist
    return player.cx + dx * scale, player.cy + dy * scale


def onMouseRelease(app, mouseX, mouseY):
    releasePressedButton(app)
    if (getattr(app, 'pendingDeselect', None) is not None
            and app.selectedPlayer == app.pendingDeselect
            and not getattr(app, 'routeDragBegan', False)):
        app.selectedPlayer = None
    app.pendingDeselect = None
    if app.throwing and app.oFormation['QB'].cy >= app.lineOfScrimmage:
        app.throwing = False
        app.ball.throwToTarget(mouseX, mouseY, app)
