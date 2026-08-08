from cmu_graphics import *
from classes import *
from constants import *
from layout import applyWindowMetrics, midX, losY, placeButtons

def onAppStart(app):
    app.width = DESIGN_WIDTH
    app.height = DESIGN_HEIGHT
    app.prevWidth = app.width
    app.prevHeight = app.height
    app.yardLine = 0
    app.totalYards = 0
    app.score = 0
    app.stepsPerSecond = 40
    app.yardsPerSecond = 5
    applyWindowMetrics(app)
    app.maxBallVelo = 6
    app.mouseX = 0
    app.mouseY = 0
    app.isPassRush = True
    app.lastPlayResult = ''
    app.lastYardsRan = 0
    app.indexExport = 0
    app.coverageShell = 'Cover 1'
    app.animationTicks = 0
    app.pressedButton = None

    loadOffensiveRoutes(app)
    loadOffensiveFormations(app, firstTime=True)
    loadStats(app)
    loadFieldButtons(app)
    loadOffensiveMenuButtons(app)
    placeButtons(app)
    resetApp(app)

    app.isField = False
    app.isMainMenu = True
    app.isOffensiveMenu = False
    app.isMainMenuLabelHovering = False
    app.isWRMenu = True

def resetApp(app, isField=True):
    for player in app.oFormation.values():
        player.cx = player.startX
        player.cy = player.startY
        player.dx = 0
        player.dy = 0
        if isinstance(player, SkillPlayer):
            player.targetX = player.startX
            player.targetY = player.startY
    app.playIsActive = False
    app.exportButton.text = "Export Play"
    app.selectedPlayer = None
    app.isDefensiveMenu = False
    app.isOffensiveMenu = False
    app.isField = isField
    if not isField:
        app.isOffensiveMenu = True
    app.isRouteCombination = False
    app.isPaused = True
    app.steps = 0
    app.playResult = ''
    app.yardsRan = 0
    app.isPlayActive = False
    app.ballVelocity = 0
    app.throwing = False
    app.qbRun = True
    app.ballCarrier = None
    app.statsButton.isStats = False
    app.ball = Ball(app.oFormation['C'].cx, app.oFormation['C'].cy, app.oFormation['C'])
    if hasattr(app, 'coverageButton'):
        app.coverageButton.text = f"Coverage: {'C2' if app.coverageShell == 'Cover 2' else 'C1'}"
    loadDefensiveFormations(app)

def offensiveLine(app, rtDepth=13):
    return {
        'LT': Lineman(midX(app, -50), losY(app, 18)),
        'LG': Lineman(midX(app, -25), losY(app, 13)),
        'C': Lineman(midX(app, 0), losY(app, 13)),
        'RG': Lineman(midX(app, 25), losY(app, 13)),
        'RT': Lineman(midX(app, 50), losY(app, rtDepth)),
    }

