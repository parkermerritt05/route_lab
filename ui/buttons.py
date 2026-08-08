from cmu_graphics import drawLabel, drawRect
from constants import (BUTTON_GREEN, BUTTON_OUTLINE_COLOR, BUTTON_OUTLINE_PAD_X,
                       BUTTON_OUTLINE_PAD_Y, BUTTON_PRESS_SHIFT,
                       DISABLED_LABEL_COLOR, DISABLED_OVERLAY_COLOR,
                       DISABLED_OVERLAY_OPACITY, ENABLED_LABEL_COLOR,
                       EXPORT_IMPORT_BUTTON_GREEN, HOVER_OVERLAY_COLOR,
                       HOVER_OVERLAY_OPACITY, INSTRUCTION_BUTTON_GREEN,
                       PANEL_CLOSE_HALF, PANEL_CLOSE_INSET, PRESS_OVERLAY_COLOR,
                       PRESS_OVERLAY_OPACITY, ROUTE_ACTIVE_BORDER,
                       ROUTE_ACTIVE_BORDER_WIDTH, ROUTE_ICON_BOX,
                       ROUTE_ICON_MARGIN, ROUTE_LABEL_SHIFT, ROUTE_LABEL_SIZE,
                       START_BUTTON_RED, STATS_BUTTON_GREEN)
from ui.route_icons import drawRouteIcon


class Button:
    def __init__(self, cx, cy, w, h, text, fillColor=BUTTON_GREEN, labelSize=18):
        self.cx = cx
        self.cy = cy
        self.w = w
        self.h = h
        self.text = text
        self.fillColor = fillColor
        self.labelSize = labelSize
        self.hovered = False
        self.pressed = False
        self.enabled = True

    def contains(self, mx, my):
        return ((self.cx - self.w // 2) <= mx <= (self.cx + self.w // 2) and
                (self.cy - self.h // 2) <= my <= (self.cy + self.h / 2))

    def isClicked(self, mx, my):
        return self.enabled and self.contains(mx, my)

    def updateHover(self, mx, my):
        self.hovered = self.enabled and self.contains(mx, my)

    def drawnCenter(self):
        if self.pressed:
            return self.cx + BUTTON_PRESS_SHIFT, self.cy + BUTTON_PRESS_SHIFT
        return self.cx, self.cy

    def draw(self):
        cx, cy = self.drawnCenter()
        self.drawOutline(cx, cy)
        drawRect(cx, cy, self.w, self.h, fill=self.fillColor, align='center')
        self.drawStateOverlay(cx, cy)
        self.drawContent(cx, cy)

    def drawOutline(self, cx, cy):
        if self.pressed:
            return
        drawRect(cx, cy, self.w + BUTTON_OUTLINE_PAD_X, self.h + BUTTON_OUTLINE_PAD_Y,
                 fill=BUTTON_OUTLINE_COLOR, align='center')

    def drawStateOverlay(self, cx, cy):
        if not self.enabled:
            self.drawOverlay(cx, cy, DISABLED_OVERLAY_COLOR, DISABLED_OVERLAY_OPACITY)
        elif self.pressed:
            self.drawOverlay(cx, cy, PRESS_OVERLAY_COLOR, PRESS_OVERLAY_OPACITY)
        elif self.hovered:
            self.drawOverlay(cx, cy, HOVER_OVERLAY_COLOR, HOVER_OVERLAY_OPACITY)

    def drawOverlay(self, cx, cy, color, opacity):
        drawRect(cx, cy, self.w, self.h, fill=color, opacity=opacity, align='center')

    def labelColor(self):
        return ENABLED_LABEL_COLOR if self.enabled else DISABLED_LABEL_COLOR

    def drawContent(self, cx, cy):
        drawLabel(self.text, cx, cy, size=self.labelSize,
                  bold=self.hovered and self.enabled, fill=self.labelColor(),
                  align='center')


class FormationButton(Button):
    def __init__(self, cx, cy, w, h, text, formation):
        super().__init__(cx, cy, w, h, text)
        self.formation = formation

    def resetFormation(self, app, formation):
        self.formation = formation


class RouteButton(Button):
    def __init__(self, cx, cy, w, h, text, routes):
        super().__init__(cx, cy, w, h, text, labelSize=ROUTE_LABEL_SIZE)
        self.leftRoute = routes[0]
        self.rightRoute = routes[1]
        self.iconRoute = routes[1]
        self.active = False

    def drawContent(self, cx, cy):
        iconCenterX = cx - self.w // 2 + ROUTE_ICON_MARGIN
        drawRouteIcon(iconCenterX, cy, ROUTE_ICON_BOX, self.iconRoute, self.labelColor())
        drawLabel(self.text, cx + ROUTE_LABEL_SHIFT, cy, size=self.labelSize,
                  bold=self.hovered and self.enabled, fill=self.labelColor(),
                  align='center')
        if self.active:
            drawRect(cx, cy, self.w, self.h, fill=None,
                     border=ROUTE_ACTIVE_BORDER, borderWidth=ROUTE_ACTIVE_BORDER_WIDTH,
                     align='center')


class InstructionButton(Button):
    def __init__(self, cx, cy, w, h, text):
        super().__init__(cx, cy, w, h, text, fillColor=INSTRUCTION_BUTTON_GREEN)
        self.isInstructions = False


class StartButton(Button):
    def __init__(self, cx, cy, w, h, text):
        super().__init__(cx, cy, w, h, text,
                         fillColor=START_BUTTON_RED, labelSize=48)


class ExportImportButton(Button):
    def __init__(self, cx, cy, w, h, text, data):
        super().__init__(cx, cy, w, h, text, fillColor=EXPORT_IMPORT_BUTTON_GREEN)
        self.data = data


class StatsButton(Button):
    def __init__(self, cx, cy, w, h, text):
        super().__init__(cx, cy, w, h, text, fillColor=STATS_BUTTON_GREEN)
        self.isStats = False


def visibleButtons(app):
    if getattr(app, 'isOffensiveMenu', False):
        routeButtons = (app.offensiveWRRouteButtons if app.isWRMenu
                        else app.offensiveRBRouteButtons)
        return (list(app.offensiveFormationButtons) + list(routeButtons)
                + [app.startGameButton, app.importButton, app.exportButton,
                   app.menuInstructionsButton])
    if getattr(app, 'isField', False):
        return (list(app.fieldButtons) + [app.coverageButton, app.exportButton,
                app.fieldInstructionsButton, app.statsButton])
    return []


def panelCloseCenter(panelCx, panelCy, panelW, panelH):
    return (panelCx + panelW // 2 - PANEL_CLOSE_INSET,
            panelCy - panelH // 2 + PANEL_CLOSE_INSET)


def panelCloseContains(mx, my, closeCx, closeCy):
    half = PANEL_CLOSE_HALF
    return (closeCx - half <= mx <= closeCx + half and
            closeCy - half <= my <= closeCy + half)


def releasePressedButton(app):
    if app.pressedButton is not None:
        app.pressedButton.pressed = False
        app.pressedButton = None
