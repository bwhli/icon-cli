import typer
from icon_cli.models.Balanced import Balanced
from icon_cli.models.Callbacks import Callbacks
from icon_cli.models.Config import Config
from icon_cli.utils import format_number_display, print_json, print_table
from rich import box
from rich import print
from rich.console import Console
from rich.table import Table

app = typer.Typer()


@app.command()
def debug():
    print(__name__)


@app.command()
def position(
    address: str = typer.Argument(..., callback=Callbacks.validate_icx_address),
    network: str = typer.Option(Config.get_default_network(), "--network", "-n", callback=Callbacks.enforce_mainnet),
    format: str = typer.Option(None, "--format", "-f", callback=Callbacks.validate_output_format),
):
    balanced = Balanced(network)
    position = balanced.query_position_from_address(address)

    if format == "json":
        print_json(position)
    else:
        print(position)


@app.command()
def position_count(
    network: str = typer.Option(Config.get_default_network(), "--network", "-n", callback=Callbacks.enforce_mainnet),
    format: str = typer.Option(None, "--format", "-f"),
):
    balanced = Balanced(network)
    position_count = balanced.query_position_count()

    if format == "json":
        response = {"position_count": position_count}
        print_json(response)
    else:
        print(f"Balanced Position Count: {position_count}")


@app.command()
def positions(
    index_start: int = typer.Option(1, "--start", "-s"),
    index_end: int = typer.Option(None, "--end", "-e"),
    min_collateralization: int = typer.Option(150, "--min-collateralization", "-min"),  # noqa 503
    max_collateralization: int = typer.Option(300, "--max-collateralization", "-max"),  # noqa 503
    sort_key: str = typer.Option(None, "--sort", "-k"),
    reverse: bool = typer.Option(False, "--reverse", "-r"),
    csv_output: bool = typer.Option(False, "--output", "-o"),
    network: str = typer.Option(Config.get_default_network(), "--network", "-n", callback=Callbacks.enforce_mainnet),
    format: str = typer.Option(None, "--format", "-f", callback=Callbacks.validate_output_format),
):
    balanced = Balanced(network)
    console = Console()

    # If index_end is None, set index_end to maximum.
    if not index_end:
        index_end = balanced.query_position_count() + 1

    # If sort_key is None, set sort_key to "pos_id".
    if not sort_key:
        sort_key = "pos_id"

    with console.status(f"[bold green]Querying Balanced positions..."):  # noqa 503
        positions = balanced.query_positions(
            index_start,
            index_end,
            min_collateralization,
            max_collateralization,
            sort_key,
            reverse,
        )  # noqa 503

    # Raise error if there are no Balanced positions.
    if len(positions) == 0:
        print("There are no Balanced positions that fit these parameters.")  # noqa 503
        raise typer.Exit()

    if format == "json":
        print_json(positions)
    else:
        table = Table(box=box.MINIMAL, show_header=True, show_lines=True)

        for header in ["#", "ADDRESS", "DEBT", "COLLATERAL", "COLLAT %"]:
            table.add_column(header, justify="left")

        for position in positions:
            table.add_row(
                str(position["pos_id"]),  # "#" # noqa 503
                position["address"],  # ADDRESS # noqa 503
                f"{format_number_display(position['total_debt'], 0, 2)} bnUSD",  # DEBT # noqa 503
                f"{format_number_display(position['collateral'], 0, 2)} sICX",  # COLLATERAL # noqa 503
                f"{format_number_display(position['ratio'] * 100, 0, 2)}%",  # COLLAT % # noqa 503
            )

        print_table(table)

        if csv_output:
            with console.status(f"[bold green]Exporting CSV file..."):  # noqa 503
                pass