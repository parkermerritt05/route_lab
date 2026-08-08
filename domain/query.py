def getPlayersOfType(app, playerType):
    return [player for player in app.oFormation.values()
            if isinstance(player, playerType)]
