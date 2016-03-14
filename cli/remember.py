import click

import lib.remember

@click.command()
@click.argument('project-file', type=click.File('rb'))
def remember(project_file):
    '''
    Ask Eidetic to remember some information for you.
    '''
    project = lib.remember.parse_markdown_project(project_file)
    lib.remember.store_project(project)
