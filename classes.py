from cmu_graphics import *
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
        if self.cy <= 10*app.yardStep:
            offset = 10*app.yardStep - app.ball.cy
        scalefactor = 1+self.height/50
        angle = self.getAngle()
        drawOval(self.cx, self.cy + offset, 10 * scalefactor, 5*scalefactor, 
                 fill='brown', align='center', rotateAngle = angle)
    
    def throwToTarget(self, targetX, targetY, app):
        self.targetX = targetX
        self.targetY = targetY
        self.carrier = None
        self.height = 5
        self.throwDistance = distance(self.cx, self.cy, targetX, targetY)
        dx = self.targetX - self.cx
        dy = self.targetY - self.cy
        ratio = app.ballVelocity/self.throwDistance
        self.dx = dx * ratio
        self.dy = dy * ratio
        self.distanceTravelled = 0
    
    def updateBallPosition(self, app):
        if self.carrier != None:
            if self.carrier == app.oFormation['C']:
                self.beingSnapped = True
                app.ballVelocity = 4
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
        elif self.targetX != None and self.targetY != None:
            #Move ball towards target
            self.cx += self.dx
            self.cy += self.dy
            self.distanceTravelled += app.ballVelocity
            self.updateHeight(app)
            self.checkCatch(app)
    
    def updateHeight(self, app):
        timePassed = self.distanceTravelled/app.ballVelocity
        totalTime = self.throwDistance/app.ballVelocity
        acceleration = 0.01
        
        yInitial = acceleration*totalTime/2
        yVelocity = yInitial-acceleration*timePassed
        self.height += yVelocity
    
    def checkCatch(self, app):
        if self.height <= 0:
            #Ball hit ground
            app.playResult = 'Incomplete'
            app.lastPlayResult = 'Incomplete'
            app.lastYardsRan = 0
            app.attempts += 1
            app.isPaused = True
            self.height = 0
            self.dx, self.dy = 0, 0
            self.targetX, self.targetY = None, None
        elif self.height <= 6:
            #Ball is catchable
            closestReceiver = None
            closestDistance = float('inf')
            allPlayers = list(app.oFormation.values())+list(app.dFormation.values())
            for player in allPlayers:
                if (isinstance(player, SkillPlayer) 
                    or (isinstance(player, Quarterback) and self.beingSnapped) 
                    or isinstance(player, CoverPlayer)):
                    distToBall = distance(self.cx, self.cy, player.cx, player.cy)
                    if distToBall < closestDistance:
                        closestDistance = distToBall
                        closestReceiver = player
            if closestDistance <= 10:
                #Caught!
                self.beingSnapped = False
                self.carrier = closestReceiver
                if isinstance(closestReceiver, CoverPlayer):
                    app.playResult = 'Intercepted'
                    app.lastPlayResult = 'Intercepted'
                    app.lastYardsRan = 0
                    app.ints += 1
                self.cx = closestReceiver.cx
                self.cy = closestReceiver.cy
                self.dx, self.dy = 0, 0
                self.targetX, self.targetY = None, None
                self.height = 0
        elif self.height <=8:
            defPlayers = list(app.dFormation.values())
            for player in defPlayers:
                if isinstance(player, CoverPlayer):
                    distToBall = distance(self.cx, self.cy, player.cx, player.cy)
                    if distToBall <= 10:
                        app.playResult = 'Incomplete'
                        app.lastPlayResult = 'Incomplete'
                        app.lastYardsRan = 0
                        app.attempts += 1
                        self.dx, self.dy = 0, 0
                        self.targetX, self.targetY = None, None
                        self.height = 0
    def getAngle(self):
        if self.targetX != None and self.targetY!= None:
            _, angle = getRadiusAndAngleToEndpoint(self.cx, self.cy, 
                                                   self.targetX, self.targetY)
            return -angle
        else:
            return 90
