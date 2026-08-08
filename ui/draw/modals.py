from cmu_graphics import drawLabel, drawLine, drawRect
from constants import (HUD_PANEL_BORDER, HUD_PANEL_BORDER_WIDTH, HUD_TEXT_COLOR,
                       INSTR_PANEL_HEIGHT, INSTR_PANEL_OFFSET_Y, INSTR_PANEL_WIDTH,
                       MODAL_BACKDROP_COLOR, MODAL_BACKDROP_OPACITY,
                       MODAL_PANEL_BORDER, MODAL_PANEL_COLOR, MODAL_PANEL_OPACITY,
                       PANEL_CLOSE_BOX, PANEL_CLOSE_BOX_OPACITY, PANEL_CLOSE_FILL,
                       PANEL_CLOSE_HALF, PANEL_CLOSE_LINE, PANEL_CLOSE_LINE_OPACITY,
                       STATS_PANEL_HEIGHT, STATS_PANEL_OFFSET_Y, STATS_PANEL_WIDTH)
from ui.buttons import panelCloseCenter


def drawGlassPanel(cx, cy, width, height, fill, opacity,
                   border=HUD_PANEL_BORDER):
    drawRect(cx, cy, width, height, fill=fill, border=border,
             borderWidth=HUD_PANEL_BORDER_WIDTH, align='center', opacity=opacity)


def drawModalBackdrop(app):
    drawRect(0, 0, app.width, app.height,
             fill=MODAL_BACKDROP_COLOR, opacity=MODAL_BACKDROP_OPACITY)


def drawPanelCloseButton(panelCx, panelCy, panelW, panelH):
    cx, cy = panelCloseCenter(panelCx, panelCy, panelW, panelH)
    half = PANEL_CLOSE_HALF
    drawRect(cx, cy, PANEL_CLOSE_BOX, PANEL_CLOSE_BOX, fill=PANEL_CLOSE_FILL,
             border=PANEL_CLOSE_LINE, borderWidth=3, align='center',
             opacity=PANEL_CLOSE_BOX_OPACITY)
    drawLine(cx - half, cy - half, cx + half, cy + half,
             fill=PANEL_CLOSE_LINE, lineWidth=2, opacity=PANEL_CLOSE_LINE_OPACITY)
    drawLine(cx - half, cy + half, cx + half, cy - half,
             fill=PANEL_CLOSE_LINE, lineWidth=2, opacity=PANEL_CLOSE_LINE_OPACITY)


def drawInstructionPanelFrame(app):
    drawModalBackdrop(app)
    panelCy = app.height // 2 - INSTR_PANEL_OFFSET_Y
    drawGlassPanel(app.width // 2, panelCy, INSTR_PANEL_WIDTH, INSTR_PANEL_HEIGHT,
                   MODAL_PANEL_COLOR, MODAL_PANEL_OPACITY, MODAL_PANEL_BORDER)
    drawLabel("Instructions:", app.width // 2, panelCy - 130, size=45, bold=True,
              fill=HUD_TEXT_COLOR)
    drawPanelCloseButton(app.width // 2, panelCy, INSTR_PANEL_WIDTH, INSTR_PANEL_HEIGHT)


def drawStatsMenu(app):
    drawModalBackdrop(app)
    centerX = app.width // 2
    baseY = app.height // 2 + STATS_PANEL_OFFSET_Y
    drawGlassPanel(centerX, baseY, STATS_PANEL_WIDTH, STATS_PANEL_HEIGHT,
                   MODAL_PANEL_COLOR, MODAL_PANEL_OPACITY, MODAL_PANEL_BORDER)
    drawPanelCloseButton(centerX, baseY, STATS_PANEL_WIDTH, STATS_PANEL_HEIGHT)
    drawLabel("Stats:", centerX, baseY - 100, size=45, bold=True,
              fill=HUD_TEXT_COLOR)
    drawLabel("Total Yards Gained: " + str(app.totalYards),
              centerX - 200, baseY - 50, size=18, bold=True, align='left',
              fill=HUD_TEXT_COLOR)
    drawLabel("Completions: " + str(app.numCompletions) + " / " + str(app.attempts),
              centerX - 200, baseY - 25, size=18, bold=True, align='left',
              fill=HUD_TEXT_COLOR)
    drawLabel("Interceptions: " + str(app.ints),
              centerX - 200, baseY, size=18, bold=True, align='left',
              fill=HUD_TEXT_COLOR)
    if app.lastPlayResult != "":
        drawLabel(f"Last Play Result: {app.lastPlayResult}",
                  centerX - 200, baseY + 25, size=18, bold=True, align='left',
                  fill=HUD_TEXT_COLOR)
        if app.lastPlayResult != 'Intercepted':
            drawLabel(f"Yards on Last Play: {app.lastYardsRan}",
                      centerX - 200, baseY + 50, size=18, bold=True, align='left',
                      fill=HUD_TEXT_COLOR)
        else:
            drawLabel("Yards on Last Play: N/A",
                      centerX - 200, baseY + 50, size=18, bold=True, align='left',
                      fill=HUD_TEXT_COLOR)
