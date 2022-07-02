from __future__ import annotations
import typing

import apimodel

from shinshin import client

from .enums import *

__all__ = [
    "Artifact",
    "BaseEquipment",
    "Character",
    "EnkaUser",
    "EquipmentStat",
    "Model",
    "PartialCharacter",
    "Player",
    "Property",
    "Weapon",
]

CHARACTER_DATA: typing.Mapping[str, typing.Mapping[str, object]] = {}

def to_icon(key: str) -> str:
    return f"https://enka.network/ui/{key}.png"

    
    

class Model(apimodel.LocalizedAPIModel):
    _client: client.Client = apimodel.Extra(NotImplemented)
    locale: str = apimodel.Extra("EN")


class Property(Model):
    type: int  # TODO: Enum
    """ID of property type."""

    ival: int
    """Integer property value."""

    val: typing.Optional[int] = None
    """Property value."""


class EquipmentStat(Model):
    id: StatEffect = apimodel.Field(name="appendPropId")
    """Stat ID."""
    
    @property
    def stat_id(self) -> str:
        return self.id.value
    
    @property
    def stat_name(self) -> str:
        return self.__class__.i18n[self.locale].get(self.id.value, self.id.value[11:].replace("_", " ").title())

    value: int = apimodel.Field(name="statValue")
    """Stat value."""

    @apimodel.root_validator(order=apimodel.Order.INITIAL_ROOT)
    def __rename_main_prop(self, values: typing.Dict[str, object]) -> typing.Dict[str, object]:
        """Rename mainPropId to appendPropId."""
        if prop := values.get("mainPropId"):
            values["appendPropId"] = prop

        return values


class BaseEquipment(Model):
    id: int = apimodel.Field(name="itemId")
    """Equipment ID."""

    level: int
    """Equipment level."""

    _name_hash: str = apimodel.Field(None, name="nameTextMapHash")
    """Equipment name hash."""
    
    @property
    def name(self) -> str:
        return self.__class__.i18n[self.locale].get(self._name_hash, self._name_hash)

    rarity: int = apimodel.Field(None, name="rankLevel")
    """Equipment rarity."""

    item_type: str = apimodel.Field(None, name="itemType")
    """Equipment type."""

    icon: str = apimodel.Field(name="icon", validator=to_icon)
    """Icon name."""


class Artifact(BaseEquipment):
    # without mainPropId

    _set_hash: str = apimodel.Field(None, name="setNameTextMapHash")
    """Equipment set name hash."""
    
    @property
    def set_name(self) -> str:
        return self.__class__.i18n[self.locale][self._set_hash]

    mainstat: EquipmentStat = apimodel.Field(None, name="reliquaryMainstat")
    """Artifact main stat."""

    substats: typing.Sequence[EquipmentStat] = apimodel.Field(None, name="reliquarySubstats")
    """Artifact substats."""

    stat_ids: typing.Sequence[int] = apimodel.Field(None, name="appendPropIdList")
    """Stat IDs."""

    type: ArtifactType = apimodel.Field(None, name="equipType")
    """Artifact position type."""


class Weapon(BaseEquipment):
    ascension: int = apimodel.Field(name="promoteLevel")
    """Ascension level."""

    refinement: typing.Mapping[int, int] = apimodel.Field(name="affixMap")
    """Refinement level."""

    stats: typing.Sequence[EquipmentStat] = apimodel.Field(None, name="weaponStats")
    """Weapon stats."""


