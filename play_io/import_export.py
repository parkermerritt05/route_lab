import json
from app.lifecycle import resetApp
from domain import Lineman, Quarterback, RunningBack, TightEnd, WideReceiver

CUSTOM_FORMATION_BUTTON_INDEX = 4


def importData(app):
    app.dataPath = app.getTextInput('Input Play File Path')
    try:
        with open(app.dataPath, 'r') as file:
            formation = json.load(file)
    except FileNotFoundError:
        app.importButton.text = "File Not Found"
        return
    if not isinstance(formation, dict):
        app.importButton.text = "Invalid Data"
        return
    rebuilt = dict()
    for position in formation:
        player = buildPlayerFromData(app, formation, position)
        if player is None:
            app.importButton.text = "Invalid Data"
            return
        rebuilt[position] = player
    app.importButton.text = "Imported!"
    app.custom = rebuilt
    app.offensiveFormationButtons[CUSTOM_FORMATION_BUTTON_INDEX].resetFormation(app, rebuilt)
    app.oFormation = app.custom


def buildPlayerFromData(app, formation, position):
    if isSkillPosition(position):
        if not checkLegalSkillPlayer(formation, position):
            return None
        return buildSkillPlayer(app, formation[position], position)
    if not checkLegalNormalPlayer(formation, position):
        return None
    return buildNormalPlayer(formation[position], position)


def buildSkillPlayer(app, info, position):
    route = info["route"]
    if "WR" in position:
        skillPlayerType = WideReceiver
    elif "RB" in position:
        skillPlayerType = RunningBack
    else:
        skillPlayerType = TightEnd
    return skillPlayerType(app, info["cx"], info["cy"], dx=info["dx"],
                           dy=info["dy"], route=route, translated=True)


def buildNormalPlayer(info, position):
    if "QB" in position:
        return Quarterback(info["cx"], info["cy"], dx=info["dx"], dy=info["dy"])
    return Lineman(info["cx"], info["cy"], dx=info["dx"], dy=info["dy"])


def exportData(app, isField=True):
    resetApp(app, isField=isField)
    playDict = dict()
    dx = dy = 0
    for position in app.oFormation:
        player = app.oFormation[position]
        playDict[position] = {"cx": player.cx, "cy": player.cy, "dx": dx, "dy": dy}
        if isSkillPosition(position):
            playDict[position]["route"] = player.route
    with open(f"routeLabPlay{app.indexExport}.json", "w") as file:
        json.dump(playDict, file, indent=2)
    app.indexExport += 1
    app.exportButton.text = "Exported!"


def isSkillPosition(position):
    return "WR" in position or "RB" in position or "TE" in position


def checkLegalSkillPlayer(formation, position):
    playerInfo = formation[position]
    return ("cx" in playerInfo and "cy" in playerInfo and
            "dx" in playerInfo and "dy" in playerInfo and
            "route" in playerInfo and
            len(playerInfo) == 5)


def checkLegalNormalPlayer(formation, position):
    playerInfo = formation[position]
    return ("cx" in playerInfo and "cy" in playerInfo and
            "dx" in playerInfo and "dy" in playerInfo and
            len(playerInfo) == 4)
