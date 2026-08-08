def loadOffensiveRoutes(app):
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
    app.route = go
