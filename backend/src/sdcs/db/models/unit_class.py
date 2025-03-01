from enum import Enum

class UnitClass(str, Enum):
    STANDARD = "STANDARD"
    JTAC = "JTAC"
    SHELTER = "SHELTER"
    CARGO = "CARGO"
    STATIC = "STATIC"
    AMMO = "AMMO"
    FUEL = "FUEL"
    NONE = "NONE"
    FARP_UTIL = "FARP_UTIL"
    SHELTER_BUILD = "SHELTER_BUILD"
    EWR = "EWR"
    LOGISTIC = "LOGISTIC"
    AIR = "AIR"
    AIR_RW = "AIR_RW"
    AIR_INTEL = "AIR_INTEL"
    FACTORY = "FACTORY"
    JTAC_TOWER = "JTAC_TOWER"
    COMPOSITION_BUILD = "COMPOSITION_BUILD"
    UNPACKABLE = "UNPACKABLE"
    FACTORY_BUILD = "FACTORY_BUILD"
    MOBILE_EWR = "MOBILE_EWR"
    MANPAD = "MANPAD"
    FATCOW = "FATCOW"
    COMPOSITION_TRUCK = "COMPOSITION_TRUCK"
    COMPOSITION_TRUCK_BUILD = "COMPOSITION_TRUCK_BUILD"
    REARM_FARP = "REARM_FARP"
    OBJECTIVE = "OBJECTIVE"
