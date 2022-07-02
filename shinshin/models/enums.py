import enum

__all__ = ["ArtifactType", "CharacterProperty", "Stat", "Element", "CharacterRarity", "StatEffect"]


class CharacterProperty(enum.IntEnum):
    """Character property."""

    XP = 1001
    """XP."""
    ASCENSION = 1002
    """Ascension."""
    LEVEL = 4001
    """Level."""


class Stat(enum.IntEnum):
    """Combat stat."""

    BASE_HP = 1
    """Base HP."""
    BASE_ATK = 4
    """Base ATK."""
    BASE_DEF = 7
    """Base DEF."""
    CRIT_RATE = 20
    """CRIT Rate."""
    CRIT_DMG = 22
    """CRIT DMG."""
    ENERGY_RECHARGE = 23
    """Energy Recharge."""
    HEALING_BONUS = 26
    """Healing Bonus."""
    INCOMING_HEALING_BONUS = 27
    """Incoming Healing Bonus."""
    ELEMENTAL_MASTERY = 28
    """Elemental Mastery."""
    PHYSICAL_RES = 29
    """Physical RES."""
    PHYSICAL_DMG_BONUS = 30
    """Physical DMG Bonus."""
    PYRO_DMG_BONUS = 40
    """Pyro DMG Bonus."""
    ELECTRO_DMG_BONUS = 41
    """Electro DMG Bonus."""
    HYDRO_DMG_BONUS = 42
    """Hydro DMG Bonus."""
    ANEMO_DMG_BONUS = 44
    """Anemo DMG Bonus."""
    GEO_DMG_BONUS = 45
    """Geo DMG Bonus."""
    CRYO_DMG_BONUS = 46
    """Cryo DMG Bonus."""
    PYRO_RES = 50
    """Pyro RES."""
    ELECTRO_RES = 51
    """Electro RES."""
    HYDRO_RES = 52
    """Hydro RES."""
    DENDRO_RES = 53
    """Dendro RES."""
    ANEMO_RES = 54
    """Anemo RES."""
    GEO_RES = 55
    """Geo RES."""
    CRYO_RES = 56
    """Cryo RES."""
    PYRO_ENEGRY_COST = 70
    """Pyro Enegry Cost."""
    ELECTRO_ENERGY_COST = 71
    """Electro Energy Cost."""
    HYDRO_ENERGY_COST = 72
    """Hydro Energy Cost."""
    DENDRO_ENERGY_COST = 73
    """Dendro Energy Cost."""
    ANEMO_ENERGY_COST = 74
    """Anemo Energy Cost."""
    CRYO_ENERGY_COST = 75
    """Cryo Energy Cost."""
    GEO_ENERGY_COST = 76
    """Geo Energy Cost."""
    MAX_HP = 2000
    """Max HP."""
    ATK = 2001
    """ATK."""
    DEF = 2002
    """DEF."""


class ArtifactType(str, enum.Enum):
    """Artifact position type."""

    FLOWER = "EQUIP_BRACER"
    """Flower."""
    FEATHER = "EQUIP_NECKLACE"
    """Feather."""
    SANDS = "EQUIP_SHOES"
    """Sands."""
    GOBLET = "EQUIP_RING"
    """Goblet."""
    CIRCLET = "EQUIP_DRESS"
    """Circlet."""


class StatEffect(str, enum.Enum):
    """Stat increase or decrease effect."""

    BASE_ATK = "FIGHT_PROP_BASE_ATTACK"
    """Base ATK."""
    FLAT_HP = "FIGHT_PROP_HP"
    """Flat HP."""
    FLAT_ATK = "FIGHT_PROP_ATTACK"
    """Flat ATK."""
    FLAT_DEF = "FIGHT_PROP_DEFENSE"
    """Flat DEF."""
    HP = "FIGHT_PROP_HP_PERCENT"
    """HP%."""
    ATK = "FIGHT_PROP_ATTACK_PERCENT"
    """ATK%."""
    DEF = "FIGHT_PROP_DEFENSE_PERCENT"
    """DEF%."""
    CRIT_RATE = "FIGHT_PROP_CRITICAL"
    """Crit RATE."""
    CRIT_DMG = "FIGHT_PROP_CRITICAL_HURT"
    """Crit DMG."""
    ENERGY_RECHARGE = "FIGHT_PROP_CHARGE_EFFICIENCY"
    """Energy Recharge."""
    HEALING_BONUS = "FIGHT_PROP_HEAL_ADD"
    """Healing Bonus."""
    ELEMENTAL_MASTERY = "FIGHT_PROP_ELEMENT_MASTERY"
    """Elemental Mastery."""
    PHYSICAL_DMG_BONUS = "FIGHT_PROP_PHYSICAL_ADD_HURT"
    """Physical DMG Bonus."""
    PYRO_DMG_BONUS = "FIGHT_PROP_FIRE_ADD_HURT"
    """Pyro DMG Bonus."""
    ELECTRO_DMG_BONUS = "FIGHT_PROP_ELEC_ADD_HURT"
    """Electro DMG Bonus."""
    HYDRO_DMG_BONUS = "FIGHT_PROP_WATER_ADD_HURT"
    """Hydro DMG Bonus."""
    ANEMO_DMG_BONUS = "FIGHT_PROP_WIND_ADD_HURT"
    """Anemo DMG Bonus."""
    CRYO_DMG_BONUS = "FIGHT_PROP_ICE_ADD_HURT"
    """Cryo DMG Bonus."""
    GEO_DMG_BONUS = "FIGHT_PROP_ROCK_ADD_HURT"
    """Geo DMG Bonus."""

class Element(str, enum.Enum):
    CRYO = "Ice"
    ANEMO = "Wind"
    HYDRO = "Water"
    ELECTRO = "Electric"
    PYRO = "Fire"
    GEO = "Rock"

class CharacterRarity(str, enum.Enum):
    ORANGE = "QUALITY_ORANGE"
    """5* Character."""
    PURPLE = "QUALITY_PURPLE"
    """4* Character."""
    ORANGE_SPECIAL = "QUALITY_ORANGE_SP"
    """5* Collab Character."""
    PURPLE_SPECIAL = "QUALITY_PURPLE_SP"
    """4* Collab Character."""
