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
@click.option('-n', '--name', prompt=True, help='name to recall it by later')
def remember(type, description, name):
    '''
    Ask Eidetic to remember something
    '''
    conn = r.connect(host="localhost", port=28015, db=DB)
    tags = {'type': type, type: name, 'description': description}
    while True:
        tag = click.prompt('tag', type=str) 
        # bail out on some key words
        if tag in ['q', 'quit', 'done', 'stop']:
            break
        # make sure we got a tag before getting a value
        elif not tag:
            continue
        _recall_type(tag, conn)
        value = click.prompt('tag value', type=str)
        # support bools
        if value in ['y', 't', 'True', 'true']:
            value = True
        if value in ['n', 'f', 'False', 'false']:
            value = False
        tags[tag] = value
    r.db(DB).table(TABLE).insert([tags]).run(conn)

def _recall_entry(type, name, conn):
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
    lines.append('## {}'.format(type))
    lines.append(o[type])
    skip = ['description', 'id', 'type', type]
    for k, v in o.items():
        if k in skip:
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

def _recall_type(type, conn):
    names = []
    c = r.db(DB).table(TABLE).filter(r.row['type'] == type).run(conn)
    for e in c:
        names.append(e[type])
    if names:
        click.echo(" ".join(names))

def _recall_types(conn):
    c = r.db(DB).table(TABLE).run(conn)
    types = set([e['type'] for e in c])
    if types:
        click.echo(" ".join(types))

@cli.command()
@click.pass_context
@click.argument('tags', nargs=-1)
def recall(ctx, tags):
    '''
    Display information Eidetic has remembered
    '''
    conn = r.connect(host="localhost", port=28015, db=DB)
    if len(tags) == 0:
        _recall_types(conn)
    elif len(tags) == 1:
        _recall_type(tags[0], conn)
    elif len(tags) == 2:
        _recall_entry(tags[0], tags[1], conn)
    else:
        click.echo(ctx.get_help())
