from constants import (DEFENSIVE_END_LEFT_FRACTION, DEFENSIVE_END_RIGHT_FRACTION,
                       DEFENSIVE_TACKLE_LEFT_FRACTION,
                       DEFENSIVE_TACKLE_RIGHT_FRACTION, DLINE_DEPTH_PX)
from domain import (CornerBack, DefensiveEnd, DefensiveTackle, LineBacker,
                    RunningBack, Safety, TightEnd, WideReceiver,
                    getPlayersOfType)


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
