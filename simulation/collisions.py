from constants import (COLLISION_OVERLAP_THRESHOLD, COLLISION_PUSH,
                       PLAYER_COLLISION_RADIUS)
from simulation.geometry import distance


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