class Zone:
    def __init__(self,left, right, top, bottom, cx=None, cy=None):
        self.cx = cx if cx != None else (left + right)/2
        self.cy = cy if cy != None else (top + bottom)/2
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
                self.cx==other.cx and
                self.cy==other.cy)
               
    def __hash__(self):
        return hash(str(self))
       
    def isOutOfBounds(self,app):
        boundaryOffset = 20
        if (self.cx <= app.sideLineOffset+boundaryOffset or 
            self.cx>=app.width-boundaryOffset):
            return True
        else: return False

    def clickInPlayer(self, mouseX, mouseY):
        if distance(self.cx, self.cy, mouseX, mouseY) <= 10:
            return True
        else:
            return False
    
    def goToPoint(self, app):
        boundaryOffset = 20
        if (self.targetX <= boundaryOffset+app.sideLineOffset):
            self.targetX = boundaryOffset+app.sideLineOffset
        elif (self.targetX >= app.width-boundaryOffset-app.sideLineOffset): 
            self.targetX = app.width-boundaryOffset-app.sideLineOffset
        dx = self.targetX - self.cx
        dy = self.targetY - self.cy
        dist = distance(self.cx, self.cy, self.targetX, self.targetY)
        if dist == 0:
            return

        # Desired velocity direction
        desiredVx = (dx / dist) * app.maxSpeed
        desiredVy = (dy / dist) * app.maxSpeed
        # Slow down when close to target
        correctionDist = 2*app.yardStep
        if dist < correctionDist:
            desiredVx *= dist / correctionDist
            desiredVy *= dist / correctionDist

        # Steering = desired - current velocity
        steerX = desiredVx - self.dx
        steerY = desiredVy - self.dy

        # Limit steering force (acceleration)
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
        goalLine = app.lineOfScrimmage - app.yardStep*85
        self.targetY = goalLine 
        self.goToPoint(app)
        self.movePlayer(app)

    def block(self, app):
        defender = self.getNearestDefender(app)
        self.stopPlayer(app, defender)

    def movePlayer(self, app):
        self.cx+=self.dx
        self.cy+=self.dy
        boundaryOffset = 20
        if self.cx <= boundaryOffset+app.sideLineOffset:
            self.cx = boundaryOffset+app.sideLineOffset
        elif self.cx >= app.width-boundaryOffset-app.sideLineOffset:
            self.cx = app.width-boundaryOffset-app.sideLineOffset

    def stopPlayer(self, app, target):
        #Assumes target is a WideReceiver, TightEnd, or RunningBack
        playerVelo=app.maxSpeed
        targetVelo = (target.dx**2 + target.dy**2)**0.5
        vRatio=targetVelo/playerVelo
        C = distance(self.cx, self.cy, target.cx, target.cy)
        _, targetAngle = getRadiusAndAngleToEndpoint(0, 0, 
                                                    target.dx, target.dy)
        _, angleToTarget = getRadiusAndAngleToEndpoint(target.cx, target.cy, 
                                                self.cx, self.cy)
        angleDifference = (targetAngle - angleToTarget) % 360
        sinTheta = math.sin(math.radians(angleDifference))
        playerAngle = (math.degrees(math.asin(sinTheta * vRatio))) % 360
        ballAngle= 180-(angleDifference + playerAngle)
        sinGoalPointAngle = math.sin(math.radians(ballAngle))
        if - 0.0015< sinGoalPointAngle<0.0015 :
            self.targetX, self.targetY = getRadiusEndpoint(self.cx, self.cy, 
                                                       10*app.yardStep, 
                                                       targetAngle)
            self.goToPoint(app)
            self.movePlayer(app)
            return
        throwDistance = (C * sinTheta) / sinGoalPointAngle
        throwAngle = (angleToTarget - 180) - playerAngle

        self.targetX, self.targetY = getRadiusEndpoint(self.cx, self.cy, 
                                                       throwDistance, 
                                                       throwAngle)
        self.goToPoint(app)
        self.movePlayer(app)

    def getNearestDefender(self, app):
        closestDist = None
        closest = None
        for player in app.dFormation.values():
            dist = distance(self.cx, self.cy, player.cx, player.cy)
            if closestDist == None or dist<closestDist:
                closest = player
                closestDist = dist
        return closest
        
