from collections import defaultdict
import readline
import rethinkdb as r
import click

DB = 'eidetic'
TABLE = 'stuff'

@click.group()
def cli():
    pass

@cli.command()
@click.option('-t', '--type', prompt=True, help='the type of stuff to remember')
@click.option('-d', '--description', prompt=True, help='more details about the stuff')
def remember(type, description):
    tags = {'type': type, 'description': description}
    while True:
        try:
            tag = raw_input('tag>> ') 
        # bail out on ctrl+C and ctrl+D
        except KeyboardInterrupt, EOFError:
            break
        # bail out on some key words
        if tag in ['q', 'quit', 'done', 'stop']:
            break
        value = raw_input('tag value>> ')
        # support bools
        if value in ['y', 't', 'True', 'true']:
            value = True
        if value in ['n', 'f', 'False', 'false']:
            value = False
        tags[tag] = value
    conn = r.connect(host="localhost", port=28015, db=DB)
    r.db(DB).table(TABLE).insert([tags]).run(conn)

@cli.command()
@click.option('-t', '--type', help='the type of stuff to recall')
@click.option('-n', '--name', help='which stuff')
def recall(type, name):
    conn = r.connect(host="localhost", port=28015, db=DB)
    c = r.db(DB).table(TABLE).filter(r.row[type] == name).run(conn)
    by_type = defaultdict(list)
    for e in c:
        by_type[e['type']].append(e)
    lines = []
    o = by_type[type]
    assert len(o) == 1
    o = o[0]
    assert o['type'] == type
    lines.append('# {}'.format(o['description']))
    for k, v in o.items():
        if k == 'description':
            continue
        lines.append('## {}'.format(k))
        lines.append(v)

    for t, es in by_type.items():
        if t == type:
            continue
        lines.append('## {}'.format(t))
        for e in es:
            lines.append('* {}'.format(e['description']))

    for line in lines:
        click.echo(line)
