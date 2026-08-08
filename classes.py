from cmu_graphics import *
from constants import *
import math
import random

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

class Zone:
    def __init__(self, left, right, top, bottom, cx=None, cy=None):
        self.cx = cx if cx is not None else (left + right) / 2
        self.cy = cy if cy is not None else (top + bottom) / 2
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

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
        # Ease off as the player closes on the target so it doesn't overshoot.
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
        # Steer toward the intercept point of a moving target using the law of sines.
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
        # Routes store the player center; draw from the circle's top apex.
        x, y = self.route[index]
        resolved = index if index >= 0 else len(self.route) + index
        if resolved == 0:
            y -= PLAYER_DRAW_RADIUS
        return x, y + cameraShift

    def drawRoute(self, app, color=ROUTE_COLOR_DEFAULT):
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

class CoverPlayer(Player):
    def __init__(self, cx, cy, dx=0, dy=0, man=None, zone=None,
                 shell='Cover 1', side='middle', leverage='balanced'):
        super().__init__(cx, cy, dx, dy)
        self.zone = zone
        self.man = man
        self.targetX = cx
        self.targetY = cy
        self.shell = shell
        self.side = side
        self.leverage = leverage
        self.helpTarget = None
        self.matchTarget = None
        self.callout = ''

    def stepTowardTarget(self, app):
        self.goToPoint(app)
        self.cx += self.dx
        self.cy += self.dy
        self.cx = clamp(self.cx, DEFENDER_SIDELINE_CLAMP,
                        app.width - DEFENDER_SIDELINE_CLAMP)

    def guardMan(self, app):
        if self.shell == 'Cover 2':
            self.playZone(app)
            return
        if self.man is None:
            if self.zone is not None:
                self.playZone(app)
            return
        self.targetX, self.targetY = getBallPlacement(self.man, app)
        if app.yardsRan < MAN_JAM_YARDS:
            cushion = app.lineOfScrimmage - app.yardStep * MAN_BACKPEDAL_DEPTH_YARDS
            self.targetY = min(cushion, self.targetY)
        self.stepTowardTarget(app)

    def playZone(self, app):
        if self.zone is None:
            return
        self.targetX, self.targetY = self.resolveZoneTarget(app)
        self.targetX = clamp(self.targetX, self.zone.left, self.zone.right)
        self.targetY = clamp(self.targetY, self.zone.top, self.zone.bottom)
        self.stepTowardTarget(app)

    def resolveZoneTarget(self, app):
        threat = self.helpTarget
        if threat is None and self.matchTarget is not None:
            ballX, ballY = getBallPlacement(self.matchTarget, app)
            if pointInZone(ballX, ballY, self.zone):
                threat = self.matchTarget
            else:
                self.matchTarget = None
                self.callout = 'Pass off!'
        if threat is None:
            threat = self.claimBestThreatInZone(app)
        if threat is not None:
            return getBallPlacement(threat, app)
        return self.zone.cx, self.zone.cy

    def claimBestThreatInZone(self, app):
        candidates = []
        for player in app.oFormation.values():
            if not isinstance(player, SkillPlayer):
                continue
            ballX, ballY = getBallPlacement(player, app)
            if pointInZone(ballX, ballY, self.zone):
                depthScore = app.lineOfScrimmage - ballY
                candidates.append((depthScore, player))
        if not candidates:
            return None
        candidates.sort(reverse=True, key=lambda t: t[0])
        bestThreat = candidates[0][1]
        self.matchTarget = bestThreat
        if len(candidates) > 1 and self.shell == 'Cover 2':
            self.callout = 'Overload!'
        return bestThreat

    def checkTackle(self, app):
        ballCarrier = app.ball.carrier
        if distance(self.cx, self.cy, ballCarrier.cx, ballCarrier.cy) > TACKLE_RANGE:
            return
        self.registerTackle(app)
        if app.qbRun:
            app.lastPlayResult += ' (QB Run)'
        else:
            app.numCompletions += 1
            app.attempts += 1

