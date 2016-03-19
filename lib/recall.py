import rethinkdb as r

import db

def format_project_markdown(project):
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
    c = db.get_table().filter(r.row['name'] == name).run(conn)
    return [format_project_markdown(p) for p in c]

def recall_project(name):
    conn = db.get_conn()
    return _recall_project(name, conn)

def _recall_names(conn):
    c = db.get_table().pluck('name').distinct().run(conn)
    return " ".join([n['name'] for n in c])

def recall_names():
    conn = db.get_conn()
    return _recall_names(conn)

def _get_next_action(actions):
    next_actions = [a for a in actions if a['next']]
    if not next_actions:
        return None
    return next_actions[0]['description']

def _recall_next_action(name, conn):
    c = db.get_table().filter({'name': name})['actions'].run(conn)
    project_actions = [actions for actions in c]
    if not project_actions:
        return None
    actions = project_actions[0]
    return _get_next_action(actions)

def _recall_next_actions(conn):
    c = db.get_table().run(conn)
    for project in c:
        yield project['name'], _get_next_action(project['actions'])

def recall_next_actions():
    conn = db.get_conn()
    return _recall_next_actions(conn)

def recall_next_action(name):
    conn = db.get_conn()
    return _recall_next_action(name, conn)
