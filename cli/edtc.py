import readline
import click

import forget
import recall
import remember

@click.group()
def cli():
    pass

cli.add_command(forget.forget)
cli.add_command(remember.remember)
cli.add_command(recall.recall)
