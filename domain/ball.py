import math
from cmu_graphics import drawLine, drawOval
from constants import (BALL_ARC_ACCELERATION, BALL_FILL, BALL_LACE_COLOR,
                       CAMERA_SCROLL_YARDS, CATCH_HEIGHT, DEFLECT_HEIGHT,
                       PLAYER_HIT_RADIUS, SNAP_BALL_VELOCITY, THROW_START_HEIGHT)
from domain.defense import CoverPlayer
from domain.offense import Quarterback, SkillPlayer
from simulation.geometry import distance, getRadiusAndAngleToEndpoint


class Ball:
    def __init__(self, cx, cy, carrier, dx=0, dy=0, targetX=None, targetY=None):
        self.carrier = carrier
        self.dx = dx
        self.dy = dy
        self.cx = cx
        self.cy = cy
        self.targetX = targetX
        self.targetY = targetY
        self.beingSnapped = False
        self.height = 0

    def drawBall(self, app):
        offset = 0
        if self.cy <= CAMERA_SCROLL_YARDS * app.yardStep:
            offset = CAMERA_SCROLL_YARDS * app.yardStep - self.cy
        scaleFactor = 1 + self.height / 50
        angle = self.getAngle()
        cx, cy = self.cx, self.cy + offset
        width, height = 10 * scaleFactor, 5 * scaleFactor
        drawOval(cx, cy, width, height, fill=BALL_FILL, align='center',
                 rotateAngle=angle)
        laceHalf = 2.2 * scaleFactor
        rad = math.radians(angle)
        dx, dy = laceHalf * math.cos(rad), laceHalf * math.sin(rad)
        drawLine(cx - dx, cy - dy, cx + dx, cy + dy,
                 fill=BALL_LACE_COLOR, lineWidth=1)

    def throwToTarget(self, targetX, targetY, app):
        self.targetX = targetX
        self.targetY = targetY
        self.carrier = None
        self.height = THROW_START_HEIGHT
        self.throwDistance = distance(self.cx, self.cy, targetX, targetY)
        dx = self.targetX - self.cx
        dy = self.targetY - self.cy
        ratio = app.ballVelocity / self.throwDistance
        self.dx = dx * ratio
        self.dy = dy * ratio
        self.distanceTravelled = 0

    def updateBallPosition(self, app):
        if self.carrier is not None:
            if self.carrier == app.oFormation['C']:
                self.beingSnapped = True
                app.ballVelocity = SNAP_BALL_VELOCITY
                self.throwToTarget(app.oFormation['QB'].cx,
                                   app.oFormation['QB'].cy, app)
                return
            self.cx = self.carrier.cx
            self.cy = self.carrier.cy
        elif app.playResult == 'Incomplete':
            self.dx = 0
            self.dy = 0
            self.cx += self.dx
            self.cy += self.dy
        elif self.targetX is not None and self.targetY is not None:
            self.cx += self.dx
            self.cy += self.dy
            self.distanceTravelled += app.ballVelocity
            self.updateHeight(app)
            self.checkCatch(app)

    def updateHeight(self, app):
        timePassed = self.distanceTravelled / app.ballVelocity
        totalTime = self.throwDistance / app.ballVelocity
        initialVerticalSpeed = BALL_ARC_ACCELERATION * totalTime / 2
        verticalSpeed = initialVerticalSpeed - BALL_ARC_ACCELERATION * timePassed
        self.height += verticalSpeed

    def checkCatch(self, app):
        if self.height <= 0:
            self.markIncomplete(app)
        elif self.height <= CATCH_HEIGHT:
            self.tryCatch(app)
        elif self.height <= DEFLECT_HEIGHT:
            self.tryDeflect(app)

    def markIncomplete(self, app, countAttempt=True):
        app.playResult = 'Incomplete'
        app.lastPlayResult = 'Incomplete'
        app.lastYardsRan = 0
        if countAttempt:
            app.attempts += 1
        app.isPaused = True
        self.height = 0
        self.dx, self.dy = 0, 0
        self.targetX, self.targetY = None, None

    def tryCatch(self, app):
        receiver = self.nearestCatcher(app)
        if receiver is None:
            return
        self.beingSnapped = False
        self.carrier = receiver
        if isinstance(receiver, CoverPlayer):
            app.playResult = 'Intercepted'
            app.lastPlayResult = 'Intercepted'
            app.lastYardsRan = 0
            app.ints += 1
        self.cx = receiver.cx
        self.cy = receiver.cy
        self.dx, self.dy = 0, 0
        self.targetX, self.targetY = None, None
        self.height = 0

    def nearestCatcher(self, app):
        closestReceiver = None
        closestDistance = float('inf')
        allPlayers = list(app.oFormation.values()) + list(app.dFormation.values())
        for player in allPlayers:
            if not self.canCatch(player):
                continue
            distToBall = distance(self.cx, self.cy, player.cx, player.cy)
            if distToBall < closestDistance:
                closestDistance = distToBall
                closestReceiver = player
        if closestDistance <= PLAYER_HIT_RADIUS:
            return closestReceiver
        return None

    def canCatch(self, player):
        return (isinstance(player, SkillPlayer)
                or (isinstance(player, Quarterback) and self.beingSnapped)
                or isinstance(player, CoverPlayer))

    def tryDeflect(self, app):
        for player in app.dFormation.values():
            if not isinstance(player, CoverPlayer):
                continue
            if distance(self.cx, self.cy, player.cx, player.cy) <= PLAYER_HIT_RADIUS:
                self.markIncomplete(app)
                return

    def getAngle(self):
        if self.targetX is not None and self.targetY is not None:
            _, angle = getRadiusAndAngleToEndpoint(self.cx, self.cy,
                                                   self.targetX, self.targetY)
            return -angle
        return 90
