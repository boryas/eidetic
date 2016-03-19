import click

import lib.recall.next_action
import lib.recall.project

@click.group()
@click.pass_context
def recall(ctx):
    '''
    Display information Eidetic has remembered.

    Can recall projects and next actions.
    '''
    pass

@recall.command()
@click.pass_context
@click.argument('name', required=False)
def project(ctx, name):
    '''
    Display information about a project.

    If no name is given, Eidetic will list available project names

    If a name is given, Eidetic will show detailed information about that project
    '''
    if not name:
        click.echo(lib.recall.project.recall_names())
    else:
        for p_md in lib.recall.project.recall_project(name):
            click.echo(p_md)

@recall.command()
@click.pass_context
@click.argument('name', required=False)
def next_action(ctx, name):
    '''
    Display information about next actions to take

    If no name is given, return all next actions.

    If a name is given, return the next action for that project.
    '''
    if not name:
        for p, next_action in lib.recall.next_action.recall_next_actions():
            click.echo('{}: {}'.format(p, next_action))
    else:
        click.echo(lib.recall.next_action.recall_next_action(name))
