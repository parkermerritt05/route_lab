from cmu_graphics import drawLine
from constants import (CAMERA_SCROLL_YARDS, PLAYER_DRAW_RADIUS,
                       ROUTE_COLOR_DEFAULT, ROUTE_FIELD_WIDTH)
from domain.player import Player
from simulation.geometry import clampX, distance


class SkillPlayer(Player):
    def __init__(self, app, cx, cy, dx=0, dy=0, route=None, translated=False):
        super().__init__(cx, cy, dx, dy)
        self.targetX = self.cx + route[0][0] * app.yardStep
        self.targetY = self.cy + route[0][1] * app.yardStep
        self.routeName = None
        if not translated:
            self.route = self.translateRoute(app, route)
        else:
            self.route = route

    def runRoute(self, app):
        yardsRunAlready = 0
        for i in range(1, len(self.route)):
            currStep = self.route[i]
            prevStep = self.route[i - 1]
            step = (currStep[0] - prevStep[0], currStep[1] - prevStep[1])
            stepLength = ((step[0])**2 + (step[1])**2)**0.5 / app.yardStep
            if app.yardsRan >= stepLength + yardsRunAlready:
                yardsRunAlready += stepLength
                if i == len(self.route) - 1:
                    self.goToPoint(app)
                    break
            else:
                self.targetX = currStep[0]
                self.targetY = currStep[1]
                self.goToPoint(app)
                break
        self.movePlayer(app)

    def translateRoute(self, app, route):
        newRoute = [(x * app.yardStep, y * app.yardStep) for (x, y) in route]
        newRoute = [(self.startX, self.startY)] + newRoute
        for i in range(1, len(newRoute)):
            endX, endY = newRoute[i]
            startX, startY = newRoute[i - 1]
            endX += startX
            endY += startY
            newRoute[i] = (clampX(app, endX), endY)
        return newRoute

    def routeDrawPoint(self, index, cameraShift):
        x, y = self.route[index]
        resolved = index if index >= 0 else len(self.route) + index
        if resolved == 0:
            x, y = self.routeStartOnRim()
        return x, y + cameraShift

    def routeStartOnRim(self):
        if len(self.route) < 2:
            return self.cx, self.cy - PLAYER_DRAW_RADIUS
        nextX, nextY = self.route[1]
        dx = nextX - self.cx
        dy = nextY - self.cy
        dist = distance(self.cx, self.cy, nextX, nextY)
        if dist == 0:
            return self.cx, self.cy - PLAYER_DRAW_RADIUS
        scale = PLAYER_DRAW_RADIUS / dist
        return self.cx + dx * scale, self.cy + dy * scale

    def drawRoute(self, app, color=ROUTE_COLOR_DEFAULT):
        if len(self.route) < 2:
            return
        offset = 0
        if app.ball.cy <= CAMERA_SCROLL_YARDS * app.yardStep:
            offset = CAMERA_SCROLL_YARDS * app.yardStep - app.ball.cy
        for i in range(1, len(self.route) - 1):
            startX, startY = self.routeDrawPoint(i - 1, offset)
            endX, endY = self.routeDrawPoint(i, offset)
            drawLine(startX, startY, endX, endY,
                     fill=color, lineWidth=ROUTE_FIELD_WIDTH)
        prevX, prevY = self.routeDrawPoint(-2, offset)
        arrowX, arrowY = self.routeDrawPoint(-1, offset)
        arrowX = clampX(app, arrowX)
        drawLine(prevX, prevY, arrowX, arrowY,
                 fill=color, lineWidth=ROUTE_FIELD_WIDTH, arrowEnd=True)


class WideReceiver(SkillPlayer):
    def __init__(self, app, cx, cy, dx=0, dy=0, route=None, translated=False):
        super().__init__(app, cx, cy, dx, dy, route, translated)


class RunningBack(SkillPlayer):
    def __init__(self, app, cx, cy, dx=0, dy=0, route=None, translated=False):
        super().__init__(app, cx, cy, dx, dy, route, translated)


class TightEnd(SkillPlayer):
    def __init__(self, app, cx, cy, dx=0, dy=0, route=None, translated=False):
        super().__init__(app, cx, cy, dx, dy, route, translated)


class Quarterback(Player):
    def __init__(self, cx, cy, dx=0, dy=0):
        super().__init__(cx, cy, dx, dy)


class Lineman(Player):
    def __init__(self, cx, cy, dx=0, dy=0):
        super().__init__(cx, cy, dx, dy)
