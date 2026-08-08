from content.zones import loadZones
from coverage.cover_one import initializeCoverOne
from coverage.cover_two import initializeCoverTwo


def loadDefensiveFormations(app):
    loadZones(app)
    app.dFormation = initializeDefense(app)


def initializeDefense(app):
    if app.coverageShell == 'Cover 2':
        return initializeCoverTwo(app)
    return initializeCoverOne(app)