class CornerBack(CoverPlayer):
    def __init__(self, cx, cy, dx=0, dy=0, man=None, zone=None,
                 shell='Cover 1', side='middle', leverage='balanced'):
        super().__init__(cx, cy, dx, dy, man, zone, shell, side, leverage)

    def guardMan(self, app):
        if self.shell != 'Cover 2':
            super().guardMan(app)
            return
        self.playCoverTwoTechnique(app)

    def playCoverTwoTechnique(self, app):
        if self.zone is None:
            super().guardMan(app)
            return
        primaryReceiver = self.man or self.findPrimaryReceiver(app)
        if primaryReceiver is None:
            self.playZone(app)
            return
        self.man = primaryReceiver
        insideLever = 1 if self.side == 'left' else -1
        flatThreat = self.findFlatThreat(app)
        if self.shouldJam(app, flatThreat, primaryReceiver):
            self.jamReceiver(app, primaryReceiver, insideLever)
        else:
            self.driveOnThreat(app, flatThreat, primaryReceiver, insideLever)
        self.goToPoint(app)
        self.movePlayer(app)

    def findPrimaryReceiver(self, app):
        bestDist = float('inf')
        primaryReceiver = None
        for player in app.oFormation.values():
            if not isinstance(player, SkillPlayer):
                continue
            onLeft = player.cx <= app.width // 2
            if self.side == 'left' and not onLeft:
                continue
            if self.side == 'right' and onLeft:
                continue
            dist = distance(self.cx, self.cy, player.cx, player.cy)
            if dist < bestDist:
                bestDist = dist
                primaryReceiver = player
        return primaryReceiver

    def findFlatThreat(self, app):
        # In Cover 2, corners drive any flat threat entering their zone,
        # not just the receiver they initially jammed.
        flatThreat = None
        flatThreatDist = float('inf')
        if self.helpTarget is not None:
            helpX, helpY = getBallPlacement(self.helpTarget, app)
            if pointInZone(helpX, helpY, self.zone):
                flatThreat = self.helpTarget
                flatThreatDist = distance(self.cx, self.cy, helpX, helpY)
        for player in app.oFormation.values():
            if not isinstance(player, SkillPlayer):
                continue
            threatX, threatY = getBallPlacement(player, app)
            if not pointInZone(threatX, threatY, self.zone):
                continue
            dist = distance(self.cx, self.cy, threatX, threatY)
            if dist < flatThreatDist:
                flatThreatDist = dist
                flatThreat = player
        return flatThreat

    def shouldJam(self, app, flatThreat, primaryReceiver):
        return (flatThreat is None and app.yardsRan <= 2.6 and
                primaryReceiver.cy >= app.lineOfScrimmage - app.yardStep)

    def jamReceiver(self, app, primaryReceiver, insideLever):
        self.targetX = primaryReceiver.cx + insideLever * app.yardStep * 0.45
        self.targetY = min(primaryReceiver.cy - app.yardStep * 0.3,
                           app.lineOfScrimmage - app.yardStep * 0.45)
        if distance(self.cx, self.cy,
                    primaryReceiver.cx, primaryReceiver.cy) <= 14:
            primaryReceiver.dx *= 0.8
            primaryReceiver.targetX += insideLever * app.yardStep * 0.35
            self.callout = 'Force inside!'

    def driveOnThreat(self, app, flatThreat, primaryReceiver, insideLever):
        targetReceiver = flatThreat if flatThreat is not None else primaryReceiver
        ballX, ballY = getBallPlacement(targetReceiver, app)
        if pointInZone(ballX, ballY, self.zone):
            self.targetX = ballX + insideLever * app.yardStep * 0.3
            self.targetY = ballY
            if targetReceiver is not primaryReceiver:
                self.callout = 'Drive flat!'
        else:
            self.targetX = self.zone.cx + insideLever * app.yardStep * 0.4
            self.targetY = self.zone.cy
        self.targetX = clamp(self.targetX, self.zone.left, self.zone.right)
        self.targetY = clamp(self.targetY, self.zone.top, self.zone.bottom)
        if primaryReceiver.cy < app.lineOfScrimmage - 6 * app.yardStep:
            self.callout = 'Carry + pass!'

class LineBacker(CoverPlayer):
    def __init__(self, cx, cy, dx=0, dy=0, man=None, zone=None,
                 shell='Cover 1', side='middle', leverage='balanced'):
        super().__init__(cx, cy, dx, dy, man, zone, shell, side, leverage)