class SkillPlayer(Player):
    def __init__(self, app,  cx, cy, dx=0, dy=0, 
                    route=None, translated=False):
        super().__init__( cx, cy, dx, dy)
        self.targetX = self.cx + route[0][0]*app.yardStep
        self.targetY = self.cy + route[0][1]*app.yardStep
        if not translated:
            self.route = self.translateRoute(app,route)
        else:
            self.route = route

    def runRoute(self, app):
        yardsRunAlready = 0
        for i in range(1, len(self.route)):
            currStep = self.route[i]
            prevStep = self.route[i-1]
            step = (currStep[0]-prevStep[0], currStep[1]-prevStep[1])
            stepLength = ((step[0])**2 + (step[1])**2)**0.5
            stepLength = stepLength/app.yardStep
            if app.yardsRan >= stepLength + yardsRunAlready: #Completed this step
                yardsRunAlready += stepLength
                if i == len(self.route)-1:
                    self.goToPoint(app)
                    break
            else:  
                self.targetX = currStep[0]
                self.targetY = currStep[1]
                self.goToPoint(app)
                break
        self.movePlayer(app)

    def translateRoute(self, app, route):
        boundaryOffset = 20
        newRoute = [(x*app.yardStep,
                      y*app.yardStep) for (x,y) in route]
        newRoute = [(self.startX, self.startY)] + newRoute
        for i in range(1, len(newRoute)):
            endX, endY = newRoute[i]
            startX, startY = newRoute[i-1]
            endX += startX
            endY += startY
            if endX <= boundaryOffset+app.sideLineOffset:
                endX = boundaryOffset+app.sideLineOffset
            elif endX>=app.width-boundaryOffset-app.sideLineOffset:
                endX = app.width-boundaryOffset-app.sideLineOffset
            newRoute[i] = (endX, endY)
        return newRoute

    def drawRoute(self, app):
        boundaryOffset = 20
        i=1
        while i < len(self.route)-1:
            endX, endY = self.route[i]
            startX, startY = self.route[i-1]
    
            drawLine(startX, startY, endX, endY,
                     fill='black', lineWidth=2)
            i+=1
        arrowX, arrowY = self.route[-1]
        if arrowX <= boundaryOffset+app.sideLineOffset:
            arrowX = boundaryOffset+app.sideLineOffset
        elif arrowX>=app.width-boundaryOffset-app.sideLineOffset:
            arrowX = app.width-boundaryOffset-app.sideLineOffset
        prevX, prevY = self.route[-2]
        drawLine(prevX, prevY, arrowX, arrowY, 
                fill='black', lineWidth=2, arrowEnd=True)

    def drawVelocity(self, app):
        drawLine(self.cx, self.cy,
                 self.cx + self.dx*5,
                 self.cy + self.dy*5,
                 fill='blue', lineWidth=2)
    

class WideReceiver(SkillPlayer):
    def __init__(self, app,  cx, cy, dx=0, dy=0, route=None, translated=False):
        super().__init__( app, cx, cy, dx, dy, route, translated)

class RunningBack(SkillPlayer):
    def __init__(self, app,  cx, cy, dx=0, dy=0, route=None, translated=False):
        super().__init__( app, cx, cy, dx, dy, route, translated)

class TightEnd(SkillPlayer):
    def __init__(self, app,  cx, cy, dx=0, dy=0, route=None, translated=False):
        super().__init__( app, cx, cy, dx, dy, route, translated)

class Quarterback(Player):
    def __init__(self,  cx, cy, dx=0, dy=0):
        super().__init__( cx, cy, dx, dy)

class Lineman(Player):
    def __init__(self,  cx, cy, dx=0, dy=0):
        super().__init__( cx, cy, dx, dy)

