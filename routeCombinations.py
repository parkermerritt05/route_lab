# Base route concepts applied when each formation is built.
# Names match RouteButton labels so the menu highlights stay in sync.

WR_PAIRS = (
    ("Crossing", 0, 2),
    ("Slant", 2, 4),
    ("Quick Out", 4, 6),
    ("Shallow Dig", 6, 8),
    ("Deep Dig", 8, 10),
    ("Shallow Out", 10, 12),
    ("Deep Out", 12, 14),
    ("Shallow Hitch", 14, 16),
    ("Deep Hitch", 16, 18),
    ("Post", 18, 20),
    ("Corner", 20, 22),
)

# Formation -> classic concept name (for UI / docs).
COMBINATION_NAMES = {
    "singleBack": "Smash",
    "shotgun": "Mesh",
    "spread": "Sail",
    "bunch": "Levels",
    "custom": "Four Verts",
}


def baseCombinations():
    # Smash: outside hitch + inside corner (Cover 2 beater).
    smash = {
        "WR1": "Shallow Hitch",
        "WR2": "Corner",
        "TE": "Deep Dig",
        "WR3": "Go",
        "RB": "RB Zone Sit",
    }
    # Mesh: slot + TE cross; outside clear / dig (man beater).
    mesh = {
        "WR1": "Go",
        "WR2": "Crossing",
        "TE": "Crossing",
        "WR3": "Deep Dig",
        "RB": "RB Zone Sit",
    }
    # Sail / flood: go + deep out + RB flat (Cover 3 vertical stretch).
    sail = {
        "WR1": "Post",
        "WR2": "Crossing",
        "WR3": "Deep Out",
        "WR4": "Go",
        "RB": "RB Out",
    }
    # Levels from bunch: stacked depths to the trips side.
    levels = {
        "WR1": "Shallow Dig",
        "WR2": "Deep Dig",
        "WR3": "Corner",
        "WR4": "Go",
        "RB": "RB Zone Sit",
    }
    # Four verts: vertical stretch across the field.
    fourVerts = {
        "WR1": "Go",
        "WR2": "Go",
        "WR3": "Go",
        "WR4": "Go",
        "RB": "RB Zone Sit",
    }
    return {
        "singleBack": smash,
        "shotgun": mesh,
        "spread": sail,
        "bunch": levels,
        "custom": fourVerts,
    }


def applyBaseCombinations(app):
    app.combinationNames = dict(COMBINATION_NAMES)
    for formationName, combo in baseCombinations().items():
        formation = getattr(app, formationName)
        applyCombination(app, formation, combo)


def applyCombination(app, formation, combo):
    for position, routeName in combo.items():
        player = formation[position]
        route = resolveRoute(app, player, routeName)
        player.route = player.translateRoute(app, route)
        player.routeName = routeName
        player.targetX = player.cx + route[0][0] * app.yardStep
        player.targetY = player.cy + route[0][1] * app.yardStep


def resolveRoute(app, player, routeName):
    leftRoute, rightRoute = routePair(app, routeName)
    if player.cx <= app.width // 2:
        return leftRoute
    return rightRoute


def routePair(app, routeName):
    if routeName == "RB Out":
        return app.rbRouteList[0], app.rbRouteList[1]
    if routeName == "RB Zone Sit":
        sit = app.rbRouteList[2]
        return sit, sit
    if routeName == "Go":
        go = app.wrRouteList[22]
        return go, go
    for name, start, end in WR_PAIRS:
        if name == routeName:
            return app.wrRouteList[start], app.wrRouteList[end - 1]
    raise ValueError(f"Unknown route name: {routeName}")
