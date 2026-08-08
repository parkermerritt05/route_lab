from content.combinations import applyBaseCombinations
from domain import (Ball, Lineman, Quarterback, RunningBack, TightEnd,
                    WideReceiver)
from ui.layout import losY, midX


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
    applyBaseCombinations(app)
    app.ball = Ball(app.oFormation['C'].cx, app.oFormation['C'].cy,
                    app.oFormation['C'])
