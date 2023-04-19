"""
Ingest the Hadoop logs from https://zenodo.org/record/3227177.
"""

import sys
from pathlib import Path
import json
import sqlite3
import re

_msg_re = re.compile(r"""
    (?P<date>\d+-\d+-\d+\s\d+:\d+:\d+,\d+)\s+
    (?P<level>[A-Z]+)\s+
    \[(?P<component>.*?)\]\s+
    (?P<name>[a-zA-Z0-9.]+):\s+
    (?P<message>.*)
""", re.X)
_prog_re = re.compile(r"Progress of TaskAttempt (?P<key>[a-zA-Z0-9_]+) is\s*:\s+(?P<prog>\d+\.\d+)")
_done_re = re.compile(r"Done acknowledgement from (?P<key>[a-zA-Z0-9_]+)")
_debug = [
    'org.apache.hadoop.mapreduce.v2.app.rm.RMContainerAllocator',
    'org.apache.hadoop.mapred.TaskAttemptListenerImpl',
]


def init_db(file):
    path = Path(file)
    if path.exists():
        path.unlink()

    conn = sqlite3.connect(file)
    conn.execute("""
        CREATE TABLE action (ts, name, action, level, payload)
    """)
    conn.execute("""
        CREATE VIEW progress
        AS SELECT ts, action, payload ->> 'key' AS key, payload->>'status' AS status, payload->>'value' AS value
        FROM action
        WHERE action = 'progress';
    """)
    conn.commit()
    return conn


def scan_file(db, file):
    with db, open(file, 'r') as lf:
        for line in lf:
            line = line.strip()
            m = _msg_re.match(line)
            if not m:
                print('bad line: ' + line, file=sys.stderr)
                continue

            ts = m.group('date').replace(',', '.')

            pm = _prog_re.match(m.group('message'))
            dm = _done_re.match(m.group('message'))
            if pm:
                db.execute("INSERT INTO action (ts, name, action, payload) VALUES (?, ?, 'progress', ?)",
                           (ts, m.group('name'), json.dumps({
                                'key': pm.group('key'),
                                'value': float(pm.group('prog')),
                                'status': 'in-progress',
                            })))
            elif dm:
                db.execute("INSERT INTO action (ts, name, action, payload) VALUES (?, ?, 'progress', ?)",
                           (ts, m.group('name'), json.dumps({
                                'key': dm.group('key'),
                                'status': 'done',
                            })))
            else:
                level = m.group('level')
                if m.group('name') in _debug:
                    level = 'DEBUG'
                db.execute("INSERT INTO action (ts, name, action, level, payload) VALUES (?, ?, 'log', ?, ?)",
                           (ts, m.group('name'), level, m.group('message')))


def scan_dirs(db, dir):
    for file in Path(dir).glob('*/*.log'):
        print('scanning', file)
        scan_file(db, file)


def main():
    dir = sys.argv[1]
    print('scanning', dir)
    db = init_db('data/hadoop.db')
    try:
        scan_dirs(db, dir)
    finally:
        db.close()


if __name__ == '__main__':
    main()
