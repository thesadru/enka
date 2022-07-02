from __future__ import annotations

import typing

import aiohttp

from . import models

__all__ = ["Client"]

ENKA_URL = "https://enka.shinshin.moe/u/{}/__data.json"
LOCALIZATION_URL = "https://raw.githubusercontent.com/EnkaNetwork/API-docs/master/store/loc.json"
CHARACTER_URL = "https://raw.githubusercontent.com/EnkaNetwork/API-docs/master/store/characters.json"


class Client:
    async def _load_localization(self) -> None:
        if "EN" in models.Model.i18n and "FIGHT_PROP_MAX_HP" in models.Model.i18n["EN"]:
            return

        async with aiohttp.ClientSession() as session:
            r = await session.get(LOCALIZATION_URL)
            data = await r.json(content_type=None)

        for key, locales in data.items():
            for locale, value in locales.items():
                models.Model.i18n[locale][key] = value

    async def _get_character_data(self) -> typing.Mapping[str, typing.Mapping[str, object]]:
        async with aiohttp.ClientSession() as session:
            r = await session.get(CHARACTER_URL)
            return await r.json(content_type=None)

    async def get_user(self, uid: int, locale: str = "EN") -> models.EnkaUser:
        await self._load_localization()

        async with aiohttp.ClientSession() as session:
            url = ENKA_URL.format(uid)
            r = await session.get(url)
            data = await r.json()

        return await models.EnkaUser.create(data, client=self, locale=locale)
