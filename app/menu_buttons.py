from ui.buttons import (Button, ExportImportButton, FormationButton,
                        InstructionButton, RouteButton, StartButton,
                        StatsButton)


def loadOffensiveMenuButtons(app):
    app.offensiveFormationButtons = [
        FormationButton(95, 80, 130, 65, "Single Back", app.singleBack),
        FormationButton(95, 170, 130, 65, "Shotgun", app.shotgun),
        FormationButton(95, 260, 130, 65, "Spread", app.spread),
        FormationButton(95, 350, 130, 65, "Bunch", app.bunch),
        FormationButton(95, 440, 130, 65, "Custom", app.custom),
    ]
    app.menuInstructionsButton = InstructionButton(105, 538, 175, 50,
                                                   "Toggle Instructions")
    app.fieldInstructionsButton = InstructionButton(app.width - 100, 50, 180, 40,
                                                    'Toggle Instructions')
    app.offensiveWRRouteButtons = [
        RouteButton(app.width - 95, 50, 130, 35, "Crossing", app.wrRouteList[0:2]),
        RouteButton(app.width - 95, 110, 130, 35, "Slant", app.wrRouteList[2:4]),
        RouteButton(app.width - 95, 170, 130, 35, "Quick Out", app.wrRouteList[4:6]),
        RouteButton(app.width - 95, 230, 130, 35, "Shallow Dig", app.wrRouteList[6:8]),
        RouteButton(app.width - 95, 290, 130, 35, "Deep Dig", app.wrRouteList[8:10]),
        RouteButton(app.width - 95, 350, 130, 35, "Shallow Out", app.wrRouteList[10:12]),
        RouteButton(app.width - 95, 410, 130, 35, "Deep Out", app.wrRouteList[12:14]),
        RouteButton(app.width - 95, 470, 130, 35, "Shallow Hitch", app.wrRouteList[14:16]),
        RouteButton(app.width - 95, 530, 130, 35, "Deep Hitch", app.wrRouteList[16:18]),
        RouteButton(app.width - 95, 590, 130, 35, "Post", app.wrRouteList[18:20]),
        RouteButton(app.width - 95, 650, 130, 35, "Corner", app.wrRouteList[20:22]),
        RouteButton(app.width - 95, 710, 130, 35, "Go",
                    [app.wrRouteList[22], app.wrRouteList[22]]),
    ]
    app.startGameButton = StartButton(app.width // 2, 650, 300, 150, "Start Game")
    app.offensiveRBRouteButtons = [
        RouteButton(app.width - 95, 50, 130, 35, "RB Out", app.rbRouteList[0:2]),
        RouteButton(app.width - 95, 110, 130, 35, "RB Zone Sit",
                    [app.rbRouteList[2], app.rbRouteList[2]]),
    ]
    app.importButton = ExportImportButton(app.sideLineOffset // 2,
                                          app.height - 120, 150, 50, "Import Play", dict())
    app.exportButton = ExportImportButton(app.sideLineOffset // 2,
                                          app.height - 45, 150, 50, "Export Play", dict())


def loadFieldButtons(app):
    resetButton = Button(app.sideLineOffset // 2, 40, 100, 50, "Reset")
    menuButton = Button(app.sideLineOffset // 2, 110, 100, 50, "Menu")
    app.coverageButton = Button(app.sideLineOffset // 2, 500, 150, 50, "Coverage: C1")
    app.fieldButtons = [resetButton, menuButton]


def loadStats(app):
    app.numCompletions = 0
    app.attempts = 0
    app.totalYards = 0
    app.ints = 0
    app.qbRun = True
    app.statsButton = StatsButton(app.width - 100, 130, 130, 40, 'Stats')
