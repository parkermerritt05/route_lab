from cmu_graphics import *
from classes import *
from init import resetApp
import json

def importData(app):
    print('importing')
    app.dataPath = app.getTextInput('Input Play File Path')
    try: 
        with open(app.dataPath, 'r') as file:
            formation = json.load(file)
    except FileNotFoundError:
        app.importButton.text = "File Not Found"
        print('Invalid File')
        return
    if not isinstance(formation, dict): 
        print('Error: Invalid Player Data')
        return
    formationRes = dict()
    for position in formation:
        if "WR" in position or "RB" in position or "TE" in position:
            isLegal = checkLegalSkillPlayer(formation, position)
            if not isLegal:
                app.importButton.text = "Invalid Data"
                print('Error: Invalid Skill Player Data')
                return
            playerInfo = formation[position]
            route = playerInfo["route"]
            if "WR" in position:
                formationRes[position] = WideReceiver(app, playerInfo["cx"],
                            playerInfo["cy"],dx = playerInfo["dx"], 
                            dy = playerInfo["dy"], route=route, translated = True)
            elif "RB" in position:
                formationRes[position] = RunningBack(app, playerInfo["cx"],
                            playerInfo["cy"],dx = playerInfo["dx"], 
                            dy = playerInfo["dy"], route=route, translated = True)
            elif "TE" in position:
                formationRes[position] = TightEnd(app, playerInfo["cx"],
                            playerInfo["cy"],dx = playerInfo["dx"], 
                            dy = playerInfo["dy"], route=route, translated = True)
        else:
            isLegal = checkLegalNormalPlayer(formation, position)
            if not isLegal:
                app.importButton.text = "Invalid Data"
                print('Error: Invalid Normal Player Data')
                return
            playerInfo = formation[position]
            if "QB" in position:
                formationRes[position] = Quarterback(playerInfo["cx"],
                            playerInfo["cy"], dx = playerInfo["dx"], 
                            dy = playerInfo["dy"])
            else:
                formationRes[position] = Lineman(playerInfo["cx"],
                            playerInfo["cy"], dx = playerInfo["dx"], 
                            dy =playerInfo["dy"])
    app.importButton.text = "Imported!"
    app.custom = formationRes
    app.offensiveFormationButtons[4].resetFormation(app, formationRes)
    app.oFormation = app.custom

def exportData(app, isField=True):
    if not isField:
        resetApp(app, isField = False)
    else:
        resetApp(app)
    playDict = dict()
    dx = dy = 0
    for position in app.oFormation:
        player = app.oFormation[position]
        if "WR" in position or "RB" in position or "TE" in position:
            playDict[position] = {"cx": player.cx, "cy":player.cy, 
                                "dx": dx, "dy":dy, 
                                "route": player.route}
        else:
            playDict[position] = {"cx": player.cx, "cy":player.cy, 
                                "dx": dx, "dy":dy}
    with open(f"routeLabPlay{app.indexExport}.json", "w") as file:
        json.dump(playDict, file, indent=2)
    app.indexExport+=1
    app.exportButton.text = "Exported!"

##################################
### Import/Export Data Helpers ###
##################################

def checkLegalSkillPlayer(formation, position):
    playerInfo = formation[position]
    return ("cx" in playerInfo and "cy" in playerInfo and 
            "dx" in playerInfo and "dy" in playerInfo and
            "route" in playerInfo and
            len(formation[position]) == 5)

def checkLegalNormalPlayer(formation, position):
    playerInfo = formation[position]
    return ("cx" in playerInfo and "cy" in playerInfo and 
            "dx" in playerInfo and "dy" in playerInfo and
            len(formation[position]) == 4)
