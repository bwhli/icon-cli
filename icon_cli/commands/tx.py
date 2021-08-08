import typer
from icon_cli.commands.subcommands.tx import balanced, gov
from icon_cli.models.Callbacks import Callbacks
from icon_cli.models.Config import Config
from icon_cli.models.Icx import Icx, IcxNetwork
from icon_cli.utils import print_object
from rich import print

app = typer.Typer()

app.add_typer(balanced.app, name="balanced")
app.add_typer(gov.app, name="gov")


@app.command()
def debug():
    print_object(__name__)


@app.command()
def send(
    to: str = typer.Argument(..., callback=Callbacks.validate_icx_address),
    value: str = typer.Argument(..., callback=Callbacks.validate_transaction_value),
    type: str = typer.Option(
        "transaction", "--type", "-t", callback=Callbacks.validate_transaction_type
    ),
    method: str = typer.Option(None, "--method", "-m"),
    params: str = typer.Option(None, "--params", "-p"),
    keystore: str = typer.Option(
        Config.get_default_keystore(),
        "--keystore",
        "-k",
        callback=Callbacks.load_wallet_from_keystore,
    ),
    network: IcxNetwork = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Callbacks.enforce_mainnet,
        case_sensitive=False,
    ),
    simulation: bool = typer.Option(False, "--simulate", "-s"),
    confirmation: bool = typer.Option(True, "--confirm", "-c"),
):
    icx = Icx(network)

    if type == "transaction":
        transaction = icx.build_transaction(keystore, to, value)
    elif type == "call_transaction":
        if not method:
            print("Please specify a contract method.")
            raise typer.Exit()
        if to[:2] != "cx":
            print(f"{to} is not a valid ICX contract address.")
            raise typer.Exit()
        transaction = icx.build_call_transaction(keystore, to, method, params)

    if simulation:
        print_object(transaction)
    else:
        if confirmation:
            prompt = typer.confirm("Please confirm transaction details.")
            if not prompt:
                print("Exiting now...")
                raise typer.Exit()
        transaction_result = icx.send_transaction(keystore, transaction)
        print(transaction_result)
