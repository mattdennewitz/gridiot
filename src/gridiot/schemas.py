"""
Defines the schema for a baseball query, and supporting data.
"""

from pydantic import BaseModel, Field
from typing import List, Union, Literal


MLB_TEAMS = """
Arizona Diamondbacks, ARI
Atlanta Braves, ATL
Baltimore Orioles, BAL
Boston Red Sox, BOS
Chicago Cubs, CHC
Chicago White Sox, CWS
Cincinnati Reds, CIN
Cleveland Guardians, CLE
Colorado Rockies, COL
Detroit Tigers, DET
Houston Astros, HOU
Kansas City Royals, KCR
Los Angeles Angels, LAA
Los Angeles Dodgers, LAD
Miami Marlins, MIA
Milwaukee Brewers, MIL
Minnesota Twins, MIN
New York Mets, NYM
New York Yankees, NYY
Oakland Athletics, OAK
Philadelphia Phillies, PHI
Pittsburgh Pirates, PIT
San Diego Padres, SDP
San Francisco Giants, SFG
Seattle Mariners, SEA
St. Louis Cardinals, STL
Tampa Bay Rays, TBR
Texas Rangers, TEX
Toronto Blue Jays, TOR
Washington Nationals, WSN
"""


class TeamCriteria(BaseModel):
    team: str = Field(
        description="The team code for the team the player is associated with."
        f"Translate informal names to team codes. Here is a guide: {MLB_TEAMS}"
    )


class AwardCriteria(BaseModel):
    award: str


class PositionCriteria(BaseModel):
    position: str


class StatCriteria(BaseModel):
    stat: Literal[
        "WAR",
        "AVG",
        "OBP",
        "SLG",
        "OPS",
        "HR",
        "RBI",
        "SB",
        "ERA",
        "WHIP",
        "K/9",
        "IP",
        "SV",
    ]
    operator: Literal["=", ">", "<", ">=", "<="]
    value: float


class Criterion(BaseModel):
    type: Literal["team", "award", "position", "stat"]
    value: Union[TeamCriteria, AwardCriteria, PositionCriteria, StatCriteria]


class LogicalGroup(BaseModel):
    operator: Literal["AND", "OR"] = "AND"
    criteria: List[Union["LogicalGroup", Criterion]]


class BaseballQuery(BaseModel):
    root: LogicalGroup


def translate_to_quickwit(query: BaseballQuery) -> str:
    """
    Translate a BaseballQuery into a Quickwit query string.

    Args:
        query (BaseballQuery): The Pydantic model representing the query

    Returns:
        str: Quickwit query string.
    """

    def translate_group(group: LogicalGroup) -> str:
        translated_criteria = []
        for criterion in group.criteria:
            if isinstance(criterion, LogicalGroup):
                translated_criteria.append(translate_group(criterion))
            elif isinstance(criterion, Criterion):
                translated_criteria.append(translate_criterion(criterion))
        return f"({' {0} '.join(translated_criteria)})".format(group.operator)

    def translate_criterion(criterion: Criterion) -> str:
        if criterion.type == "team":
            return f"team_season_stint:{criterion.value.team}"
        elif criterion.type == "award":
            return f"awards:{criterion.value.award}"
        elif criterion.type == "position":
            return f"positions:{criterion.value.position}"
        elif criterion.type == "stat":
            return f"stat_{criterion.value.stat.lower()}:{criterion.value.operator}{criterion.value.value}"
        else:
            raise ValueError(f"Unknown criterion type: {criterion.type}")

    return translate_group(query.root)