class PassRusher(Player):
    def __init__(self, cx, cy, dx=0, dy=0):
        super().__init__(cx, cy, dx, dy)
        self.rushingQB = False

    def rushQB(self, app):
        if not app.isPassRush:
            self.targetX = self.cx
            self.targetY = self.cy
            return
        qb = app.oFormation['QB']
        if self.rushingQB:
            self.targetX = qb.cx
            self.targetY = qb.cy
        else:
            self.holdContain(app, qb)
        self.goToPoint(app)
        self.movePlayer(app)

    def holdContain(self, app, qb):
        # Loiter near the hash marks and only commit to the QB occasionally,
        # giving the illusion of a live pass rush.
        hashOffset = 8
        closestRusher = self.nearestRusherToQB(app, qb)
        if qb.cx < leftHashX(app) and closestRusher == self:
            self.rushingQB = True
        elif qb.cx > rightHashX(app) and closestRusher == self:
            self.rushingQB = True
        elif self.cx < leftHashX(app) + hashOffset:
            self.targetX = leftHashX(app) + hashOffset
        elif self.cx > rightHashX(app) - hashOffset:
            self.targetX = rightHashX(app) - hashOffset
        else:
            self.targetX = self.cx
        self.targetY = app.lineOfScrimmage + app.yardStep
        if random.randrange(0, app.stepsPerSecond * 40) == 1 and app.yardsRan > 3:
            self.rushingQB = True

    def nearestRusherToQB(self, app, qb):
        closestRusher = None
        closestDist = float('inf')
        for player in app.dFormation.values():
            dist = distance(player.cx, player.cy, qb.cx, qb.cy)
            if dist < closestDist or closestRusher is None:
                closestRusher = player
                closestDist = dist
        return closestRusher

    def checkTackle(self, app):
        ballCarrier = app.ball.carrier
        if distance(self.cx, self.cy, ballCarrier.cx, ballCarrier.cy) > TACKLE_RANGE:
            return
        self.registerTackle(app)
        app.numCompletions = 0
        app.attempts = 0

class DefensiveTackle(PassRusher):
    def __init__(self, cx, cy, dx=0, dy=0):
        super().__init__(cx, cy, dx, dy)

class DefensiveEnd(PassRusher):
    def __init__(self, cx, cy, dx=0, dy=0):
        super().__init__(cx, cy, dx, dy)

class Safety(CoverPlayer):
    def __init__(self, cx, cy, dx=0, dy=0, man=None, zone=None,
                 shell='Cover 1', side='middle', leverage='balanced'):
        super().__init__(cx, cy, dx, dy, man, zone, shell, side, leverage)