def loadOffensiveFormations(app, firstTime=False):
    app.singleBack = {
        'WR1': WideReceiver(app, midX(app, -190), losY(app, 13), route=app.route),
        'WR2': WideReceiver(app, midX(app, -130), losY(app, 33), route=app.route),
        **offensiveLine(app, rtDepth=13),
        'TE': TightEnd(app, midX(app, 75), losY(app, 28), route=app.route),
        'WR3': WideReceiver(app, midX(app, 160), losY(app, 13), route=app.route),
        'QB': Quarterback(midX(app, 0), losY(app, 40)),
        'RB': RunningBack(app, midX(app, 0), losY(app, 70),
                          route=app.rbRouteList[2]),
    }
    app.shotgun = {
        'WR1': WideReceiver(app, midX(app, -190), losY(app, 13), route=app.route),
        'WR2': WideReceiver(app, midX(app, -130), losY(app, 33), route=app.route),
        **offensiveLine(app, rtDepth=13),
        'TE': TightEnd(app, midX(app, 75), losY(app, 28), route=app.route),
        'WR3': WideReceiver(app, midX(app, 160), losY(app, 13), route=app.route),
        'QB': Quarterback(midX(app, 0), losY(app, 70)),
        'RB': RunningBack(app, midX(app, 35), losY(app, 70),
                          route=app.rbRouteList[2]),
    }
    app.spread = {
        'WR1': WideReceiver(app, midX(app, -200), losY(app, 13), route=app.route),
        'WR2': WideReceiver(app, midX(app, -160), losY(app, 33), route=app.route),
        **offensiveLine(app, rtDepth=18),
        'WR3': WideReceiver(app, midX(app, 160), losY(app, 33), route=app.route),
        'WR4': WideReceiver(app, midX(app, 225), losY(app, 13), route=app.route),
        'QB': Quarterback(midX(app, 0), losY(app, 70)),
        'RB': RunningBack(app, midX(app, 35), losY(app, 70),
                          route=app.rbRouteList[2]),
    }
    app.bunch = {
        'WR1': WideReceiver(app, midX(app, -190), losY(app, 13), route=app.route),
        'WR2': WideReceiver(app, midX(app, -160), losY(app, 27), route=app.route),
        'WR3': WideReceiver(app, midX(app, -120), losY(app, 15), route=app.route),
        **offensiveLine(app, rtDepth=18),
        'WR4': WideReceiver(app, midX(app, 225), losY(app, 13), route=app.route),
        'QB': Quarterback(midX(app, 0), losY(app, 70)),
        'RB': RunningBack(app, midX(app, 35), losY(app, 70),
                          route=app.rbRouteList[2]),
    }
    app.custom = {
        'WR1': WideReceiver(app, midX(app, -210), losY(app, 40), route=app.route),
        'WR2': WideReceiver(app, midX(app, -160), losY(app, 40), route=app.route),
        **offensiveLine(app, rtDepth=18),
        'WR3': WideReceiver(app, midX(app, 160), losY(app, 40), route=app.route),
        'WR4': WideReceiver(app, midX(app, 210), losY(app, 40), route=app.route),
        'QB': Quarterback(midX(app, 0), losY(app, 70)),
        'RB': RunningBack(app, midX(app, 35), losY(app, 70),
                          route=app.rbRouteList[2]),
    }
    app.oFormation = app.singleBack
    app.ball = Ball(app.oFormation['C'].cx, app.oFormation['C'].cy,
                    app.oFormation['C'])

def loadOffensiveRoutes(app):
    # Routes are lists of (dx, dy) waypoints measured in yard-steps, relative to
    # the previous point. "Left/Right" names the field side the route is drawn for.
    crossingLeft = [(10, -10), (10, -10)]
    crossingRight = [(-10, -10), (-10, -10)]

    slantLeft = [(0, -5), (15, -15)]
    slantRight = [(0, -5), (-15, -15)]

    quickOutLeft = [(0, -3), (-8, 0)]
    quickOutRight = [(0, -3), (8, 0)]

    shallowDigLeft = [(0, -5), (15, 0)]
    shallowDigRight = [(0, -5), (-15, 0)]

    deepDigLeft = [(0, -10), (15, 0)]
    deepDigRight = [(0, -10), (-15, 0)]

    shallowOutLeft = [(0, -5), (-8, 0)]
    shallowOutRight = [(0, -5), (8, 0)]

    deepOutLeft = [(0, -10), (-8, 0)]
    deepOutRight = [(0, -10), (8, 0)]

    shallowHitchLeft = [(0, -8), (2, 2)]
    shallowHitchRight = [(0, -8), (-2, 2)]

    deepHitchLeft = [(0, -12), (2, 3)]
    deepHitchRight = [(0, -12), (-2, 3)]

    postLeft = [(0, -12), (5, -10)]
    postRight = [(0, -12), (-5, -10)]
    cornerLeft = [(0, -12), (-5, -10)]
    cornerRight = [(0, -12), (5, -10)]

    go = [(0, -11), (0, -11)]

    rbOutLeft = [(8, -4), (5, -2.5)]
    rbOutRight = [(-8, -4), (-5, -2.5)]
    rbZoneSit = [(0, -10), (0, 1)]

    app.wrRouteList = [crossingLeft, crossingRight, slantLeft, slantRight,
                       quickOutLeft, quickOutRight, shallowDigLeft,
                       shallowDigRight, deepDigLeft, deepDigRight,
                       shallowOutLeft, shallowOutRight, deepOutLeft,
                       deepOutRight, shallowHitchLeft, shallowHitchRight,
                       deepHitchLeft, deepHitchRight, postLeft, postRight,
                       cornerLeft, cornerRight, go]
    app.rbRouteList = [rbOutRight, rbOutLeft, rbZoneSit]
    app.route = go  # default route

