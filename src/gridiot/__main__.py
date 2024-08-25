import click

from gridiot.fetch import fetch_season_data


@click.group()
def cli(): ...


@cli.command("fetch")
@click.option(
    "-s",
    "--season",
    "seasons",
    type=int,
    multiple=True,
    help="Season to fetch data for.",
)
@click.option(
    "-o",
    "--output-path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True),
    default="data",
    help="Path to save fetched data to.",
)
def run_data_fetch(seasons: list[int], output_path: str) -> None:
    for season in seasons:
        fetch_season_data(season, output_path)


def run_data_ingestion(): ...