class PartialCharacter(Model):
    id: str = apimodel.Field(name="avatarId")
    """Character ID."""

    level: typing.Optional[int] = apimodel.Field(None)
    """Character level"""

    outfit_id: typing.Optional[int] = apimodel.Field(None, name="costumeId")
    """Character skin ID."""
    
    # cached:
    
    element: Element = apimodel.Field(name="Element")
    """Character Element."""
    
    constellation_icons: typing.Sequence[str] = apimodel.Field(name="Consts")
    """Character constellations icons."""
    
    talent_id_order: typing.Sequence[int] = apimodel.Field(name="SkillOrder")
    """Character talent ID order."""
    
    talent_icons: typing.Sequence[str] = apimodel.Field(name="Skills")
    """Character talent icons."""
    
    unlocked_talent_map: typing.Mapping[int, int] = apimodel.Field(name="ProudMap")
    """I have no idea what this is, sorry."""
    
    _name_hash: str = apimodel.Field(name="NameTextMapHash")
    """Character name hash."""
    
    @property
    def name(self) -> str:
        return self.__class__.i18n[self.locale][self._name_hash]
    
    side_icon: str = apimodel.Field(name="SideIconName", validator=to_icon)
    
    rarity_type: CharacterRarity = apimodel.Field(name="QualityType")
    """Rarity type based on character icon border."""
    
    @property
    def rarity(self) -> int:
        return 5 if "ORANGE" in self.rarity_type.name else 4
    

    @apimodel.root_validator(order=apimodel.Order.INITIAL_ROOT)
    async def __add_cached_data(self, values: typing.Dict[str, object]) -> typing.Dict[str, object]:
        global CHARACTER_DATA

        if not CHARACTER_DATA or self.id not in CHARACTER_DATA:
            CHARACTER_DATA = await self._client._get_character_data()

        values.update(CHARACTER_DATA[str(values["avatarId"])])

        return values


class Character(PartialCharacter):
    properties: typing.Mapping[typing.Union[CharacterProperty, int], Property] = apimodel.Field(name="propMap")
    """Character properties."""

    stats: typing.Mapping[typing.Union[Stat, int], float] = apimodel.Field(name="fightPropMap")
    """Character combat stats."""

    talent_set_id: int = apimodel.Field(name="skillDepotId")
    """Character talent-set ID."""

    unlocked_talent_ids: typing.Sequence[int] = apimodel.Field(name="inherentProudSkillList")
    """Unlocked talent IDs."""

    talent_levels: typing.Mapping[int, typing.Optional[int]] = apimodel.Field(name="skillLevelMap")
    """Character skill levels."""

    artifacts: typing.Sequence[Artifact]
    """Character arifacts."""

    weapon: Weapon
    """Character weapon."""

    friendship: int = apimodel.Field(name="fetterInfo", validator=lambda x: x["expLevel"])
    """Character friendship level."""

    constellation_ids: typing.Sequence[int] = apimodel.Field(None, name="talentIdList")
    """Character constellation IDs."""

    special_talent_levels: typing.Optional[typing.Mapping[int, int]] = apimodel.Field(
        None, name="proudSkillExtraLevelMap"
    )
    """Special talent levels."""

    @apimodel.root_validator(order=apimodel.Order.INITIAL_ROOT)
    def __flatten_equipment(self, values: typing.Dict[str, typing.Any]) -> typing.Dict[str, object]:
        """Flatten equipment."""
        values["artifacts"] = typing.cast("list[object]", [])

        for equipment in values["equipList"]:
            data: typing.Dict[str, typing.Any] = {
                "itemId": equipment["itemId"],
                **equipment["flat"],
            }

            if reliquary := equipment.get("reliquary"):
                data.update(reliquary)
                values["artifacts"].append(data)
            elif weapon := equipment.get("weapon"):
                data.update(weapon)
                values["weapon"] = data
            else:
                raise ValueError("Unknown equipment type")

        return values

class Player(Model):
    nickname: str
    """Player nickname."""

    level: int
    """Player level."""

    signature: str
    """Player signature."""

    world_level: int = apimodel.Field(name="worldLevel")
    """Player world level."""

    namecard_id: int = apimodel.Field(name="nameCardId")
    """Profile namecard ID."""

    achievements: int = apimodel.Field(name="finishAchievementNum")
    """Number of completed achievements."""

    abyss_floor: int = apimodel.Field(name="towerFloorIndex")
    """Player's current floor in the abyss."""

    abyss_level: int = apimodel.Field(name="towerLevelIndex")
    """Player's current level in the abyss."""

    characters: typing.Sequence[PartialCharacter] = apimodel.Field(name="showAvatarInfoList")
    """Player's displayed characters."""

    namecard_ids: typing.Sequence[int] = apimodel.Field(name="showNameCardIdList")
    """Player's displayed namecards."""

    profile_picture: int = apimodel.Field(name="profilePicture", validator=lambda x: x["avatarId"])
    """Character ID of the player's profile picture."""



class EnkaUser(Model):
    player: Player = apimodel.Field(name="playerInfo")
    """Player profile."""

    characters: typing.Sequence[Character] = apimodel.Field(name="avatarInfoList")
    """Detailed characters from profile showcase."""

    ttl: int
    """Cache ttl info."""
