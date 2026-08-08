import math
from constants import BOUNDARY_OFFSET


def distance(x1, y1, x2, y2):
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5


def clamp(value, low, high):
    return max(low, min(value, high))


def clampX(app, x):
    left = BOUNDARY_OFFSET + app.sideLineOffset
    right = app.width - BOUNDARY_OFFSET - app.sideLineOffset
    return clamp(x, left, right)


def leftHashX(app):
    return 3 * app.width // 7


def rightHashX(app):
    return 4 * app.width // 7


def pointInZone(x, y, zone):
    return zone.left <= x <= zone.right and zone.top <= y <= zone.bottom


def getRadiusEndpoint(cx, cy, r, theta):
    return (cx + r * math.cos(math.radians(theta)),
            cy - r * math.sin(math.radians(theta)))


def getRadiusAndAngleToEndpoint(cx, cy, targetX, targetY):
    radius = distance(cx, cy, targetX, targetY)
    angle = math.degrees(math.atan2(cy - targetY, targetX - cx)) % 360
    return (radius, angle)


def getBallPlacement(target, app):
    qb = app.oFormation['QB']
    ballVelo = app.velocity * 3
    playerVelo = (target.dx**2 + target.dy**2)**0.5
    veloRatio = playerVelo / ballVelo
    distanceToTarget = distance(qb.cx, qb.cy, target.cx, target.cy)
    _, targetAngle = getRadiusAndAngleToEndpoint(0, 0, target.dx, target.dy)
    _, angleToTarget = getRadiusAndAngleToEndpoint(target.cx, target.cy,
                                                   qb.cx, qb.cy)
    angleDifference = (targetAngle - angleToTarget) % 360
    sinTheta = math.sin(math.radians(angleDifference))
    leadAngle = math.degrees(math.asin(sinTheta * veloRatio)) % 360
    ballAngle = 180 - (angleDifference + leadAngle)
    sinBallAngle = math.sin(math.radians(ballAngle))
    if sinBallAngle == 0:
        sinBallAngle = 0.0001
    throwDistance = (distanceToTarget * sinTheta) / sinBallAngle
    throwAngle = (angleToTarget - 180) - leadAngle

    ballX, ballY = getRadiusEndpoint(qb.cx, qb.cy, throwDistance, throwAngle)
    if qb.cx == ballX and qb.cy == ballY:
        return ballX, ballY
    ballDistanceToQb = distance(qb.cx, qb.cy, ballX, ballY)
    leadX = (qb.cx - ballX) / ballDistanceToQb
    leadY = (qb.cy - ballY) / ballDistanceToQb
    correctedX = ballX + leadX * app.yardStep * 0.5
    correctedY = ballY + leadY * app.yardStep * 0.5
    return correctedX, correctedY