class CoverPlayer(Player):
    def __init__(self,  cx, cy, dx=0, dy=0, man=None, zone=None,
                 shell='Cover 1', side='middle', leverage='balanced'):
        super().__init__( cx, cy, dx, dy)
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
    
    def guardMan(self, app):
        if self.shell == 'Cover 2':
            self.playZone(app)
            return
        if self.man == None:
            if self.zone != None:
                self.playZone(app)
            return
        self.targetX, self.targetY = getBallPlacement(self.man, app)
        if app.yardsRan < 3:
            self.targetY = min(app.lineOfScrimmage - app.yardStep*5, self.targetY)
        # if distance(self.cx, self.cy, self.targetX, self.targetY) < 30:
        #     self.targetX = self.cx
        #     self.targetY = self.cy
        self.goToPoint(app)
        self.cx += self.dx
        self.cy += self.dy
        
        
        if self.cx <= 24:
            self.cx = 24
        elif self.cx >= app.width-24:
            self.cx = app.width-24
    
    def playZone(self, app):
        zone = self.zone
        if zone is None:
            return
        #Find target point in zone
        self.targetX = zone.cx
        self.targetY = zone.cy
        bestThreat = self.helpTarget
        if bestThreat is None and self.matchTarget is not None:
            ballX, ballY = getBallPlacement(self.matchTarget, app)
            if pointInZone(ballX, ballY, zone):
                bestThreat = self.matchTarget
            else:
                self.matchTarget = None
                self.callout = 'Pass off!'
        if bestThreat is None:
            candidates = []
            for player in app.oFormation.values():
                if not isinstance(player, SkillPlayer):
                    continue
                ballX, ballY = getBallPlacement(player, app)
                if pointInZone(ballX, ballY, zone):
                    depthScore = app.lineOfScrimmage - ballY
                    candidates.append((depthScore, player, ballX, ballY))
            if len(candidates) > 0:
                candidates.sort(reverse=True, key=lambda t: t[0])
                _, bestThreat, targetX, targetY = candidates[0]
                self.matchTarget = bestThreat
                self.targetX = targetX
                self.targetY = targetY
                if len(candidates) > 1 and self.shell == 'Cover 2':
                    self.callout = 'Overload!'
        if bestThreat is not None:
            targetX, targetY = getBallPlacement(bestThreat, app)
            self.targetX = targetX
            self.targetY = targetY

        self.targetX = clamp(self.targetX, zone.left, zone.right)
        self.targetY = clamp(self.targetY, zone.top, zone.bottom)
        self.goToPoint(app)
        self.cx += self.dx
        self.cy += self.dy
        
        if self.cx <= 24:
            self.cx = 24
        elif self.cx >= app.width-24:
            self.cx = app.width-24
    
    def checkTackle(self, app):
        ballCarrier= app.ball.carrier
        dist = distance(self.cx, self.cy, ballCarrier.cx, ballCarrier.cy)
        if dist <= 15:
            app.playResult = 'Tackled'
            app.lastPlayResult = 'Tackled'
            app.lastYardsRan = int((app.lineOfScrimmage - 
                                app.ball.carrier.cy)/app.yardStep)
            app.totalYards += int((app.lineOfScrimmage - 
                                app.ball.carrier.cy)/app.yardStep)
            if app.qbRun:
                app.lastPlayResult += ' (QB Run)'
            else:
                app.numCompletions += 1
                app.attempts += 1

