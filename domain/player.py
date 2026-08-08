import math
from constants import (BOUNDARY_OFFSET, GOAL_LINE_YARDS, PLAYER_HIT_RADIUS)
from simulation.geometry import (clampX, distance, getRadiusAndAngleToEndpoint,
                                 getRadiusEndpoint)


class Player:
    def __init__(self, cx, cy, dx=0, dy=0, targetX=None, targetY=None):
        self.startX = cx
        self.startY = cy
        self.cx = cx
        self.cy = cy
        self.dx = dx
        self.dy = dy
        self.targetX = targetX
        self.targetY = targetY

    def __repr__(self):
        return f"cx = {self.cx}, cy = {self.cy}"

    def __eq__(self, other):
        return (isinstance(other, Player) and
                self.cx == other.cx and
                self.cy == other.cy)

    def __hash__(self):
        return hash(str(self))

    def isOutOfBounds(self, app):
        return (self.cx <= app.sideLineOffset + BOUNDARY_OFFSET or
                self.cx >= app.width - BOUNDARY_OFFSET)

    def clickInPlayer(self, mouseX, mouseY):
        return distance(self.cx, self.cy, mouseX, mouseY) <= PLAYER_HIT_RADIUS

    def goToPoint(self, app):
        self.targetX = clampX(app, self.targetX)
        dx = self.targetX - self.cx
        dy = self.targetY - self.cy
        dist = distance(self.cx, self.cy, self.targetX, self.targetY)
        if dist == 0:
            return

        desiredVx = (dx / dist) * app.maxSpeed
        desiredVy = (dy / dist) * app.maxSpeed
        slowdownDist = 2 * app.yardStep
        if dist < slowdownDist:
            desiredVx *= dist / slowdownDist
            desiredVy *= dist / slowdownDist

        steerX = desiredVx - self.dx
        steerY = desiredVy - self.dy
        steerMag = distance(0, 0, steerX, steerY)
        if steerMag > app.acceleration:
            steerX = (steerX / steerMag) * app.acceleration
            steerY = (steerY / steerMag) * app.acceleration
        self.dx += steerX
        self.dy += steerY

        speed = distance(0, 0, self.dx, self.dy)
        if speed > app.maxSpeed:
            self.dx = (self.dx / speed) * app.maxSpeed
            self.dy = (self.dy / speed) * app.maxSpeed

    def trackBall(self, app):
        self.targetX = app.ball.targetX
        self.targetY = app.ball.targetY
        self.goToPoint(app)
        self.movePlayer(app)

    def runWithBall(self, app):
        self.targetX = self.cx
        self.targetY = app.lineOfScrimmage - app.yardStep * GOAL_LINE_YARDS
        self.goToPoint(app)
        self.movePlayer(app)

    def block(self, app):
        defender = self.getNearestDefender(app)
        self.stopPlayer(app, defender)

    def movePlayer(self, app):
        self.cx += self.dx
        self.cy += self.dy
        self.cx = clampX(app, self.cx)

    def stopPlayer(self, app, target):
        playerVelo = app.maxSpeed
        targetVelo = (target.dx**2 + target.dy**2)**0.5
        veloRatio = targetVelo / playerVelo
        distanceToTarget = distance(self.cx, self.cy, target.cx, target.cy)
        _, targetAngle = getRadiusAndAngleToEndpoint(0, 0, target.dx, target.dy)
        _, angleToTarget = getRadiusAndAngleToEndpoint(target.cx, target.cy,
                                                       self.cx, self.cy)
        angleDifference = (targetAngle - angleToTarget) % 360
        sinTheta = math.sin(math.radians(angleDifference))
        pursuitAngle = (math.degrees(math.asin(sinTheta * veloRatio))) % 360
        interceptAngle = 180 - (angleDifference + pursuitAngle)
        sinInterceptAngle = math.sin(math.radians(interceptAngle))
        if -0.0015 < sinInterceptAngle < 0.0015:
            self.targetX, self.targetY = getRadiusEndpoint(self.cx, self.cy,
                                                           10 * app.yardStep,
                                                           targetAngle)
            self.goToPoint(app)
            self.movePlayer(app)
            return
        pursuitDistance = (distanceToTarget * sinTheta) / sinInterceptAngle
        pursuitHeading = (angleToTarget - 180) - pursuitAngle
        self.targetX, self.targetY = getRadiusEndpoint(self.cx, self.cy,
                                                       pursuitDistance,
                                                       pursuitHeading)
        self.goToPoint(app)
        self.movePlayer(app)

    def getNearestDefender(self, app):
        closestDist = None
        closest = None
        for player in app.dFormation.values():
            dist = distance(self.cx, self.cy, player.cx, player.cy)
            if closestDist is None or dist < closestDist:
                closest = player
                closestDist = dist
        return closest

    def registerTackle(self, app):
        app.playResult = 'Tackled'
        app.lastPlayResult = 'Tackled'
        yards = int((app.lineOfScrimmage - app.ball.carrier.cy) / app.yardStep)
        app.lastYardsRan = yards
        app.totalYards += yards
