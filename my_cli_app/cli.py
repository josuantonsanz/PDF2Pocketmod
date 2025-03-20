"""My CLI App - A simple command-line tool."""

import click

@click.group()
def cli():
    """My awesome CLI application."""
    pass

@cli.command()
@click.argument('name', default='World')
def hello(name):
    """Say hello to the provided name."""
    click.echo(f"Hello, {name}!")

@cli.command()
def version():
    """Show the current version."""
    click.echo("My CLI App version 0.1.0")

if __name__ == '__main__':
    cli()
