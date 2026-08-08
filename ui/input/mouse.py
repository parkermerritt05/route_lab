from ui.buttons import releasePressedButton, visibleButtons
from ui.input.field_controls import handleFieldClick
from ui.input.selection import handleMenuClick, inStartButton


def onMouseMove(app, mx, my):
    if app.isMainMenu:
        app.isMainMenuLabelHovering = inStartButton(app, mx, my)
        return
    for button in visibleButtons(app):
        button.updateHover(mx, my)


def onMousePress(app, mx, my):
    app.exportButton.text = "Export Play"
    app.importButton.text = "Import Play"
    app.routeDragBegan = False
    app.routeAwaitingExit = False
    app.pendingDeselect = None
    pressButtonUnderCursor(app, mx, my)
    if app.isMainMenu:
        handleMainMenuClick(app, mx, my)
    elif app.isField:
        handleFieldClick(app, mx, my)
    elif app.isOffensiveMenu:
        handleMenuClick(app, mx, my)


def pressButtonUnderCursor(app, mx, my):
    for button in visibleButtons(app):
        if button.enabled and button.contains(mx, my):
            button.pressed = True
            app.pressedButton = button
            return


def handleMainMenuClick(app, mx, my):
    if inStartButton(app, mx, my):
        app.isMainMenuLabelHovering = False
        app.isMainMenu = False
        app.isOffensiveMenu = True
