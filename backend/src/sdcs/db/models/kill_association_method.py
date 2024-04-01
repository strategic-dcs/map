import enum

class KillAssociationMethod(str, enum.Enum):
    UNKNOWN = "UNKNOWN"
    KILL = "KILL"
    HIT = "HIT"
    SPLASH = "SPLASH"
    PROX = "PROX"
    PROX_BY = "PROX_BY"
    PROX_BY_TYPE = "PROX_BY_TYPE"
    PROX_TYPE = "PROX_TYPE"
    SHOT_BY = "SHOT_BY"
    SHOT_BY_TYPE = "SHOT_BY_TYPE"
    SHOOTING_ACTIVE = "SHOOTING_ACTIVE"
    SHOOTING = "SHOOTING"
    SHOOTING_NEAR = "SHOOTING_NEAR"