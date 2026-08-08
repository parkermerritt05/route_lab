from domain import (CornerBack, LineBacker, RunningBack, Safety, TightEnd,
                    WideReceiver, getPlayersOfType)
from coverage.cover_two import buildDLine


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
    los = app.lineOfScrimmage
    for i in range(totalLBs):
        linebacker = coverage[f"LB{i+1}"]
        xCoord = 2 * app.width // 5 + (i + 1) * (app.width // 5) // (totalLBs + 1)
        linebacker.cx, linebacker.cy = xCoord, los - app.yardStep * 4