def loadDefensiveFormations(app):
    loadZones(app)
    app.dFormation = initializeDefense(app)

def initializeDefense(app):
    if app.coverageShell == 'Cover 2':
        return initializeCoverTwo(app)
    return initializeCoverOne(app)

def initializeCoverOne(app):
    wrLocations = getPlayersOfType(app, WideReceiver)
    teLocations = getPlayersOfType(app, TightEnd)
    rbLocations = getPlayersOfType(app, RunningBack)
    coverOne = dict()
    assignCornersToReceivers(app, coverOne, wrLocations)
    numZoneLBs = assignLinebackers(app, coverOne, wrLocations,
                                   teLocations, rbLocations)
    spreadZoneLinebackers(app, coverOne, numZoneLBs + len(rbLocations))
    coverOne |= buildDLine(app)
    coverOne['S'] = Safety(app.width // 2, app.lineOfScrimmage - app.yardStep * 12,
                           0, 0, None, app.zones['middleDeep'])
    return coverOne

def assignCornersToReceivers(app, coverage, wrLocations):
    los = app.lineOfScrimmage
    for i, wr in enumerate(wrLocations):
        # Mirror the corner across the line of scrimmage from its receiver.
        coverage[f"CB{i+1}"] = CornerBack(wr.cx, los - (wr.cy - los), 0, 0, wr)

def assignLinebackers(app, coverage, wrLocations, teLocations, rbLocations):
    los = app.lineOfScrimmage
    numLBs = 6 - len(wrLocations)
    numCoverLBs = len(teLocations) + len(rbLocations)
    numZoneLBs = numLBs - numCoverLBs
    for i in range(numZoneLBs):
        coverage[f"LB{i+1}"] = LineBacker(0, 0, 0, 0, None,
                                          app.zones["middleIntermediate"])
    for i, rb in enumerate(rbLocations):
        coverage[f"LB{i+1+numZoneLBs}"] = LineBacker(rb.cx, los - (rb.cy - los + 10),
                                                     0, 0, rb)
    numRBs = len(rbLocations)
    for i, te in enumerate(teLocations):
        coverage[f"LB{i+1+numRBs+numZoneLBs}"] = LineBacker(
            te.cx, los - (te.cy - los + 10), 0, 0, te)
    return numZoneLBs

def spreadZoneLinebackers(app, coverage, totalLBs):
    # Evenly distribute the non-TE linebackers between the hash marks.
    los = app.lineOfScrimmage
    for i in range(totalLBs):
        linebacker = coverage[f"LB{i+1}"]
        xCoord = 2 * app.width // 5 + (i + 1) * (app.width // 5) // (totalLBs + 1)
        linebacker.cx, linebacker.cy = xCoord, los - app.yardStep * 4

def buildDLine(app):
    depth = app.lineOfScrimmage - DLINE_DEPTH_PX
    return {
        'DE1': DefensiveEnd(app.width * DEFENSIVE_END_LEFT_FRACTION, depth),
        'DE2': DefensiveEnd(app.width * DEFENSIVE_END_RIGHT_FRACTION, depth),
        'DT1': DefensiveTackle(app.width * DEFENSIVE_TACKLE_LEFT_FRACTION, depth),
        'DT2': DefensiveTackle(app.width * DEFENSIVE_TACKLE_RIGHT_FRACTION, depth),
    }