class Button:
    def __init__(self, cx, cy, w, h, text, fillColor=BUTTON_GREEN, labelSize=18):
        self.cx = cx
        self.cy = cy
        self.w = w
        self.h = h
        self.text = text
        self.fillColor = fillColor
        self.labelSize = labelSize
        self.hovered = False
        self.pressed = False
        self.enabled = True

    def contains(self, mx, my):
        return ((self.cx - self.w // 2) <= mx <= (self.cx + self.w // 2) and
                (self.cy - self.h // 2) <= my <= (self.cy + self.h / 2))

    def isClicked(self, mx, my):
        return self.enabled and self.contains(mx, my)

    def updateHover(self, mx, my):
        self.hovered = self.enabled and self.contains(mx, my)

    def drawnCenter(self):
        # Pressed buttons sink toward their outline; every other visual keys off this point.
        if self.pressed:
            return self.cx + BUTTON_PRESS_SHIFT, self.cy + BUTTON_PRESS_SHIFT
        return self.cx, self.cy

    def draw(self):
        cx, cy = self.drawnCenter()
        self.drawOutline(cx, cy)
        drawRect(cx, cy, self.w, self.h, fill=self.fillColor, align='center')
        self.drawStateOverlay(cx, cy)
        self.drawContent(cx, cy)

    def drawOutline(self, cx, cy):
        if self.pressed:
            return
        drawRect(cx, cy, self.w + BUTTON_OUTLINE_PAD_X, self.h + BUTTON_OUTLINE_PAD_Y,
                 fill=BUTTON_OUTLINE_COLOR, align='center')

    def drawStateOverlay(self, cx, cy):
        if not self.enabled:
            self.drawOverlay(cx, cy, DISABLED_OVERLAY_COLOR, DISABLED_OVERLAY_OPACITY)
        elif self.pressed:
            self.drawOverlay(cx, cy, PRESS_OVERLAY_COLOR, PRESS_OVERLAY_OPACITY)
        elif self.hovered:
            self.drawOverlay(cx, cy, HOVER_OVERLAY_COLOR, HOVER_OVERLAY_OPACITY)

    def drawOverlay(self, cx, cy, color, opacity):
        drawRect(cx, cy, self.w, self.h, fill=color, opacity=opacity, align='center')

    def labelColor(self):
        return ENABLED_LABEL_COLOR if self.enabled else DISABLED_LABEL_COLOR

    def drawContent(self, cx, cy):
        drawLabel(self.text, cx, cy, size=self.labelSize,
                  bold=self.hovered and self.enabled, fill=self.labelColor(),
                  align='center')

class FormationButton(Button):
    def __init__(self, cx, cy, w, h, text, formation):
        super().__init__(cx, cy, w, h, text)
        self.formation = formation

    def resetFormation(self, app, formation):
        self.formation = formation

class RouteButton(Button):
    def __init__(self, cx, cy, w, h, text, routes):
        super().__init__(cx, cy, w, h, text, labelSize=ROUTE_LABEL_SIZE)
        self.leftRoute = routes[0]
        self.rightRoute = routes[1]
        self.iconRoute = routes[1]
        self.active = False

    def drawContent(self, cx, cy):
        iconCenterX = cx - self.w // 2 + ROUTE_ICON_MARGIN
        drawRouteIcon(iconCenterX, cy, ROUTE_ICON_BOX, self.iconRoute, self.labelColor())
        drawLabel(self.text, cx + ROUTE_LABEL_SHIFT, cy, size=self.labelSize,
                  bold=self.hovered and self.enabled, fill=self.labelColor(),
                  align='center')
        if self.active:
            drawRect(cx, cy, self.w, self.h, fill=None,
                     border=ROUTE_ACTIVE_BORDER, borderWidth=ROUTE_ACTIVE_BORDER_WIDTH,
                     align='center')

class InstructionButton(Button):
    def __init__(self, cx, cy, w, h, text):
        super().__init__(cx, cy, w, h, text, fillColor=INSTRUCTION_BUTTON_GREEN)
        self.isInstructions = False

class StartButton(Button):
    def __init__(self, cx, cy, w, h, text):
        super().__init__(cx, cy, w, h, text,
                         fillColor=START_BUTTON_RED, labelSize=48)

class ExportImportButton(Button):
    def __init__(self, cx, cy, w, h, text, data):
        super().__init__(cx, cy, w, h, text, fillColor=EXPORT_IMPORT_BUTTON_GREEN)
        self.data = data

class StatsButton(Button):
    def __init__(self, cx, cy, w, h, text):
        super().__init__(cx, cy, w, h, text, fillColor=STATS_BUTTON_GREEN)
        self.isStats = False

def visibleButtons(app):
    # The single source of truth for which buttons the active screen shows, used
    # for hover, press feedback, and hit-testing so those never drift apart.
    if getattr(app, 'isOffensiveMenu', False):
        routeButtons = (app.offensiveWRRouteButtons if app.isWRMenu
                        else app.offensiveRBRouteButtons)
        return (list(app.offensiveFormationButtons) + list(routeButtons)
                + [app.startGameButton, app.importButton, app.exportButton,
                   app.menuInstructionsButton])
    if getattr(app, 'isField', False):
        return (list(app.fieldButtons) + [app.coverageButton, app.exportButton,
                app.fieldInstructionsButton, app.statsButton])
    return []

def panelCloseCenter(panelCx, panelCy, panelW, panelH):
    return (panelCx + panelW // 2 - PANEL_CLOSE_INSET,
            panelCy - panelH // 2 + PANEL_CLOSE_INSET)

def panelCloseContains(mx, my, closeCx, closeCy):
    half = PANEL_CLOSE_HALF
    return (closeCx - half <= mx <= closeCx + half and
            closeCy - half <= my <= closeCy + half)

def routeWaypoints(route):
    # Convert a route's relative (dx, dy) steps into absolute points anchored at
    # the origin, matching how translateRoute accumulates them on the field.
    points = [(0.0, 0.0)]
    x = y = 0.0
    for dx, dy in route:
        x += dx
        y += dy
        points.append((x, y))
    return points

def drawRouteIcon(centerX, centerY, box, route, color):
    points = fitRouteToBox(routeWaypoints(route), centerX, centerY, box)
    for i in range(1, len(points)):
        drawLine(*points[i - 1], *points[i], fill=color, lineWidth=2)
    drawRouteArrowhead(points[-2], points[-1], color)
    startX, startY = points[0]
    drawCircle(startX, startY, ROUTE_ICON_START_DOT_RADIUS, fill=color)

def drawRouteArrowhead(fromPoint, toPoint, color):
    fromX, fromY = fromPoint
    toX, toY = toPoint
    shaftAngle = math.atan2(toY - fromY, toX - fromX)
    barbLength = routeArrowBarbLength(fromPoint, toPoint)
    for spread in (ROUTE_ICON_ARROW_SPREAD, -ROUTE_ICON_ARROW_SPREAD):
        barbAngle = shaftAngle + math.pi + spread
        barbX = toX + barbLength * math.cos(barbAngle)
        barbY = toY + barbLength * math.sin(barbAngle)
        drawLine(toX, toY, barbX, barbY, fill=color, lineWidth=2)

def routeArrowBarbLength(fromPoint, toPoint):
    # Keep the arrowhead from overwhelming a short final segment (e.g. a hitch's
    # tight comeback) by capping it to a fraction of that segment's length.
    segmentLength = distance(*fromPoint, *toPoint)
    return min(ROUTE_ICON_ARROW_SIZE, segmentLength * ROUTE_ICON_ARROW_MAX_SEGMENT_RATIO)

def fitRouteToBox(points, centerX, centerY, box):
    xs = [x for x, _ in points]
    ys = [y for _, y in points]
    scale = (box - 6) / max(max(xs) - min(xs), max(ys) - min(ys), 1e-6)
    midX = (min(xs) + max(xs)) / 2
    midY = (min(ys) + max(ys)) / 2
    return [(centerX + (x - midX) * scale, centerY + (y - midY) * scale)
            for x, y in points]

def moveOffense(app):
    for player in app.oFormation.values():
        updateOffensivePlayer(app, player)

def updateOffensivePlayer(app, player):
    if player == app.ball.carrier and not isinstance(player, Lineman):
        player.goToPoint(app)
        player.movePlayer(app)
    elif isinstance(player, Quarterback):
        player.targetX = player.cx
        player.targetY = app.lineOfScrimmage + app.yardStep * QB_DROPBACK_YARDS
        player.goToPoint(app)
        player.cx += player.dx
        player.cy += player.dy
    elif isinstance(player, SkillPlayer):
        updateSkillPlayer(app, player)

def updateSkillPlayer(app, player):
    ball = app.ball
    if ball.targetX is not None and ball.targetY is not None and not ball.beingSnapped:
        player.trackBall(app)
    elif ball.carrier == app.oFormation['QB']:
        player.runRoute(app)
    elif player == ball.carrier:
        player.runWithBall(app)
    else:
        player.block(app)

def moveDefense(app):
    if app.coverageShell == 'Cover 2':
        coordinateCoverTwo(app)
    for player in app.dFormation.values():
        if isinstance(player, CoverPlayer):
            updateCoverPlayer(app, player)
        elif isinstance(player, PassRusher):
            player.rushQB(app)
            if app.ball.carrier == app.oFormation['QB']:
                player.checkTackle(app)

def updateCoverPlayer(app, player):
    ball = app.ball
    qb = app.oFormation['QB']
    if ball.targetX is not None and ball.targetY is not None and not ball.beingSnapped:
        player.trackBall(app)
    elif (ball.carrier == qb and qb.cy > app.lineOfScrimmage) or ball.beingSnapped:
        player.guardMan(app)
    else:
        player.stopPlayer(app, ball.carrier)
        player.checkTackle(app)

##############################
### Moving Players Helpers ###
##############################

def getBallPlacement(target, app):
    # Predict where to lead the target so the ball and receiver meet, using the
    # law of sines with the QB as the throwing origin.
    qb = None
    for player in app.oFormation.values():
        if isinstance(player, Quarterback):
            qb = player
            break
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
    # Lead the target slightly so the defender/receiver arrives in front of it.
    ballDistanceToQb = distance(qb.cx, qb.cy, ballX, ballY)
    leadX = (qb.cx - ballX) / ballDistanceToQb
    leadY = (qb.cy - ballY) / ballDistanceToQb
    correctedX = ballX + leadX * app.yardStep * 0.5
    correctedY = ballY + leadY * app.yardStep * 0.5
    return correctedX, correctedY

def getRadiusEndpoint(cx, cy, r, theta):
    return (cx + r * math.cos(math.radians(theta)),
            cy - r * math.sin(math.radians(theta)))

def getRadiusAndAngleToEndpoint(cx, cy, targetX, targetY):
    radius = distance(cx, cy, targetX, targetY)
    angle = math.degrees(math.atan2(cy - targetY, targetX - cx)) % 360
    return (radius, angle)

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

def coordinateCoverTwo(app):
    zoneDefenders = collectZoneDefenders(app)
    threatMap = mapThreatsToDefenders(app, zoneDefenders)
    assignZoneHelp(zoneDefenders, threatMap)

def collectZoneDefenders(app):
    zoneDefenders = []
    for player in app.dFormation.values():
        if isinstance(player, CoverPlayer) and player.zone is not None:
            zoneDefenders.append(player)
            player.helpTarget = None
            player.callout = ''
            if player.matchTarget is not None:
                ballX, ballY = getBallPlacement(player.matchTarget, app)
                if not pointInZone(ballX, ballY, player.zone):
                    player.matchTarget = None
                    player.callout = 'Pass off!'
    return zoneDefenders

def mapThreatsToDefenders(app, zoneDefenders):
    threatMap = dict()
    for defender in zoneDefenders:
        threats = []
        for offensivePlayer in app.oFormation.values():
            if not isinstance(offensivePlayer, SkillPlayer):
                continue
            ballX, ballY = getBallPlacement(offensivePlayer, app)
            if pointInZone(ballX, ballY, defender.zone):
                depth = app.lineOfScrimmage - ballY
                threats.append((depth, offensivePlayer, ballX, ballY))
        threats.sort(reverse=True, key=lambda t: t[0])
        threatMap[defender] = threats
    return threatMap

def assignZoneHelp(zoneDefenders, threatMap):
    for defender in zoneDefenders:
        threats = threatMap[defender]
        if len(threats) <= 1:
            continue
        _, extraThreat, extraX, extraY = threats[1]
        helper = nearestHelper(zoneDefenders, defender, extraX, extraY)
        if helper is not None and helper.helpTarget is None:
            helper.helpTarget = extraThreat
            defender.callout = 'Need help!'
            helper.callout = 'I got #2'

def nearestHelper(zoneDefenders, defender, threatX, threatY):
    helper = None
    helperDist = float('inf')
    for teammate in zoneDefenders:
        if teammate == defender:
            continue
        if not pointInZone(threatX, threatY, teammate.zone):
            continue
        dist = distance(teammate.cx, teammate.cy, threatX, threatY)
        if dist < helperDist:
            helperDist = dist
            helper = teammate
    return helper

def handleCollisions(app):
    players = list(app.oFormation.values()) + list(app.dFormation.values())
    for i in range(len(players)):
        for j in range(i + 1, len(players)):
            resolveCollision(players[i], players[j])

def resolveCollision(p1, p2):
    xDiff = p2.cx - p1.cx
    yDiff = p2.cy - p1.cy
    dist = distance(p1.cx, p1.cy, p2.cx, p2.cy)
    if dist == 0:
        xDiff = 0.01
        yDiff = 0.01
        dist = distance(0, 0, xDiff, yDiff)
    overlap = 2 * PLAYER_COLLISION_RADIUS - dist
    if overlap > COLLISION_OVERLAP_THRESHOLD:
        nx, ny = xDiff / dist, yDiff / dist
        p1.cx -= nx * COLLISION_PUSH
        p1.cy -= ny * COLLISION_PUSH
        p2.cx += nx * COLLISION_PUSH
        p2.cy += ny * COLLISION_PUSH
