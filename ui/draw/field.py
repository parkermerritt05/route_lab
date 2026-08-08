from cmu_graphics import drawLabel, drawLine, drawRect
from constants import (BOUNDARY_OFFSET, CAMERA_SCROLL_YARDS, FIELD_APRON,
                       FIELD_GREEN, FIELD_GREEN_STRIPE, HASH_MARK_COLOR,
                       HASH_MARK_LENGTH, LOS_COLOR, LOS_TICK_HALF, LOS_WIDTH,
                       MOW_STRIPE_YARDS, SIDELINE_WIDTH, YARD_LINE_MAJOR,
                       YARD_LINE_MAJOR_WIDTH, YARD_LINE_MINOR,
                       YARD_LINE_MINOR_WIDTH, YARD_NUMBER_COLOR, YARD_NUMBER_SIZE)
from simulation.geometry import leftHashX, rightHashX


def cameraOffset(app):
    if app.ball.cy <= CAMERA_SCROLL_YARDS * app.yardStep:
        return CAMERA_SCROLL_YARDS * app.yardStep - app.ball.cy
    return 0


def drawField(app, scrimmageLine=True):
    drawMowStripes(app)
    drawFieldApron(app)
    drawYardLines(app)
    if scrimmageLine and not app.isPlayActive:
        drawLineOfScrimmage(app)
    drawSidelines(app)


def drawMowStripes(app):
    offset = cameraOffset(app)
    stripeHeight = app.yardStep * MOW_STRIPE_YARDS
    yardZeroY = app.height + app.yardStep
    index = 0
    while yardZeroY - index * stripeHeight + offset < app.height:
        index -= 1
    while yardZeroY - index * stripeHeight + offset > 0:
        worldTop = yardZeroY - (index + 1) * stripeHeight
        color = FIELD_GREEN if index % 2 == 0 else FIELD_GREEN_STRIPE
        drawRect(0, worldTop + offset, app.width, stripeHeight, fill=color)
        index += 1


def drawFieldApron(app):
    leftX = app.sideLineOffset + BOUNDARY_OFFSET
    rightX = app.width - BOUNDARY_OFFSET - app.sideLineOffset
    drawRect(0, 0, leftX, app.height, fill=FIELD_APRON)
    drawRect(rightX, 0, app.width - rightX, app.height, fill=FIELD_APRON)


def drawLineOfScrimmage(app):
    offset = cameraOffset(app)
    losY = app.lineOfScrimmage + offset
    left = BOUNDARY_OFFSET + app.sideLineOffset
    right = app.width - BOUNDARY_OFFSET - app.sideLineOffset
    drawLine(left, losY, right, losY, fill=LOS_COLOR, lineWidth=LOS_WIDTH)
    tick = LOS_TICK_HALF
    for hashX in (leftHashX(app), rightHashX(app)):
        drawLine(hashX, losY - tick, hashX, losY + tick,
                 fill=LOS_COLOR, lineWidth=LOS_WIDTH)


def drawYardLines(app):
    offset = cameraOffset(app)
    yardMarkerCount = 1
    lineCount = 0
    leftEdge = 30 + app.sideLineOffset
    rightEdge = app.width - 30 - app.sideLineOffset
    yardStep = app.yardStep
    if yardStep <= 0:
        return
    worldY = float(app.height)
    while worldY > 0:
        lineCount += 1
        y = worldY + offset
        if lineCount % 5 == 0:
            drawMajorYardLine(app, leftEdge, rightEdge, y, lineCount,
                              yardMarkerCount)
            if lineCount % 10 == 0:
                yardMarkerCount += 1
        else:
            drawHashMarks(app, leftEdge, rightEdge, y)
        worldY -= yardStep


def drawMajorYardLine(app, leftEdge, rightEdge, y, lineCount, yardMarkerCount):
    isTenYard = lineCount % 10 == 0
    color = YARD_LINE_MAJOR if isTenYard else YARD_LINE_MINOR
    width = YARD_LINE_MAJOR_WIDTH if isTenYard else YARD_LINE_MINOR_WIDTH
    drawLine(leftEdge, y, rightEdge, y, fill=color, lineWidth=width)
    if not isTenYard:
        return
    drawLabel(f'{yardMarkerCount} 0', 60 + app.sideLineOffset, y,
              size=YARD_NUMBER_SIZE, fill=YARD_NUMBER_COLOR, rotateAngle=90)
    drawLabel(f'{yardMarkerCount} 0', app.width - 60 - app.sideLineOffset, y,
              size=YARD_NUMBER_SIZE, fill=YARD_NUMBER_COLOR, rotateAngle=270)


def drawHashMarks(app, leftEdge, rightEdge, y):
    mark = HASH_MARK_LENGTH
    drawLine(leftEdge, y, leftEdge + mark, y, fill=HASH_MARK_COLOR)
    drawLine(rightEdge, y, rightEdge - mark, y, fill=HASH_MARK_COLOR)
    drawLine(leftHashX(app), y, leftHashX(app) + mark, y, fill=HASH_MARK_COLOR)
    drawLine(rightHashX(app), y, rightHashX(app) + mark, y, fill=HASH_MARK_COLOR)


def drawSidelines(app):
    leftX = app.sideLineOffset + BOUNDARY_OFFSET
    rightX = app.width - BOUNDARY_OFFSET - app.sideLineOffset
    drawLine(leftX, 0, leftX, app.height, fill='white', lineWidth=SIDELINE_WIDTH)
    drawLine(rightX, 0, rightX, app.height, fill='white', lineWidth=SIDELINE_WIDTH)
