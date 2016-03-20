import markdown
import rethinkdb as r

import lib.db as db

def _format_project_html(project):
    md = _format_project_markdown(project)
    html = markdown.markdown(md, output_format='html5')
    return html

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

def _recall_project(name, conn, format_fn):
    c = db.get_table().filter(r.row['name'] == name).run(conn)
    p = c.next()
    if not p:
        return None
    return format_fn(p)

def recall_project(name, format='md'):
    conn = db.get_conn()
    if format == 'md':
        return _recall_project(name, conn, _format_project_markdown)
    if format == 'html':
        return _recall_project(name, conn, _format_project_html)
    if format == 'json':
        return _recall_project(name, conn, id)

def _recall_names(conn):
    c = db.get_table().pluck('name').distinct().run(conn)
    return " ".join([n['name'] for n in c])

def recall_names():
    conn = db.get_conn()
    return _recall_names(conn)