class CornerBack(CoverPlayer):
    def __init__(self,  cx, cy, dx=0, dy=0, man=None, zone=None,
                 shell='Cover 1', side='middle', leverage='balanced'):
        super().__init__( cx, cy, dx, dy, man, zone, shell, side, leverage)

    def guardMan(self, app):
        if self.shell != 'Cover 2':
            super().guardMan(app)
            return
        self.playCoverTwoTechnique(app)

    def playCoverTwoTechnique(self, app):
        zone = self.zone
        if zone is None:
            super().guardMan(app)
            return
        primaryReceiver = self.man
        if primaryReceiver is None:
            bestDist = float('inf')
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
        if primaryReceiver is None:
            self.playZone(app)
            return
        self.man = primaryReceiver
        insideLever = 1 if self.side == 'left' else -1

        # In Cover 2, corners must drive any flat threat (RB, WR, or TE) entering
        # their zone, not only the initially jammed outside receiver.
        flatThreat = None
        flatThreatDist = float('inf')
        if self.helpTarget is not None:
            helpX, helpY = getBallPlacement(self.helpTarget, app)
            if pointInZone(helpX, helpY, zone):
                flatThreat = self.helpTarget
                flatThreatDist = distance(self.cx, self.cy, helpX, helpY)
        for player in app.oFormation.values():
            if not isinstance(player, SkillPlayer):
                continue
            threatX, threatY = getBallPlacement(player, app)
            if not pointInZone(threatX, threatY, zone):
                continue
            dist = distance(self.cx, self.cy, threatX, threatY)
            if dist < flatThreatDist:
                flatThreatDist = dist
                flatThreat = player

        # Jam-and-funnel phase at the line, forcing release to inside help.
        if (flatThreat is None and app.yardsRan <= 2.6 and
            primaryReceiver.cy >= app.lineOfScrimmage - app.yardStep):
            self.targetX = primaryReceiver.cx + insideLever * app.yardStep * 0.45
            self.targetY = min(primaryReceiver.cy - app.yardStep * 0.3,
                               app.lineOfScrimmage - app.yardStep * 0.45)
            if distance(self.cx, self.cy, primaryReceiver.cx, primaryReceiver.cy) <= 14:
                primaryReceiver.dx *= 0.8
                primaryReceiver.targetX += insideLever * app.yardStep * 0.35
                self.callout = 'Force inside!'
        else:
            targetReceiver = flatThreat if flatThreat is not None else primaryReceiver
            ballX, ballY = getBallPlacement(targetReceiver, app)
            if pointInZone(ballX, ballY, zone):
                self.targetX = ballX + insideLever * app.yardStep * 0.3
                self.targetY = ballY
                if targetReceiver is not primaryReceiver:
                    self.callout = 'Drive flat!'
            else:
                self.targetX = zone.cx + insideLever * app.yardStep * 0.4
                self.targetY = zone.cy
            self.targetX = clamp(self.targetX, zone.left, zone.right)
            self.targetY = clamp(self.targetY, zone.top, zone.bottom)
            if primaryReceiver.cy < app.lineOfScrimmage - 6 * app.yardStep:
                self.callout = 'Carry + pass!'
        self.goToPoint(app)
        self.movePlayer(app)

class LineBacker(CoverPlayer):
    def __init__(self,  cx, cy, dx=0, dy=0, man=None, zone=None,
                 shell='Cover 1', side='middle', leverage='balanced'):
        super().__init__( cx, cy, dx, dy, man, zone, shell, side, leverage)

