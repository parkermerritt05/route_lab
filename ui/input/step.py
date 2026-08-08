from simulation.collisions import handleCollisions
from simulation.tick import moveDefense, moveOffense


def onStep(app):
    app.animationTicks += 1
    if app.isPaused:
        return
    elif app.isField:
        takeStep(app)


def takeStep(app):
    app.steps += 1
    app.playIsActive = True
    if app.throwing:
        app.ballVelocity += 0.3
        if app.ballVelocity >= app.maxBallVelo:
            app.ballVelocity = app.maxBallVelo
    app.yardsRan = (app.velocity * app.steps) / app.yardStep
    if app.playResult == '':
        moveDefense(app)
        moveOffense(app)
        handleCollisions(app)
    else:
        app.throwing = False
    app.ball.updateBallPosition(app)
