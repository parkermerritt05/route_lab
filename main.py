from cmu_graphics import *
from app.lifecycle import onAppStart
from ui.draw import redrawAll
from ui.input import (onMouseMove, onMouseDrag, onMousePress, onMouseRelease,
                      onKeyPress, onKeyHold, onKeyRelease, onStep)
from ui.layout import onResize

def main():
    runApp()

main()
