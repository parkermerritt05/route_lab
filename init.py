from cmu_graphics import *
from classes import *

def onAppStart(app):
    app.width = 1000
    app.height = 750
    app.sideLineOffset = 194
    app.yardLine = 0
    app.totalYards = 0
    app.score = 0
    app.yardStep = 20
    app.lineOfScrimmage = app.height-(app.yardStep*14)
    app.stepsPerSecond = 40
    app.yardsPerSecond = 5
    app.velocity = app.yardsPerSecond * (app.yardStep/app.stepsPerSecond)
    app.maxSpeed = app.velocity
    app.acceleration = 0.2 * app.yardStep/app.stepsPerSecond
    app.fieldSides = [30, app.width-30]
    app.maxBallVelo = 6
    app.mouseX = 0
    app.mouseY = 0
    app.isPashRush = True
    app.lastPlayResult = ''
    app.lastYardsRan = 0
    app.indexExport = 0
    app.coverageShell = 'Cover 1'

    loadOffensiveRoutes(app)
    loadOffensiveFormations(app, firstTime =True)
    loadStats(app)
    loadFieldButtons(app)
    loadOffensiveMenuButtons(app)
    resetApp(app)

    app.isField = False
    app.isMainMenu = True
    app.isOffensiveMenu = False
    app.isMainMenuLabelHovering = False
    app.isWRMenu = True

def resetApp(app, isField=True):
    for position in app.oFormation:
        player = app.oFormation[position]
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
    if isField:
        app.isField = True
    else:
        app.isField = False
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
    app.ball = Ball(app.oFormation['C'].cx,app.oFormation['C'].cy,app.oFormation['C'])
    if hasattr(app, 'coverageButton'):
        app.coverageButton.text = f"Coverage: {'C2' if app.coverageShell == 'Cover 2' else 'C1'}"
    loadDefensiveFormations(app)

