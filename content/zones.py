from constants import BOUNDARY_OFFSET
from domain import Zone


def loadZones(app):
    fieldLeft = app.sideLineOffset + BOUNDARY_OFFSET
    fieldRight = app.width - app.sideLineOffset - BOUNDARY_OFFSET
    fieldWidth = fieldRight - fieldLeft
    fieldMid = (fieldLeft + fieldRight) / 2
    los = app.lineOfScrimmage
    yard = app.yardStep
    zones = dict()

    zones['middleDeep'] = Zone(fieldWidth / 5 + fieldLeft,
                               fieldRight - fieldWidth / 5, 0,
                               los - 10 * yard,
                               fieldMid,
                               los - 12 * yard)
    zones['middleIntermediate'] = Zone(fieldWidth // 3 + fieldLeft,
                                       fieldRight - fieldWidth // 3,
                                       los - 9 * yard,
                                       los - 3 * yard)
    zones['leftDeepHalf'] = Zone(fieldLeft, fieldMid, 0,
                                 los - 8 * yard,
                                 fieldLeft + fieldWidth * 0.25,
                                 los - 12 * yard)
    zones['rightDeepHalf'] = Zone(fieldMid, fieldRight, 0,
                                  los - 8 * yard,
                                  fieldLeft + fieldWidth * 0.75,
                                  los - 12 * yard)
    zones['leftFlat'] = Zone(fieldLeft,
                             fieldLeft + fieldWidth * 0.28,
                             los - 8 * yard,
                             los + 2 * yard,
                             fieldLeft + fieldWidth * 0.14,
                             los - 3.5 * yard)
    zones['rightFlat'] = Zone(fieldRight - fieldWidth * 0.28,
                              fieldRight,
                              los - 8 * yard,
                              los + 2 * yard,
                              fieldLeft + fieldWidth * 0.86,
                              los - 3.5 * yard)
    zones['leftHook'] = Zone(fieldLeft + fieldWidth * 0.18,
                             fieldMid,
                             los - 10 * yard,
                             los - 2 * yard,
                             fieldLeft + fieldWidth * 0.36,
                             los - 6 * yard)
    zones['middleHook'] = Zone(fieldLeft + fieldWidth * 0.36,
                               fieldRight - fieldWidth * 0.36,
                               los - 11 * yard,
                               los - 3 * yard,
                               fieldMid,
                               los - 6.5 * yard)
    zones['rightHook'] = Zone(fieldMid,
                              fieldRight - fieldWidth * 0.18,
                              los - 10 * yard,
                              los - 2 * yard,
                              fieldLeft + fieldWidth * 0.64,
                              los - 6 * yard)
    app.zones = zones
