import click

import lib.remember

@click.command()
@click.option('-f', '--project-file', type=click.File('rb'))
def remember(project_file):
    '''
    Ask Eidetic to remember some information.

    You can pass a project file in a dead simple markdown format.
    If not, Eidetic will open up $EDITOR to let you edit a project
    in a tmp file.

    \b
    Expected format:
    # <description>
    ## Purpose
    <High level purpose of the project>
    ## Desired outcomes
    * <outcome>
    ## Waiting on
    * <blocker>
    ## Actions
    * <action>
    ## Next Action
    * <action>'''
    if not project_file:
        name = click.prompt('Project name')
        category = click.prompt('Project category (e.g. business, pleasure)')
        project = lib.remember.parse_markdown_project_from_editor(name, category)
    else:
        project = lib.remember.parse_markdown_project_from_file(project_file)
    lib.remember.store_project(project)
