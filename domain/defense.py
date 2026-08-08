import random
from constants import (DEFENDER_SIDELINE_CLAMP, MAN_BACKPEDAL_DEPTH_YARDS,
                       MAN_JAM_YARDS, TACKLE_RANGE)
from domain.offense import SkillPlayer
from domain.player import Player
from simulation.geometry import (clamp, distance, getBallPlacement, leftHashX,
                                 pointInZone, rightHashX)


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
