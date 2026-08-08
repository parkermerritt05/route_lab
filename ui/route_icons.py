import math
from cmu_graphics import drawCircle, drawLine
from constants import (ROUTE_ICON_ARROW_MAX_SEGMENT_RATIO, ROUTE_ICON_ARROW_SIZE,
                       ROUTE_ICON_ARROW_SPREAD, ROUTE_ICON_START_DOT_RADIUS)
from simulation.geometry import distance


def routeWaypoints(route):
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