class PassRusher(Player):
    def __init__(self,  cx, cy, dx=0, dy=0):
        super().__init__( cx, cy, dx, dy)
        self.rushingQB = False
    
    def rushQB(self, app):
        if app.isPashRush == False:
            self.targetX = self.cx
            self.targetY = self.cy
            return
        qb = app.oFormation['QB']
        if self.rushingQB:
            self.targetX = qb.cx
            self.targetY = qb.cy
        else:
            #Give illusion of pass rush
            hashOffset = 8
            closestRusher = None
            closestDist = float('inf')
            for position in app.dFormation:
                player = app.dFormation[position]
                if (distance(player.cx, player.cy, qb.cx, qb.cy)<closestDist or
                    closestRusher == None):
                    closestRusher = player
                    closestDist = distance(player.cx, player.cy, qb.cx, qb.cy)

            if qb.cx < 3*app.width//7 and closestRusher == self:
                self.rushingQB = True
            elif qb.cx > 4*app.width//7 and closestRusher == self:
                self.rushingQB = True
            elif self.cx < 3*app.width//7+hashOffset:
                self.targetX = 3*app.width//7+hashOffset
            elif self.cx > 4*app.width//7-hashOffset:
                self.targetX = 4*app.width//7-hashOffset
            else:
                self.targetX = self.cx
            self.targetY = app.lineOfScrimmage + 1*app.yardStep
            #Actual pash rush is random
            if random.randrange(0, app.stepsPerSecond*40) == 1 and app.yardsRan >3:
                self.rushingQB = True
        self.goToPoint(app)
        self.movePlayer(app)
    
    def checkTackle(self, app):
        ballCarrier= app.ball.carrier
        dist = distance(self.cx, self.cy, ballCarrier.cx, ballCarrier.cy)
        if dist <= 15:
            app.playResult = 'Tackled'
            app.lastPlayResult = 'Tackled'
            app.lastYardsRan = int((app.lineOfScrimmage - 
                                app.ball.carrier.cy)/app.yardStep)
            app.totalYards += int((app.lineOfScrimmage - 
                                app.ball.carrier.cy)/app.yardStep)
            app.numCompletions = 0
            app.attempts = 0

class DefensiveTackle(PassRusher):
    def __init__(self,  cx, cy, dx=0, dy=0):
        super().__init__( cx, cy, dx, dy)

class DefensiveEnd(PassRusher):
    def __init__(self,  cx, cy, dx=0, dy=0):
        super().__init__( cx, cy, dx, dy)

class Safety(CoverPlayer):
    def __init__(self,  cx, cy, dx=0, dy=0, man=None, zone=None,
                 shell='Cover 1', side='middle', leverage='balanced'):
        super().__init__( cx, cy, dx, dy, man, zone, shell, side, leverage)

