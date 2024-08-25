import pathlib

from pybaseball import batting_stats, fielding_stats, pitching_stats


def fetch_season_data(
    season: int,
    output_path: str,
):
    runners = (
        ("pitching", pitching_stats),
        ("batting", batting_stats),
        ("fielding", fielding_stats),
    )

    for context, runner in runners:
        data = runner(season, ind=0, team="0,to", qual=0)
        data["season"] = season
        output_filename = str(
            (pathlib.Path(output_path) / f"{context}-{season}.parquet")
            .expanduser()
            .resolve()
        )
        data.to_parquet(output_filename)
