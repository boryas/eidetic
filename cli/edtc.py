import readline
import click

import recall
import remember

@click.group()
def cli():
    pass

cli.add_command(remember.remember)
cli.add_command(recall.recall)
