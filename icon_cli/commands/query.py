import typer
from icon_cli.callbacks import Callbacks
from icon_cli.commands.subcommands.query import balanced, cps, gov, omm
from icon_cli.config import Config
from icon_cli.icx import Icx, IcxNetwork
from icon_cli.utils import print_json, print_object
from rich import print

app = typer.Typer()

app.add_typer(balanced.app, name="balanced")
app.add_typer(cps.app, name="cps")
app.add_typer(gov.app, name="gov")
app.add_typer(omm.app, name="omm")


@app.command()
def debug():
    print_object(__name__)


@app.command()
def account(
    address: str = typer.Argument(..., callback=Callbacks.validate_icx_address),
    network: IcxNetwork = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Callbacks.enforce_mainnet,
        case_sensitive=False,
    ),
    format: str = typer.Option(
        None, "--format", "-f", callback=Callbacks.validate_output_format
    ),
):
    icx = Icx(network)
    account_info = icx.query_address_info(address)

    if format == "json":
        print_json(account_info)
    else:
        print("TBD")


@app.command()
def balance(
    address: str = typer.Argument(..., callback=Callbacks.validate_icx_address),
    network: IcxNetwork = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Callbacks.enforce_mainnet,
        case_sensitive=False,
    ),
    format: str = typer.Option(
        None, "--format", "-f", callback=Callbacks.validate_output_format
    ),
):
    icx = Icx(network)
    balance = icx.query_icx_balance(address)

    print_json(balance)


@app.command()
def block(
    block: int = typer.Argument(0, callback=Callbacks.validate_block),
    network: IcxNetwork = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Callbacks.enforce_mainnet,
        case_sensitive=False,
    ),
    format: str = typer.Option(
        None, "--format", "-f", callback=Callbacks.validate_output_format
    ),
):
    """
    Returns block info for the specified block height.
    """
    icx = Icx(network)
    block_data = icx.query_block(block)

    print_json(block_data)


@app.command()
def supply(
    network: IcxNetwork = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Callbacks.enforce_mainnet,
        case_sensitive=False,
    ),
    format: str = typer.Option(
        None, "--format", "-f", callback=Callbacks.validate_output_format
    ),
):
    icx = Icx(network)
    icx_supply = icx.query_icx_supply()

    print_json(icx_supply)


@app.command()
def transaction(
    transaction_hash: str = typer.Argument(...),
    network: IcxNetwork = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Callbacks.enforce_mainnet,
        case_sensitive=False,
    ),
    format: str = typer.Option(
        None, "--format", "-f", callback=Callbacks.validate_output_format
    ),
):
    icx = Icx(network)
    transaction_result = icx.query_transaction_result(transaction_hash)

    print_json(transaction_result)
