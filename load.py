import pathlib

import polars as pl


PITCHING_STATS = [
    "WAR",
]

BATTING_STATS = [
    "WAR",
]


def load_data(season: int):
    df = pl.read_parquet(str(pathlib.Path(f"./data/batting-{season}.parquet")))

    fielding_df = pl.read_parquet(
        str(pathlib.Path(f"./data/fielding-{season}.parquet"))
    )

    player_positions_season = fielding_df.group_by("IDfg", "Season", "Team").agg(
        pl.col("Pos").list.explode().alias("positions")
    )

    df = df.join(player_positions_season, on=["IDfg", "Season", "Team"], how="left")

    # extract data for shaping
    df.select(
        pl.col("IDfg").alias("fgid").cast(pl.Utf8),
        pl.col("Name").alias("player_name"),
        pl.col("Season").alias("season"),
        pl.col("Team").alias("team_season_stint"),
        pl.col("positions"),
        *[pl.col(stat).alias(f"stat_{stat.lower()}") for stat in BATTING_STATS],
    ).write_ndjson(f"batters-{season}.ndjson")


if __name__ == "__main__":
    load_data(2023)
