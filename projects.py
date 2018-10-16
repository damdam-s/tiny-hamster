#!/usr/bin/env python

import sys
import os
try:
    from pysqlite2 import dbapi2 as sqlite
except ImportError:
    import sqlite3 as sqlite
import tinylib
import tinyconf

def usage():
    print "usage: projects.py [find|export] <project pattern>"
    sys.exit(1)

def get_projects(tiny, project_pattern):
    projects = []
    for project in tiny.search_project(project_pattern, timesheetable_only=True):
        projects.append(project[1])
    return projects

def find_projects(projects):
    for project in projects:
        print project

def export_projects(projects):
    try:
        con = sqlite.connect(os.path.expanduser("~/.local/share/hamster-applet/hamster.db"))
        cur = con.cursor()
        for project in projects:
            cur.execute("""
            INSERT INTO categories(name,search_name)
            SELECT :project, :project
              WHERE NOT EXISTS(
                SELECT 1 FROM categories
                  WHERE name = :project
                    AND search_name = :project)
            """, (project,))
        con.commit()
    except Exception as err:
        print "Failed to export projects to Hamster: %s" % err
        sys.exit(1)
    else:
        print "Projects successfully exported to Hamster"
    finally:
        if con:
            con.close()

def main():
    try:
        action = sys.argv[1]
        pattern = sys.argv[2]
    except IndexError:
        usage()

    if action != "find" and action != "export":
        usage()

    tinyconf = common.build_config()
    tiny_server = tinylib.TinyServer(
        tinyconf.user_name,
        tinyconf.user_pwd,
        tinyconf.tiny_db,
        tinyconf.rpc_url
    )
    pjs = get_projects(tiny_server, pattern)

    if action == "find":
        find_projects(pjs)
    elif action == "export":
        export_projects(pjs)

if __name__ == "__main__":
    main()