def loadOffensiveFormations(app, firstTime = False):
    dx = dy = 0
    app.singleBack = {'WR1' : WideReceiver(app, 310, app.lineOfScrimmage+13, 
                                dx, dy, app.route),
                  'WR2': WideReceiver(app, 370, app.lineOfScrimmage+33, 
                                dx, dy, app.route),
                  'LT': Lineman(450, app.lineOfScrimmage+18, dx, dy),
                  'LG': Lineman(475, app.lineOfScrimmage+13, dx, dy),
                  'C': Lineman(app.width//2, app.lineOfScrimmage+13, dx, dy),
                  'RG': Lineman(525, app.lineOfScrimmage+13, dx, dy),
                  'RT': Lineman(550, app.lineOfScrimmage+13, dx, dy),
                  'TE': TightEnd(app, 575, app.lineOfScrimmage+28, 
                                dx, dy, app.route),
                  'WR3': WideReceiver(app, 660, app.lineOfScrimmage+13, 
                                dx, dy, app.route),
                  'QB': Quarterback(app.width//2, app.lineOfScrimmage+40, 
                                dx, dy),
                  'RB': RunningBack(app, app.width//2, app.lineOfScrimmage+70, 
                                dx, dy, app.rbRouteList[2]),
                 }
    app.shotgun = {'WR1' : WideReceiver(app, 310, app.lineOfScrimmage+13, 
                                dx, dy, app.route),
                  'WR2': WideReceiver(app, 370, app.lineOfScrimmage+33, 
                                dx, dy, app.route),
                  'LT': Lineman(450, app.lineOfScrimmage+18, dx, dy),
                  'LG': Lineman(475, app.lineOfScrimmage+13, dx, dy),
                  'C': Lineman(app.width//2, app.lineOfScrimmage+13, dx, dy),
                  'RG': Lineman(525, app.lineOfScrimmage+13, dx, dy),
                  'RT': Lineman(550, app.lineOfScrimmage+13, dx, dy),
                  'TE': TightEnd(app, 575, app.lineOfScrimmage+28, 
                                dx, dy, app.route),
                  'WR3': WideReceiver(app, 660, app.lineOfScrimmage+13, 
                                dx, dy, app.route),
                  'QB': Quarterback(app.width//2, app.lineOfScrimmage+70, 
                                dx, dy),
                  'RB': RunningBack(app, app.width//2 + 35, app.lineOfScrimmage+70, 
                                dx, dy, app.rbRouteList[2]),
                 }
    app.spread = {'WR1' : WideReceiver(app, 300, app.lineOfScrimmage+13, 
                                dx, dy, app.route),
                  'WR2': WideReceiver(app, 340, app.lineOfScrimmage+33, 
                                dx, dy, app.route),
                  'LT': Lineman(450, app.lineOfScrimmage+18, dx, dy),
                  'LG': Lineman(475, app.lineOfScrimmage+13, dx, dy),
                  'C': Lineman(app.width//2, app.lineOfScrimmage+13, dx, dy),
                  'RG': Lineman(525, app.lineOfScrimmage+13, dx, dy),
                  'RT': Lineman(550, app.lineOfScrimmage+18, dx, dy),
                  'WR3': WideReceiver(app, 660, app.lineOfScrimmage+33, 
                                dx, dy, app.route),
                  'WR4': WideReceiver(app, 725, app.lineOfScrimmage+13, 
                                dx, dy, app.route),
                  'QB': Quarterback(app.width//2, app.lineOfScrimmage+70, 
                                dx, dy),
                  'RB': RunningBack(app, app.width//2 + 35, app.lineOfScrimmage+70,
                                dx, dy, app.rbRouteList[2]),
                 }
    app.bunch = {'WR1' : WideReceiver(app, 310, app.lineOfScrimmage+13, 
                                dx, dy, app.route),
                  'WR2': WideReceiver(app, 340, app.lineOfScrimmage+27, 
                                dx, dy, app.route),
                  'WR3': WideReceiver(app, 380, app.lineOfScrimmage+15, 
                                dx, dy, app.route),
                  'LT': Lineman(450, app.lineOfScrimmage+18, dx, dy),
                  'LG': Lineman(475, app.lineOfScrimmage+13, dx, dy),
                  'C': Lineman(app.width//2, app.lineOfScrimmage+13, dx, dy),
                  'RG': Lineman(525, app.lineOfScrimmage+13, dx, dy),
                  'RT': Lineman(550, app.lineOfScrimmage+18, dx, dy),
                  'WR4': WideReceiver(app, 725, app.lineOfScrimmage+13, 
                                dx, dy, app.route),
                  'QB': Quarterback(app.width//2, app.lineOfScrimmage+70, 
                                dx, dy),
                  'RB': RunningBack(app, app.width//2 + 35, app.lineOfScrimmage+70,
                                dx, dy, app.rbRouteList[2]),
                 }
    app.custom = {'WR1' : WideReceiver(app, 290, app.lineOfScrimmage+40, 
                                dx, dy, app.route),
                  'WR2': WideReceiver(app, 340, app.lineOfScrimmage+40, 
                                dx, dy, app.route),
                  'LT': Lineman(450, app.lineOfScrimmage+18, dx, dy),
                  'LG': Lineman(475, app.lineOfScrimmage+13, dx, dy),
                  'C': Lineman(app.width//2, app.lineOfScrimmage+13, dx, dy),
                  'RG': Lineman(525, app.lineOfScrimmage+13, dx, dy),
                  'RT': Lineman(550, app.lineOfScrimmage+18, dx, dy),
                  'WR3': WideReceiver(app, 660, app.lineOfScrimmage+40, 
                                dx, dy, app.route),
                  'WR4': WideReceiver(app, 710, app.lineOfScrimmage+40, 
                                dx, dy, app.route),
                  'QB': Quarterback(app.width//2, app.lineOfScrimmage+70, 
                                dx, dy),
                  'RB': RunningBack(app, app.width//2 + 35, app.lineOfScrimmage+70,
                                dx, dy, app.rbRouteList[2]),
                 }
    app.oFormation = app.singleBack

    app.ball = Ball(app.oFormation['C'].cx,app.oFormation['C'].cy,app.oFormation['C'])

def loadOffensiveRoutes(app):
    #Routes are in (yards, dx, dy) format where yards are steps.
    #'Left/Right' is the starting location relative to center of field
    #RB routes start with 'rb'
    crossingLeft = [(10,-10), (10, -10)]
    crossingRight = [(-10,-10), (-10, -10)]

    slantLeft = [(0, -5), (15,-15)]
    slantRight = [(0, -5), (-15, -15)]

    quickOutLeft = [(0, -3), (-8, 0)]
    quickOutRight = [(0, -3), (8, 0)]  # ((3, 0, -3), (8, 3, 0))

    shallowDigLeft = [(0, -5), (15, 0)]
    shallowDigRight = [(0, -5), (-15, 0)]

    deepDigLeft = [(0, -10), (15, 0)]
    deepDigRight = [(0, -10), (-15,  0)]

    shallowOutLeft = [(0, -5), (-8, 0)]
    shallowOutRight = [(0, -5), (8, 0)]

    deepOutLeft = [(0, -10), (-8, 0)]
    deepOutRight = [(0, -10), (8, 0)]

    shallowHitchLeft = [(0, -8), (2, 2)]
    shallowHitchRight = [(0,-8), (-2, 2)]

    deepHitchLeft = [( 0, -12), (2,3)]
    deepHitchRight = [( 0, -12), (-2,3)]

    postLeft = [( 0, -12), (5, -10)]
    postRight = [(0, -12), (-5, -10)]
    cornerLeft = [(0, -12), (-5, -10)]
    cornerRight = [(0, -12), (5, -10)]

    go = [(0, -11), (0, -11)]

    rbOutLeft = [( 8, -4), ( 5, -2.5)]
    rbOutRight = [(-8, -4), (-5, -2.5)]
    rbZoneSit = [(0, -10), (0, 1)]

   
    app.wrRouteList= [crossingLeft, crossingRight, slantLeft, slantRight,
                    quickOutLeft, quickOutRight, shallowDigLeft,
                    shallowDigRight, deepDigLeft, deepDigRight,
                    shallowOutLeft, shallowOutRight, deepOutLeft,  
                    deepOutRight, shallowHitchLeft, shallowHitchRight,
                    deepHitchLeft, deepHitchRight, postLeft, postRight,
                    cornerLeft, cornerRight, go]
    app.rbRouteList = [rbOutRight, rbOutLeft, rbZoneSit]
    
    app.route = go  #Default route
   
def loadOffensivePlayerRoutes(app):
    for position in app.oFormation:
        player = app.oFormation[position]
        if isinstance(player, WideReceiver) or isinstance(player, TightEnd):
            randomRoute = random.randrange(len(app.wrRouteList))
            
            player.route = player.translateRoute(app, app.route) #app.rbRouteList[randomRoute]
            player.goToPoint(app)
        elif isinstance(player, RunningBack):
            route = app.rbRouteList[0] #Default to zone sit
            player.route = player.translateRoute(app, route) #app.rbRouteList[randomRoute]
            player.goToPoint(app)
            # randomRoute = random.randrange(len(app.rbRouteList))
            # player.route = app.route #app.rbRouteList[randomRoute]
            # targetX = player.cx + player.route.x1*app.yardStep
            # targetY = player.cy + player.route.y1*app.yardStep
            # player.dx, player.dy = goToPoint(app)

#Initialize Defense  
def loadDefensiveFormations(app):
    loadZones(app)
    app.dFormation = initializeDefense(app)

def initializeDefense(app):
    if app.coverageShell == 'Cover 2':
        return initializeCoverTwo(app)
    return initializeCoverOne(app)

def initializeCoverOne(app):
    dx = dy = 0
    wrLocations = getWRLocations(app)
    teLocations = getTELocations(app)
    rbLocations = getRBLocations(app)
    coverOne = dict()
    #Map a CB/LB to a WR/TE
    for i in range(len(wrLocations)):
        wr = wrLocations[i]
        cornerBack = f"CB{i+1}"
        coverOne[cornerBack] = CornerBack(wr.cx,
                    app.lineOfScrimmage-(wr.cy-app.lineOfScrimmage),
                    dx, dy, wr)
    
    
    #Assign LBs to RBs and TEs
    numLBs = 6-len(wrLocations)
    numCoverLBs = len(teLocations) + len(rbLocations)
    numZoneLBs = numLBs-numCoverLBs
    for i in range(numZoneLBs):
        linebacker = f"LB{i+1}"
        zone = app.zones["middleIntermediate"]
        coverOne[linebacker] = LineBacker(0,0,0,0, None, zone)
    
    for i in range(len(rbLocations)):
        rb = rbLocations[i]
        lineBacker = f"LB{i+1 + numZoneLBs}"
        coverOne[lineBacker] = LineBacker(rb.cx,
                app.lineOfScrimmage-(rb.cy-app.lineOfScrimmage+10),
                dx, dy, rb)
        
    numRBs = len(rbLocations)
        
    for i in range(len(teLocations)):
        te = teLocations[i]
        lineBacker = f"LB{i+1+numRBs+numZoneLBs}"
        coverOne[lineBacker] = LineBacker(te.cx,
                app.lineOfScrimmage-(te.cy-app.lineOfScrimmage+10),
                dx, dy, te)
    totalLBs = numZoneLBs + numRBs #not coutning TEs

    for i in range(totalLBs):
        linebacker = coverOne[f"LB{i+1}"]
        #Evenly distribute LBs not gaurding TEs between hash marks
        xCord = 2*app.width//5 + (i+1)*(app.width//5)//(totalLBs+1)
        linebacker.cx,linebacker.cy = xCord, app.lineOfScrimmage - app.yardStep*4
    toUnionCoverOne = {'DE1': DefensiveEnd(app.width*205/500, app.lineOfScrimmage-10, dx, dy),
                       'DE2': DefensiveEnd(app.width*293/500, app.lineOfScrimmage-10, dx, dy),
                       'DT1': DefensiveTackle(app.width*238/500, app.lineOfScrimmage-10, dx, dy),
                       'DT2': DefensiveTackle(app.width*263/500, app.lineOfScrimmage-10, dx, dy),
                       'S': Safety(app.width//2, 
                                   app.lineOfScrimmage-app.yardStep*12, dx, dy, 
                                   None, app.zones['middleDeep'])
                       }
    coverOne |= toUnionCoverOne
    return coverOne

def initializeCoverTwo(app):
    dx = dy = 0
    allEligible = getWRLocations(app) + getTELocations(app) + getRBLocations(app)
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
                                 dx, dy, leftOutside, app.zones['leftFlat'],
                                 shell='Cover 2', side='left', leverage='inside')
    coverTwo['CB2'] = CornerBack(rightCornerX,
                                 app.lineOfScrimmage - app.yardStep * 1.5,
                                 dx, dy, rightOutside, app.zones['rightFlat'],
                                 shell='Cover 2', side='right', leverage='inside')

    coverTwo['LB1'] = LineBacker(app.zones['leftHook'].cx,
                                 app.lineOfScrimmage - app.yardStep * 4.2,
                                 dx, dy, None, app.zones['leftHook'],
                                 shell='Cover 2', side='left')
    coverTwo['LB2'] = LineBacker(app.zones['middleHook'].cx,
                                 app.lineOfScrimmage - app.yardStep * 4.5,
                                 dx, dy, None, app.zones['middleHook'],
                                 shell='Cover 2', side='middle')
    coverTwo['LB3'] = LineBacker(app.zones['rightHook'].cx,
                                 app.lineOfScrimmage - app.yardStep * 4.2,
                                 dx, dy, None, app.zones['rightHook'],
                                 shell='Cover 2', side='right')

    coverTwo['S1'] = Safety(app.zones['leftDeepHalf'].cx,
                            app.lineOfScrimmage - app.yardStep * 11.5,
                            dx, dy, None, app.zones['leftDeepHalf'],
                            shell='Cover 2', side='left')
    coverTwo['S2'] = Safety(app.zones['rightDeepHalf'].cx,
                            app.lineOfScrimmage - app.yardStep * 11.5,
                            dx, dy, None, app.zones['rightDeepHalf'],
                            shell='Cover 2', side='right')

    toUnionCoverTwo = {
        'DE1': DefensiveEnd(app.width*205/500, app.lineOfScrimmage-10, dx, dy),
        'DE2': DefensiveEnd(app.width*293/500, app.lineOfScrimmage-10, dx, dy),
        'DT1': DefensiveTackle(app.width*238/500, app.lineOfScrimmage-10, dx, dy),
        'DT2': DefensiveTackle(app.width*263/500, app.lineOfScrimmage-10, dx, dy)
    }
    coverTwo |= toUnionCoverTwo
    return coverTwo

def loadZones(app):
    fieldLeft = app.sideLineOffset + 20
    fieldRight = app.width - app.sideLineOffset - 20
    fieldWidth = fieldRight - fieldLeft
    fieldMid = (fieldLeft + fieldRight) / 2
    zones = dict()

    zones['middleDeep'] = Zone(fieldWidth/5 + fieldLeft,
                               fieldRight - fieldWidth/5,  0,
                               app.lineOfScrimmage - 10*app.yardStep,
                               fieldMid,
                               app.lineOfScrimmage - 12*app.yardStep)
    
    zones['middleIntermediate'] = Zone(fieldWidth//3 + fieldLeft,
                                       fieldRight - fieldWidth//3,
                                       app.lineOfScrimmage - 9*app.yardStep,
                                       app.lineOfScrimmage - 3*app.yardStep)

    zones['leftDeepHalf'] = Zone(fieldLeft,
                                 fieldMid,
                                 0,
                                 app.lineOfScrimmage - 8*app.yardStep,
                                 fieldLeft + fieldWidth*0.25,
                                 app.lineOfScrimmage - 12*app.yardStep)
    zones['rightDeepHalf'] = Zone(fieldMid,
                                  fieldRight,
                                  0,
                                  app.lineOfScrimmage - 8*app.yardStep,
                                  fieldLeft + fieldWidth*0.75,
                                  app.lineOfScrimmage - 12*app.yardStep)
    zones['leftFlat'] = Zone(fieldLeft,
                             fieldLeft + fieldWidth*0.28,
                             app.lineOfScrimmage - 8*app.yardStep,
                             app.lineOfScrimmage + 2*app.yardStep,
                             fieldLeft + fieldWidth*0.14,
                             app.lineOfScrimmage - 3.5*app.yardStep)
    zones['rightFlat'] = Zone(fieldRight - fieldWidth*0.28,
                              fieldRight,
                              app.lineOfScrimmage - 8*app.yardStep,
                              app.lineOfScrimmage + 2*app.yardStep,
                              fieldLeft + fieldWidth*0.86,
                              app.lineOfScrimmage - 3.5*app.yardStep)
    zones['leftHook'] = Zone(fieldLeft + fieldWidth*0.18,
                             fieldMid,
                             app.lineOfScrimmage - 10*app.yardStep,
                             app.lineOfScrimmage - 2*app.yardStep,
                             fieldLeft + fieldWidth*0.36,
                             app.lineOfScrimmage - 6*app.yardStep)
    zones['middleHook'] = Zone(fieldLeft + fieldWidth*0.36,
                               fieldRight - fieldWidth*0.36,
                               app.lineOfScrimmage - 11*app.yardStep,
                               app.lineOfScrimmage - 3*app.yardStep,
                               fieldMid,
                               app.lineOfScrimmage - 6.5*app.yardStep)
    zones['rightHook'] = Zone(fieldMid,
                              fieldRight - fieldWidth*0.18,
                              app.lineOfScrimmage - 10*app.yardStep,
                              app.lineOfScrimmage - 2*app.yardStep,
                              fieldLeft + fieldWidth*0.64,
                              app.lineOfScrimmage - 6*app.yardStep)
    # zones['leftIntermediate'] = Zone( fieldWidth//4 + 30, app.lineOfScrimmage - 6)
    # zones['rightIntermediate'] = Zone( 3*fieldWidth//4 + 30, app.lineOfScrimmage - 6)
    # zones['leftDeep'] = Zone(fieldWidth//4+30, app.lineOfScrimmage - 12) 
    # zones['rightDeep'] = Zone(3*fieldWidth//4+30, app.lineOfScrimmage - 12)
    app.zones = zones

def loadOffensiveMenuButtons(app):
    app.offensiveFormationButtons = []
    app.offensiveWRRouteButtons = []
    app.offensiveRBRouteButtons = []
    singleBack = FormationButton(95, 80, 
                    130, 65, "Single Back", app.singleBack)
    shotgunButton = FormationButton(95, 170, 
                    130, 65, "Shotgun", app.shotgun)
    spreadButton = FormationButton(95, 260, 
                    130, 65, "Spread", app.spread)
    bunchButton = FormationButton(95, 350, 
                    130, 65, "Bunch", app.bunch)
    customButton = FormationButton(95, 440, 
                    130, 65, "Custom", app.custom)
    app.offensiveFormationButtons.append(singleBack)
    app.offensiveFormationButtons.append(shotgunButton)
    app.offensiveFormationButtons.append(spreadButton)
    app.offensiveFormationButtons.append(bunchButton)
    app.offensiveFormationButtons.append(customButton)

    app.menuInstructionsButton = InstructionButton(105, 538, 175, 50, 
                                            "Toggle Instructions")
    app.fieldInstructionsButton = InstructionButton(app.width - 100, 
                                50, 180, 40, 'Toggle Instructions')

    #splices app.WR routes to get left and right route
    crossingButton = RouteButton(app.width-95, 50, 
                            130, 35, "Crossing", app.wrRouteList[0:2]) 
    slantButton = RouteButton(app.width-95, 110, 
                            130, 35, "Slant", app.wrRouteList[2:4])
    quickOutButton = RouteButton(app.width-95, 170, 
                            130, 35, "Quick Out", app.wrRouteList[4:6])
    shallowDigButton = RouteButton(app.width-95, 230, 
                            130, 35, "Shallow Dig", app.wrRouteList[6:8])
    deepDigButton = RouteButton(app.width-95, 290, 
                            130, 35, "Deep Dig", app.wrRouteList[8:10])
    shallowOutButton = RouteButton(app.width-95, 350, 
                            130, 35, "Shallow Out", app.wrRouteList[10:12])
    deepOutButton = RouteButton(app.width-95, 410, 
                            130, 35, "Deep Out", app.wrRouteList[12:14])
    shallowHitchButton = RouteButton(app.width-95, 470, 
                            130, 35, "Shallow Hitch", app.wrRouteList[14:16])
    deepHitchButton = RouteButton(app.width-95, 530, 
                            130, 35, "Deep Hitch", app.wrRouteList[16:18])
    postButton = RouteButton(app.width-95, 590, 
                            130, 35, "Post", app.wrRouteList[18:20])
    cornerButton = RouteButton(app.width-95, 650, 
                            130, 35, "Corner", app.wrRouteList[20:22])
    goButton = RouteButton(app.width-95, 710, 
                            130, 35, "Go", [app.wrRouteList[22], 
                                            app.wrRouteList[22]])
    app.offensiveWRRouteButtons.append(crossingButton)
    app.offensiveWRRouteButtons.append(slantButton)
    app.offensiveWRRouteButtons.append(quickOutButton)
    app.offensiveWRRouteButtons.append(shallowDigButton)
    app.offensiveWRRouteButtons.append(deepDigButton)
    app.offensiveWRRouteButtons.append(shallowOutButton)
    app.offensiveWRRouteButtons.append(deepOutButton)
    app.offensiveWRRouteButtons.append(shallowHitchButton)
    app.offensiveWRRouteButtons.append(deepHitchButton)
    app.offensiveWRRouteButtons.append(postButton)
    app.offensiveWRRouteButtons.append(cornerButton)
    app.offensiveWRRouteButtons.append(goButton)
    app.startGameButton = StartButton(app.width//2, 650, 300, 
                                        150 , "Start Game")

    rbOutButton = RouteButton(app.width-95, 50, 
                        130, 35, "RB Out", app.rbRouteList[0:2]) 
    rbZoneSitButton = RouteButton(app.width-95, 110, 
                        130, 35, "RB Zone Sit", [app.rbRouteList[2], 
                                                app.rbRouteList[2]])
    app.offensiveRBRouteButtons.append(rbOutButton)
    app.offensiveRBRouteButtons.append(rbZoneSitButton)
    app.importButton = exportImportButton(app.sideLineOffset//2, 
                    app.height-120, 150, 50, "Import Play", dict())
    app.exportButton = exportImportButton(app.sideLineOffset//2, 
                app.height-45, 150, 50, "Export Play", dict())

def loadFieldButtons(app):
    resetButton = Button(app.sideLineOffset//2, 40, 100, 50, "Reset")
    menuButton = Button(app.sideLineOffset//2, 110, 100, 50, "Menu")
    app.coverageButton = Button(app.sideLineOffset//2, 500, 150, 50, "Coverage: C1")
    app.fieldButtons = [resetButton, menuButton]

def getWRLocations(app):
    wrLocations = []
    for position in app.oFormation:
        player = app.oFormation[position]
        if isinstance(player, WideReceiver):
            wrLocations.append(player)
    return wrLocations

def getTELocations(app):
    teLocations = []
    for position in app.oFormation:
        player = app.oFormation[position]
        if isinstance(player, TightEnd):
            teLocations.append(player)
    return teLocations

def getRBLocations(app):
    rbLocations = []
    for position in app.oFormation:
        player = app.oFormation[position]
        if isinstance(player, RunningBack):
            rbLocations.append(player)
    return rbLocations

def loadStats(app):
    app.numCompletions = 0
    app.attempts = 0
    app.totalYards = 0
    app.ints = 0
    app.qbRun = True
    app.statsButton = StatsButton(app.width - 100, 130, 130, 40, 'Stats')
