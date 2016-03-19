import click
import lib.forget
import lib.recall

@click.command()
@click.pass_context
@click.argument('name', required=False)
def forget(ctx, name):
    '''
    Forget information Eidetic has remembered.

    If no name is given, Eidetic will list available project names

    If a name is given, Eidetic will forget everything about that project
    '''
    if not name:
        click.echo(lib.recall.recall_names())
    else:
        lib.forget.forget_project(name)
