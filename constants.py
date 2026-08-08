from cmu_graphics import rgb

# --- Design canvas (layout scales from this size) ---
DESIGN_WIDTH = 1000
DESIGN_HEIGHT = 750
DESIGN_SIDELINE = 194
DESIGN_YARD_STEP = 20

# --- Player / ball geometry (pixels) ---
PLAYER_DRAW_RADIUS = 13
PLAYER_HIT_RADIUS = 10          # click / catch / interception proximity
PLAYER_COLLISION_RADIUS = 10
BOUNDARY_OFFSET = 20            # inset from the sideline players may occupy
TACKLE_RANGE = 15
DEFENDER_SIDELINE_CLAMP = 24    # hard screen-edge clamp for cover players

# --- Field layout (in yard-steps unless noted) ---
SCRIMMAGE_YARDS_FROM_BOTTOM = 14   # lineOfScrimmage = height - yardStep * this
CAMERA_SCROLL_YARDS = 10           # scroll once the ball is within this of the end zone
GOAL_LINE_YARDS = 85               # depth a ball carrier runs toward
DLINE_DEPTH_PX = 10                # defensive line depth above the line of scrimmage
QB_DROPBACK_YARDS = 3              # how far behind the line the QB sets up

# Defensive-line horizontal spots as fractions of the field width.
DEFENSIVE_END_LEFT_FRACTION = 205 / 500
DEFENSIVE_END_RIGHT_FRACTION = 293 / 500
DEFENSIVE_TACKLE_LEFT_FRACTION = 238 / 500
DEFENSIVE_TACKLE_RIGHT_FRACTION = 263 / 500

# --- Ball physics ---
SNAP_BALL_VELOCITY = 4
THROW_START_HEIGHT = 5
CATCH_HEIGHT = 6
DEFLECT_HEIGHT = 8
BALL_ARC_ACCELERATION = 0.01

# --- Coverage tuning ---
MAN_JAM_YARDS = 3                  # yards into the route a corner presses before bailing
MAN_BACKPEDAL_DEPTH_YARDS = 5      # cushion depth kept during the jam phase

# --- Collision resolution ---
COLLISION_OVERLAP_THRESHOLD = 7    # overlap before two players are pushed apart
COLLISION_PUSH = 0.5               # per-frame separation nudge

# --- Colors (coaching-tablet palette) ---
FIELD_GREEN = rgb(28, 138, 80)          # softer dark band (5-yard mow)
FIELD_GREEN_STRIPE = rgb(32, 146, 86)   # lighter alternating 5-yard band
FIELD_APRON = rgb(14, 88, 50)           # darker strip outside the sidelines
MOW_STRIPE_YARDS = 5                    # real-field mow stripe width
YARD_LINE_MAJOR = 'white'               # 10-yard lines
YARD_LINE_MINOR = rgb(210, 225, 215)    # 5-yard lines
HASH_MARK_COLOR = rgb(200, 215, 205)
YARD_NUMBER_COLOR = rgb(220, 235, 225)
LOS_COLOR = rgb(245, 180, 55)           # warm amber set line
LOS_WIDTH = 3
LOS_TICK_HALF = 8                       # hash ticks centered on the LOS
SIDELINE_WIDTH = 5
YARD_LINE_MAJOR_WIDTH = 2
YARD_LINE_MINOR_WIDTH = 1
HASH_MARK_LENGTH = 8
YARD_NUMBER_SIZE = 16

OFFENSE_RED = rgb(215, 80, 75)
OFFENSE_RED_SELECTED = rgb(180, 30, 50)
DEFENSE_FILL = rgb(245, 248, 250)
PLAYER_LABEL_SIZE = 9
PLAYER_LABEL_COLOR = 'white'

# Madden-style per-receiver route colors (keyed by formation position).
ROUTE_FIELD_WIDTH = 3
ROUTE_COLOR_DEFAULT = rgb(196, 148, 42)
ROUTE_COLORS_BY_POSITION = {
    'WR1': rgb(196, 148, 42),     # deep gold
    'WR2': rgb(38, 120, 128),     # steel teal
    'WR3': rgb(168, 64, 96),      # wine rose
    'WR4': rgb(56, 122, 78),      # forest sage
    'TE': rgb(176, 92, 48),       # burnt copper
    'RB': rgb(72, 78, 140),       # slate indigo
}

BALL_FILL = rgb(120, 72, 40)
BALL_LACE_COLOR = 'white'

THROW_AIM_COLOR = rgb(120, 200, 140)

# Button palette
BUTTON_GREEN = rgb(19, 130, 60)
INSTRUCTION_BUTTON_GREEN = rgb(8, 110, 40)
START_BUTTON_RED = rgb(215, 80, 75)
EXPORT_IMPORT_BUTTON_GREEN = rgb(8, 90, 35)
STATS_BUTTON_GREEN = rgb(10, 70, 25)

# Main-menu gradient and accent lines
MENU_GREEN_LIGHT = rgb(27, 150, 85)
MENU_GREEN_MID = rgb(19, 130, 60)
MENU_GREEN_DARK = rgb(10, 110, 30)
MENU_RED = rgb(215, 80, 75)
MENU_RED_ACCENT = rgb(190, 90, 70)

