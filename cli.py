import os
import sys
import json
import click
import requests
from requests.exceptions import RequestException



API_BASE: str = os.getenv("API_BASE", "http://127.0.0.1:8000/math")
API_TOKEN: str = os.getenv("API_TOKEN", "topsecret")

HEADERS = {
    "X-API-Token": API_TOKEN,
    "Content-Type": "application/json",
}

TIMEOUT = 5




@click.group()
def cli() -> None:
    """Client de linie de comandă pentru Math Service."""




@cli.command()
@click.argument("base", type=float)
@click.argument("exponent", type=float)
def pow(base: float, exponent: float) -> None:
    """Calculează base^exponent."""
    _request("pow", {"base": base, "exponent": exponent})




@cli.command()
@click.argument("n", type=int)
def fib(n: int) -> None:
    """n‑th Fibonacci number."""
    _request("fib", {"n": n})




@cli.command()
@click.argument("n", type=int)
def fact(n: int) -> None:
    """Factorialul lui n."""
    _request("fact", {"n": n})




def _request(endpoint: str, payload: dict) -> None:
    url = f"{API_BASE}/{endpoint}"
    try:
        resp = requests.post(url, headers=HEADERS, json=payload, timeout=TIMEOUT)
        resp.raise_for_status()
        click.echo(resp.json()["result"])
    except RequestException as exc:
        click.echo(f"HTTP error: {exc}", err=True)
        sys.exit(1)
    except (KeyError, json.JSONDecodeError) as exc:
        click.echo(f"Unexpected response format: {exc}", err=True)
        sys.exit(2)




if __name__ == "__main__":
    cli()
