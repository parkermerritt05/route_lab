from app.lifecycle import resetApp
from coverage.setup import initializeDefense
from play_io.import_export import exportData
from ui.input.selection import clickedInstructionClose, clickedStatsClose


def handleFieldClick(app, mx, my):
    if app.coverageButton.isClicked(mx, my):
        toggleCoverage(app)
        return
    checkFieldButtons(app, mx, my)
    if app.statsButton.isClicked(mx, my) and (app.playResult != '' or app.isPaused):
        app.statsButton.isStats = not app.statsButton.isStats
        return
    if clickedStatsClose(app, mx, my):
        app.statsButton.isStats = False
        return
    if (app.fieldInstructionsButton.isClicked(mx, my)
            and (app.playResult != '' or app.isPaused)):
        app.fieldInstructionsButton.isInstructions = not app.fieldInstructionsButton.isInstructions
        return
    if (app.playIsActive and app.ball.carrier == app.oFormation['QB']
            and app.playResult == ''):
        startThrow(app, mx, my)
    if clickedInstructionClose(app, mx, my, app.fieldInstructionsButton):
        app.fieldInstructionsButton.isInstructions = not app.fieldInstructionsButton.isInstructions
        return


def toggleCoverage(app):
    if app.playIsActive and app.playResult == '' and not app.isPaused:
        return
    app.coverageShell = 'Cover 2' if app.coverageShell == 'Cover 1' else 'Cover 1'
    app.coverageButton.text = f"Coverage: {'C2' if app.coverageShell == 'Cover 2' else 'C1'}"
    app.dFormation = initializeDefense(app)
    app.statsButton.isStats = False
    app.fieldInstructionsButton.isInstructions = False


def startThrow(app, mx, my):
    app.ballVelocity = 1
    app.qbRun = False
    app.throwing = True
    app.mouseX = mx
    app.mouseY = my


def checkFieldButtons(app, mx, my):
    if (app.exportButton.text == "Export Play" and
            app.exportButton.isClicked(mx, my)):
        exportData(app)
    for button in app.fieldButtons:
        if button.isClicked(mx, my):
            if button.text == 'Reset':
                app.isPlayActive = False
                app.statsButton.isStats = False
                app.fieldInstructionsButton.isInstructions = False
                resetApp(app)
                return
            else:
                app.importButton.text = "Import Play"
                app.isPlayActive = False
                app.menuInstructionsButton.isInstructions = False
                resetApp(app)
                app.isField = False
                app.isOffensiveMenu = True
                return