def initializeCoverTwo(app):
    allEligible = (getPlayersOfType(app, WideReceiver)
                   + getPlayersOfType(app, TightEnd)
                   + getPlayersOfType(app, RunningBack))
    allEligible.sort(key=lambda p: p.cx)
    coverTwo = dict()

    fieldMid = app.width // 2
    leftEligible = [p for p in allEligible if p.cx <= fieldMid]
    rightEligible = [p for p in allEligible if p.cx > fieldMid]
    leftOutside = leftEligible[0] if leftEligible else (allEligible[0] if allEligible else None)
    rightOutside = rightEligible[-1] if rightEligible else (allEligible[-1] if allEligible else None)

    leftCornerX = app.zones['leftFlat'].cx
    rightCornerX = app.zones['rightFlat'].cx
    if leftOutside is not None:
        leftCornerX = min(app.zones['leftFlat'].right, leftOutside.cx + app.yardStep * 0.35)
    if rightOutside is not None:
        rightCornerX = max(app.zones['rightFlat'].left, rightOutside.cx - app.yardStep * 0.35)

    coverTwo['CB1'] = CornerBack(leftCornerX,
                                 app.lineOfScrimmage - app.yardStep * 1.5,
                                 0, 0, leftOutside, app.zones['leftFlat'],
                                 shell='Cover 2', side='left', leverage='inside')
    coverTwo['CB2'] = CornerBack(rightCornerX,
                                 app.lineOfScrimmage - app.yardStep * 1.5,
                                 0, 0, rightOutside, app.zones['rightFlat'],
                                 shell='Cover 2', side='right', leverage='inside')

    coverTwo['LB1'] = LineBacker(app.zones['leftHook'].cx,
                                 app.lineOfScrimmage - app.yardStep * 4.2,
                                 0, 0, None, app.zones['leftHook'],
                                 shell='Cover 2', side='left')
    coverTwo['LB2'] = LineBacker(app.zones['middleHook'].cx,
                                 app.lineOfScrimmage - app.yardStep * 4.5,
                                 0, 0, None, app.zones['middleHook'],
                                 shell='Cover 2', side='middle')
    coverTwo['LB3'] = LineBacker(app.zones['rightHook'].cx,
                                 app.lineOfScrimmage - app.yardStep * 4.2,
                                 0, 0, None, app.zones['rightHook'],
                                 shell='Cover 2', side='right')

    coverTwo['S1'] = Safety(app.zones['leftDeepHalf'].cx,
                            app.lineOfScrimmage - app.yardStep * 11.5,
                            0, 0, None, app.zones['leftDeepHalf'],
                            shell='Cover 2', side='left')
    coverTwo['S2'] = Safety(app.zones['rightDeepHalf'].cx,
                            app.lineOfScrimmage - app.yardStep * 11.5,
                            0, 0, None, app.zones['rightDeepHalf'],
                            shell='Cover 2', side='right')

    coverTwo |= buildDLine(app)
    return coverTwo

def loadZones(app):
    fieldLeft = app.sideLineOffset + BOUNDARY_OFFSET
    fieldRight = app.width - app.sideLineOffset - BOUNDARY_OFFSET
    fieldWidth = fieldRight - fieldLeft
    fieldMid = (fieldLeft + fieldRight) / 2
    los = app.lineOfScrimmage
    yard = app.yardStep
    zones = dict()

    zones['middleDeep'] = Zone(fieldWidth / 5 + fieldLeft,
                               fieldRight - fieldWidth / 5, 0,
                               los - 10 * yard,
                               fieldMid,
                               los - 12 * yard)

    zones['middleIntermediate'] = Zone(fieldWidth // 3 + fieldLeft,
                                       fieldRight - fieldWidth // 3,
                                       los - 9 * yard,
                                       los - 3 * yard)

    zones['leftDeepHalf'] = Zone(fieldLeft, fieldMid, 0,
                                 los - 8 * yard,
                                 fieldLeft + fieldWidth * 0.25,
                                 los - 12 * yard)
    zones['rightDeepHalf'] = Zone(fieldMid, fieldRight, 0,
                                  los - 8 * yard,
                                  fieldLeft + fieldWidth * 0.75,
                                  los - 12 * yard)
    zones['leftFlat'] = Zone(fieldLeft,
                             fieldLeft + fieldWidth * 0.28,
                             los - 8 * yard,
                             los + 2 * yard,
                             fieldLeft + fieldWidth * 0.14,
                             los - 3.5 * yard)
    zones['rightFlat'] = Zone(fieldRight - fieldWidth * 0.28,
                              fieldRight,
                              los - 8 * yard,
                              los + 2 * yard,
                              fieldLeft + fieldWidth * 0.86,
                              los - 3.5 * yard)
    zones['leftHook'] = Zone(fieldLeft + fieldWidth * 0.18,
                             fieldMid,
                             los - 10 * yard,
                             los - 2 * yard,
                             fieldLeft + fieldWidth * 0.36,
                             los - 6 * yard)
    zones['middleHook'] = Zone(fieldLeft + fieldWidth * 0.36,
                               fieldRight - fieldWidth * 0.36,
                               los - 11 * yard,
                               los - 3 * yard,
                               fieldMid,
                               los - 6.5 * yard)
    zones['rightHook'] = Zone(fieldMid,
                              fieldRight - fieldWidth * 0.18,
                              los - 10 * yard,
                              los - 2 * yard,
                              fieldLeft + fieldWidth * 0.64,
                              los - 6 * yard)
    app.zones = zones

