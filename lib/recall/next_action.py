import rethinkdb as r

import lib.db as db

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
