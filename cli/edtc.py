from collections import defaultdict
import readline
import rethinkdb as r
import click
import os

DB = 'eidetic'
TABLE = 'projects'

@click.group()
def cli():
    pass

def _format_project_markdown(project):
    lines = []
    lines.append('# {}'.format(project['description']))
    lines.append('')
    lines.append('## Purpose')
    lines.append(project['purpose'])
    if 'outcomes' in project:
        lines.append('')
        lines.append('## Desired Outcomes')
        for outcome in project['outcomes']:
            lines.append("* {}".format(outcome['description']))
    if 'waitings' in project:
        lines.append('')
        lines.append('## Waiting')
        for waiting in project['waitings']:
            lines.append("* {}".format(waiting['description']))
    if 'actions' in project:
        lines.append('')
        lines.append('## Actions')
        for action in project['actions']:
            lines.append("* {}".format(action['description']))
    return "\n".join(lines)

def _recall_project(name, conn):
    c = r.db(DB).table(TABLE).filter(r.row['name'] == name).run(conn)
    for p in c:
        project_md = _format_project_markdown(p)
        click.echo(project_md)

def _recall_names(conn):
    c = r.db(DB).table(TABLE).pluck('name').distinct().run(conn)
    names = " ".join([n['name'] for n in c])
    if names:
        click.echo(names)

@cli.command()
@click.pass_context
@click.argument('names', nargs=-1)
def recall(ctx, names):
    '''
    Display information Eidetic has remembered.

    If no name is given, Eidetic will list available project names

    If a name is given, Eidetic will show detailed information about that project
    '''
    conn = r.connect(host="localhost", port=28015, db=DB)
    if not names:
        _recall_names(conn)
    else:
        for name in names:
            _recall_project(name, conn)

def _get_tags_from_filename(fname):
    dir, file = os.path.split(fname)
    _, dir = os.path.split(dir)
    file, _ = os.path.splitext(file)
    return dir, file

def _parse_h2(h2):
    h2 = h2.lower()
    if 'action' in h2:
        if 'next' in h2:
            return 'action', True
        return 'action', False
    if 'outcome' in h2:
        return 'outcome', False
    if 'waiting' in h2:
        if 'blocked' in h2:
            return 'waiting', True
        return 'waiting', False
    return h2, False

def _pluralize(s):
    return s+'s'

def _depluralize(s):
    if s.endswith('s'):
        return s[:-1]

def _parse_markdown_project(project_file):
    category, project = _get_tags_from_filename(project_file.name)
    lines = project_file.readlines()
    tag = None
    parsed_project = {'name': project, 'tags': [category]}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('# '):
            parsed_project['description'] = line.rpartition('# ')[2]
        elif line.startswith('## '):
            h2, next = _parse_h2(line.rpartition('## ')[2])
        else:
            if line.startswith('* '):
                if _pluralize(h2) not in parsed_project:
                    parsed_project[_pluralize(h2)] = []
                item = line.rpartition('* ')[2]
                parsed_project[_pluralize(h2)].append(
                        {'description': item,
                         'next': next})
            else:
                parsed_project[h2] = line
    return parsed_project


@cli.command()
@click.argument('project-file', type=click.File('rb'))
def remember(project_file):
    '''
    Ask Eidetic to remember some information for you.
    '''
    parsed_project = _parse_markdown_project(project_file)
    conn = r.connect(host="localhost", port=28015, db=DB)
    r.db(DB).table(TABLE).insert(parsed_project).run(conn)
