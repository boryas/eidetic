import click

import lib.remember

@click.command()
@click.argument('project-file', required=False, type=click.File('rb'))
def remember(project_file):
    '''
    Ask Eidetic to remember some information for you.
    '''
    if not project_file:
        name = click.prompt('Project name')
        category = click.prompt('Project category')
        project = lib.remember.parse_markdown_project_from_editor(name, category)
    else:
        project = lib.remember.parse_markdown_project_from_file(project_file)
    lib.remember.store_project(project)
