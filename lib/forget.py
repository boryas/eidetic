import rethinkdb as r

import db

def _forget_project(name, conn):
    db.get_table().filter(r.row['name'] == name).delete().run(conn)

def forget_project(name):
    conn = db.get_conn()
    return _forget_project(name, conn)
