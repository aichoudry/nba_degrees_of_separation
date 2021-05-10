from __future__ import annotations

from datetime import datetime
from typing import *


class Player:
    """
    name: the player's name
    slug: the unique identifier of the player
    birthdate: a datetime object of the player's birthdate
    teams: a map from a team name to a map with season year and a roster of
        teammates
    """
    name: str
    slug: str
    birthdate: datetime
    teams: Dict[str, List[Dict[str, Union[Set[Player], int]]]]

    def __init__(self, name=None, slug=None, birthdate=None):
        self.name = name
        self.slug = slug
        self.birthdate = birthdate
        self.teams = {}

    def set_birthdate(self, birthdate: datetime):
        self.birthdate = birthdate

    def set_name(self, name: str):
        self.name = name

    def set_slug(self, slug: str):
        self.slug = slug

    def add_team(self, team_name: str, year: int, teammates: Set[Player]):
        if team_name not in self.teams:
            self.teams[team_name] = []
        self.teams[team_name].append({"year": year, "teammates": teammates})

    def __repr__(self):
        return f'{self.name}'

    def __str__(self):
        return Player.__repr__(self)

    def __eq__(self, other: Player):
        if type(other) != Player:
            return False
        return self.slug == other.slug

    def __hash__(self):
        return hash(self.slug)
