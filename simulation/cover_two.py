from domain.defense import CoverPlayer
from domain.offense import SkillPlayer
from simulation.geometry import distance, getBallPlacement, pointInZone


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
