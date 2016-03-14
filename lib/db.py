import rethinkdb as r

DB = 'eidetic'
TABLE = 'projects'

def get_conn():
    conn = r.connect(host="localhost", port=28015, db=DB)
    return conn

def get_table():
    return r.db(DB).table(TABLE)
