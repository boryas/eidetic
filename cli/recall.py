import click

import lib.recall

@click.command()
@click.pass_context
@click.argument('names', nargs=-1)
def recall(ctx, names):
    '''
    Display information Eidetic has remembered.

    If no name is given, Eidetic will list available project names

    If a name is given, Eidetic will show detailed information about that project
    '''
    if not names:
        click.echo(lib.recall.recall_names())
    else:
        for name in names:
            for p_md in lib.recall.recall_project(name):
                click.echo(p_md)