class Button:
    customGreen1 = rgb(19, 130, 60)
    def __init__(self, cx, cy, w, h, text):
        self.cx = cx
        self.cy = cy
        self.w = w
        self.h = h
        self.text = text
        self.bolded = False
    
    def isClicked(self, mx, my):
        return ((self.cx-self.w//2)<=mx<=(self.cx+self.w//2) and 
                (self.cy-self.h//2)<=my<=(self.cy+self.h/2))

    def checkBold(self, mx, my):
        if self.isClicked(mx, my):
            self.bolded = True
        else:
            self.bolded = False

    def draw(self):
        drawRect(self.cx, self.cy, self.w+7, self.h+4.4,
                fill='black', align='center')
        drawRect(self.cx, self.cy, self.w, self.h,
                fill=Button.customGreen1, align='center')
        drawLabel(self.text, self.cx, self.cy, size=18, 
                    bold = self.bolded, align='center')

class FormationButton(Button):
    def __init__(self, cx, cy, w, h, text, formation):
        super().__init__(cx, cy, w, h, text)
        self.formation = formation

    def resetFormation(self, app, formation):
        self.formation = formation

class RouteButton(Button):
    def __init__(self, cx, cy, w, h, text, routes):
        super().__init__(cx, cy, w, h, text)
        self.leftRoute = routes[0]
        self.rightRoute = routes[1]

class InstructionButton(Button):
    customGreen2 = rgb(8, 110, 40)
    def __init__(self, cx, cy, w, h, text):
        super().__init__(cx, cy, w, h, text)
        self.isInstructions = False

    def draw(self):
        drawRect(self.cx, self.cy, self.w+7, self.h+4.4,
                fill='black', align='center')
        drawRect(self.cx, self.cy, self.w, self.h,
                fill=InstructionButton.customGreen2, align='center')
        drawLabel(self.text, self.cx, self.cy, size=18, 
                    bold = self.bolded, align='center')


class StartButton(Button):
    customComplimentRed = rgb(215, 80, 75)
    def __init__(self, cx, cy, w, h, text):
        super().__init__(cx, cy, w, h, text)


    def draw(self):
        drawRect(self.cx, self.cy, self.w+7, self.h+4.4,
                fill='black', align='center')
        drawRect(self.cx, self.cy, self.w, self.h,
                fill=StartButton.customComplimentRed, align='center')
        drawLabel(self.text, self.cx, self.cy, size=48, 
                    bold = self.bolded, align='center')

class exportImportButton(Button):
    customGreen3 = rgb(8, 90, 35)
    def __init__(self, cx, cy, w, h, text, data):
        super().__init__(cx, cy, w, h, text)
        self.data = data

    def draw(self):
        drawRect(self.cx, self.cy, self.w+7, self.h+4.4,
                fill='black', align='center')
        drawRect(self.cx, self.cy, self.w, self.h,
                fill=exportImportButton.customGreen3, align='center')
        drawLabel(self.text, self.cx, self.cy, size=18, 
                    bold = self.bolded, align='center')

class StatsButton(Button):
    customGreen4 = rgb(10, 70, 25)
    def __init__(self, cx, cy, w, h, text):
        super().__init__(cx, cy, w, h, text)
        self.isStats = False

    def draw(self):
        drawRect(self.cx, self.cy, self.w+7, self.h+4.4,
                fill='black', align='center')
        drawRect(self.cx, self.cy, self.w, self.h,
                fill=StatsButton.customGreen4, align='center')
        drawLabel(self.text, self.cx, self.cy, size=18, 
                    bold = self.bolded, align='center')

def moveQB(app):
    self = app.oFormation['QB']
    self.targetX = 10#self.cx
    self.targetY = 10#app.lineOfScrimmage + app.yardStep*3
    self.goToPoint(app)
    self.cx += self.dx
    self.cy += self.dy

def moveOffense(app):
    for position in app.oFormation:
        player = app.oFormation[position]
        if player == app.ball.carrier and not isinstance(player, Lineman):
            player.goToPoint(app)
            player.movePlayer(app)
        elif isinstance(player, Quarterback):
            player.targetX = player.cx
            player.targetY = app.lineOfScrimmage + app.yardStep*3
            player.goToPoint(app)
            player.cx += player.dx
            player.cy += player.dy
        elif isinstance(player, SkillPlayer): #or \
        #    isinstance(app.oFormation[position], TightEnd) or \
        #    isinstance(app.oFormation[position], RunningBack):
            if (app.ball.targetX != None and app.ball.targetY != None 
                and not app.ball.beingSnapped):
                player.trackBall(app)
            elif app.ball.carrier == app.oFormation['QB']:
                player.runRoute(app)
            elif player == app.ball.carrier:
                player.runWithBall(app)
            else:
                player.block(app)

def moveDefense(app):
    if app.coverageShell == 'Cover 2':
        coordinateCoverTwo(app)
    for position in app.dFormation:
        player = app.dFormation[position]
        if isinstance(player, CoverPlayer):
            if (app.ball.targetX != None and app.ball.targetY != None 
                and not app.ball.beingSnapped):
                player.trackBall(app)
            elif (app.ball.carrier == app.oFormation['QB'] and 
                  app.oFormation['QB'].cy > app.lineOfScrimmage
                  or app.ball.beingSnapped):
                player.guardMan(app)
            else: # try to tackle him
                player.stopPlayer(app, app.ball.carrier)
                player.checkTackle(app)
        elif isinstance(player, PassRusher):
            player.rushQB(app)
            if app.ball.carrier == app.oFormation['QB']:
                player.checkTackle(app)

##############################
### Moving Players Helpers ###
##############################


def getBallPlacement(target, app):
    #Assumes target is a WideReceiver, TightEnd, or RunningBack
    #Find self
    for position in app.oFormation:
        player = app.oFormation[position]
        if isinstance(player, Quarterback):
            self = player
            break
    ballVelo=app.velocity*3
    playerVelo = (target.dx**2 + target.dy**2)**0.5
    vRatio=playerVelo/ballVelo
    C = distance(self.cx, self.cy, target.cx, target.cy)
    _, targetAngle = getRadiusAndAngleToEndpoint(0, 0, 
                                                   target.dx, target.dy)
    _, angleToTarget = getRadiusAndAngleToEndpoint(target.cx, target.cy, 
                                               self.cx, self.cy)
    angleDifference = (targetAngle - angleToTarget) % 360
    sinTheta = math.sin(math.radians(angleDifference))
    playerAngle = math.degrees(math.asin(sinTheta * vRatio)) % 360
    ballAngle= 180-(angleDifference + playerAngle)
    Point = math.sin(math.radians(ballAngle))
    if Point == 0:
        Point = 0.0001
    throwDistance = (C * sinTheta) / Point
    throwAngle = (angleToTarget - 180) - playerAngle

    ballX, ballY = getRadiusEndpoint(self.cx, self.cy, throwDistance, throwAngle)
    #put the tartget slightly in front of the target
    ballDistanceToself = distance(self.cx, self.cy, ballX, ballY)
    if (self.cx == ballX) and (self.cy == ballY):
        return ballX, ballY
    ballToselfX =  (self.cx - ballX)/ballDistanceToself 
    ballToselfY = (self.cy - ballY)/ballDistanceToself
    correctedX = ballX + ballToselfX * app.yardStep*0.5
    correctedY = ballY + ballToselfY * app.yardStep*0.5
    return correctedX, correctedY

def getRadiusEndpoint(cx, cy, r, theta):
    return (cx + r*math.cos(math.radians(theta)),
            cy - r*math.sin(math.radians(theta)))

def getRadiusAndAngleToEndpoint(cx, cy, targetX, targetY):
    radius = distance(cx, cy, targetX, targetY)
    angle = math.degrees(math.atan2(cy-targetY, targetX-cx)) % 360
    return (radius, angle)

def distance(x1, y1, x2, y2):
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

def clamp(value, low, high):
    return max(low, min(value, high))

def pointInZone(x, y, zone):
    return zone.left <= x <= zone.right and zone.top <= y <= zone.bottom

def coordinateCoverTwo(app):
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

    for defender in zoneDefenders:
        threats = threatMap[defender]
        if len(threats) <= 1:
            continue
        _, extraThreat, extraX, extraY = threats[1]
        helper = None
        helperDist = float('inf')
        for teammate in zoneDefenders:
            if teammate == defender:
                continue
            if not pointInZone(extraX, extraY, teammate.zone):
                continue
            dist = distance(teammate.cx, teammate.cy, extraX, extraY)
            if dist < helperDist:
                helperDist = dist
                helper = teammate
        if helper is not None and helper.helpTarget is None:
            helper.helpTarget = extraThreat
            defender.callout = 'Need help!'
            helper.callout = 'I got #2'
    
def correctPlayers(app):
    offset = 10*app.yardStep - app.ball.carrier.cy
    players = list(app.oFormation.values()) + list(app.dFormation.values())
    for player in players:
        player.cy += offset

def handleCollisions(app):
    players = list(app.oFormation.values()) + list(app.dFormation.values())
    r1 = r2 = 10  # radius of players
    for i in range(len(players)):
        for j in range(i+1, len(players)):
            p1 = players[i]
            p2 = players[j]
            xDiff = p2.cx - p1.cx
            yDiff = p2.cy - p1.cy
            dist = distance(p1.cx, p1.cy, p2.cx, p2.cy)
            if dist == 0:
                xDiff = 0.01
                yDiff = 0.01
                dist = distance(0,0,xDiff,yDiff)
            overlap = (r1 + r2) - dist
            
            if overlap > 7:  # collision detected
                nx, ny = xDiff/dist, yDiff/dist
                correction = 0.5
            
                p1.cx -= nx * correction 
                p1.cy -= ny * correction 
                p2.cx += nx * correction 
                p2.cy += ny * correction 
