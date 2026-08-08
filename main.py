from cmu_graphics import *
from init import onAppStart
from drawing import redrawAll
from handlers import (onMouseMove, onMouseDrag, onMousePress, onMouseRelease,
                      onKeyPress, onKeyHold, onStep)
from layout import onResize

def main():
    runApp()

main()