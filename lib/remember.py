import os
import rethinkdb as r

import db

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

def parse_markdown_project(project_file):
    category, project = _get_tags_from_filename(project_file.name)
    lines = project_file.readlines()
    tag = None
    project = {'name': project, 'tags': [category]}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('# '):
            project['description'] = line.rpartition('# ')[2]
        elif line.startswith('## '):
            h2, next = _parse_h2(line.rpartition('## ')[2])
        else:
            if line.startswith('* '):
                if _pluralize(h2) not in project:
                    project[_pluralize(h2)] = []
                item = line.rpartition('* ')[2]
                project[_pluralize(h2)].append(
                        {'description': item,
                         'next': next})
            else:
                project[h2] = line
    return project

def store_project(project):
    conn = db.get_conn()
    f = r.row['name'] == project['name']
    exists = bool(list(
        db.get_table().filter(f).run(conn)))
    if exists:
        db.get_table().filter(f).update(project).run(conn)
    else:
        db.get_table().insert(project).run(conn)