# --- Button styling ---
BUTTON_OUTLINE_COLOR = rgb(8, 50, 25)  # soft dark-green frame (not pure black)
BUTTON_OUTLINE_PAD_X = 7               # extra width the outline adds around the button
BUTTON_OUTLINE_PAD_Y = 4.4            # extra height the outline adds around the button
BUTTON_PRESS_SHIFT = 2                 # pixels a button sinks toward its outline when pressed
HOVER_OVERLAY_COLOR = 'white'          # translucent wash that lightens a hovered button
HOVER_OVERLAY_OPACITY = 20
PRESS_OVERLAY_COLOR = 'black'          # translucent wash that darkens a pressed button
PRESS_OVERLAY_OPACITY = 28
DISABLED_OVERLAY_COLOR = rgb(70, 70, 70)
DISABLED_OVERLAY_OPACITY = 55
DISABLED_LABEL_COLOR = rgb(210, 210, 210)
ENABLED_LABEL_COLOR = 'black'

# Small note shown under the coverage button while the beta shell is active.
COVERAGE_BETA_TEXT = 'Cover 2 is in beta'
COVERAGE_BETA_GAP = 14                  # pixels between the button's bottom edge and the note
COVERAGE_BETA_SIZE = 11
COVERAGE_BETA_COLOR = rgb(255, 235, 180)

# --- Route-button icons ---
ROUTE_ICON_BOX = 24                    # square drawing area (px) reserved for the route glyph
ROUTE_ICON_MARGIN = 20                 # distance from the button's left edge to the icon center
ROUTE_ICON_COLOR = 'black'
ROUTE_ICON_START_DOT_RADIUS = 2.5
ROUTE_ICON_ARROW_SIZE = 5               # length (px) of each arrowhead barb on a route glyph
ROUTE_ICON_ARROW_SPREAD = 0.5           # half-angle (radians) between the barbs and the shaft
ROUTE_ICON_ARROW_MAX_SEGMENT_RATIO = 0.4  # barb length capped to this fraction of the final segment
ROUTE_LABEL_SIZE = 15
ROUTE_LABEL_SHIFT = 14                 # label nudged right to make room for the icon
ROUTE_ACTIVE_BORDER = rgb(255, 215, 110)
ROUTE_ACTIVE_BORDER_WIDTH = 3

# --- Modal panels ---
MODAL_BACKDROP_COLOR = 'black'
MODAL_BACKDROP_OPACITY = 40
MODAL_PANEL_COLOR = rgb(22, 40, 32)
MODAL_PANEL_BORDER = rgb(190, 210, 195)
MODAL_PANEL_OPACITY = 90
INSTR_PANEL_WIDTH = 500
INSTR_PANEL_HEIGHT = 350
INSTR_PANEL_OFFSET_Y = 175              # panel center sits this far above screen middle
STATS_PANEL_WIDTH = 500
STATS_PANEL_HEIGHT = 270
STATS_PANEL_OFFSET_Y = 200              # panel center sits this far below screen middle

# Shared close ("x") button for modal panels.
PANEL_CLOSE_INSET = 28                  # distance from the panel's top-right corner to the x center
PANEL_CLOSE_HALF = 10                   # half-size of the clickable box and the drawn cross
PANEL_CLOSE_BOX = 20
PANEL_CLOSE_FILL = rgb(40, 55, 45)
PANEL_CLOSE_LINE = rgb(210, 220, 210)
PANEL_CLOSE_BOX_OPACITY = 70
PANEL_CLOSE_LINE_OPACITY = 90

# --- On-field heads-up display ---
HUD_TOP_Y = 44                         # vertical center of the top-center readout/banner
HUD_BOTTOM_MARGIN = 28                 # distance of the pause hint above the screen bottom
HUD_TEXT_COLOR = 'white'
HUD_PANEL_COLOR = rgb(22, 40, 32)
HUD_PANEL_BORDER = rgb(200, 220, 205)
HUD_PANEL_BORDER_WIDTH = 1
HUD_PANEL_OPACITY = 82
LIVE_YARDS_WIDTH = 150
LIVE_YARDS_HEIGHT = 40
RESULT_BANNER_WIDTH = 300
RESULT_BANNER_HEIGHT = 60
RESULT_BANNER_OPACITY = 92
BANNER_GAIN_COLOR = rgb(24, 110, 65)
BANNER_LOSS_COLOR = rgb(175, 55, 55)
PAUSE_HINT_WIDTH = 260
PAUSE_HINT_HEIGHT = 34
PAUSE_HINT_OPACITY = 78

# --- Throw power meter ---
POWER_BAR_WIDTH = 200
POWER_BAR_HEIGHT = 16
POWER_BAR_BOTTOM_MARGIN = 46
POWER_BAR_TRACK_COLOR = rgb(22, 40, 32)
POWER_BAR_TRACK_OPACITY = 80
POWER_BAR_BORDER = rgb(200, 220, 205)
POWER_BAR_FILL_LOW = rgb(60, 200, 90)
POWER_BAR_FILL_HIGH = rgb(220, 70, 60)
POWER_BAR_FULL_THRESHOLD = 0.85        # fraction of max velocity that turns the bar "hot"

# --- Main-menu animation ---
MENU_NODE_BASE_RADIUS = 18
MENU_NODE_PULSE_AMPLITUDE = 3
MENU_NODE_PULSE_SPEED = 0.12           # radians of pulse advanced per animation tick