def loadOffensiveMenuButtons(app):
    app.offensiveFormationButtons = [
        FormationButton(95, 80, 130, 65, "Single Back", app.singleBack),
        FormationButton(95, 170, 130, 65, "Shotgun", app.shotgun),
        FormationButton(95, 260, 130, 65, "Spread", app.spread),
        FormationButton(95, 350, 130, 65, "Bunch", app.bunch),
        FormationButton(95, 440, 130, 65, "Custom", app.custom),
    ]

    app.menuInstructionsButton = InstructionButton(105, 538, 175, 50,
                                                   "Toggle Instructions")
    app.fieldInstructionsButton = InstructionButton(app.width - 100, 50, 180, 40,
                                                    'Toggle Instructions')

    # Each route button holds the [leftSide, rightSide] variants sliced from
    # the master WR route list.
    app.offensiveWRRouteButtons = [
        RouteButton(app.width - 95, 50, 130, 35, "Crossing", app.wrRouteList[0:2]),
        RouteButton(app.width - 95, 110, 130, 35, "Slant", app.wrRouteList[2:4]),
        RouteButton(app.width - 95, 170, 130, 35, "Quick Out", app.wrRouteList[4:6]),
        RouteButton(app.width - 95, 230, 130, 35, "Shallow Dig", app.wrRouteList[6:8]),
        RouteButton(app.width - 95, 290, 130, 35, "Deep Dig", app.wrRouteList[8:10]),
        RouteButton(app.width - 95, 350, 130, 35, "Shallow Out", app.wrRouteList[10:12]),
        RouteButton(app.width - 95, 410, 130, 35, "Deep Out", app.wrRouteList[12:14]),
        RouteButton(app.width - 95, 470, 130, 35, "Shallow Hitch", app.wrRouteList[14:16]),
        RouteButton(app.width - 95, 530, 130, 35, "Deep Hitch", app.wrRouteList[16:18]),
        RouteButton(app.width - 95, 590, 130, 35, "Post", app.wrRouteList[18:20]),
        RouteButton(app.width - 95, 650, 130, 35, "Corner", app.wrRouteList[20:22]),
        RouteButton(app.width - 95, 710, 130, 35, "Go",
                    [app.wrRouteList[22], app.wrRouteList[22]]),
    ]
    app.startGameButton = StartButton(app.width // 2, 650, 300, 150, "Start Game")

    app.offensiveRBRouteButtons = [
        RouteButton(app.width - 95, 50, 130, 35, "RB Out", app.rbRouteList[0:2]),
        RouteButton(app.width - 95, 110, 130, 35, "RB Zone Sit",
                    [app.rbRouteList[2], app.rbRouteList[2]]),
    ]
    app.importButton = ExportImportButton(app.sideLineOffset // 2,
                                          app.height - 120, 150, 50, "Import Play", dict())
    app.exportButton = ExportImportButton(app.sideLineOffset // 2,
                                          app.height - 45, 150, 50, "Export Play", dict())

def loadFieldButtons(app):
    resetButton = Button(app.sideLineOffset // 2, 40, 100, 50, "Reset")
    menuButton = Button(app.sideLineOffset // 2, 110, 100, 50, "Menu")
    app.coverageButton = Button(app.sideLineOffset // 2, 500, 150, 50, "Coverage: C1")
    app.fieldButtons = [resetButton, menuButton]

def getPlayersOfType(app, playerType):
    return [player for player in app.oFormation.values()
            if isinstance(player, playerType)]

def loadStats(app):
    app.numCompletions = 0
    app.attempts = 0
    app.totalYards = 0
    app.ints = 0
    app.qbRun = True
    app.statsButton = StatsButton(app.width - 100, 130, 130, 40, 'Stats')
