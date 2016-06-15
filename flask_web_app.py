#!/usr/bin/env python

import sqlite3

import os
import plotly
import json
from flask import Flask, render_template, session, g
from flask_bootstrap import Bootstrap
from git_insight_generator import generate_branch_insight, generate_monthly_commit_data, generate_month_change_data, generate_commit_time_of_day
import locale


DATABASE = './database/git_repo_data.db'

app = Flask(__name__)
Bootstrap(app)


def print_local_number(number):
    locale.setlocale(locale.LC_ALL,'en_GB')
    return locale.format("%d", number, grouping=True)

app.jinja_env.filters['local_number'] =  print_local_number

def get_base_url():
    if app.config['SERVER_NAME'] is not None:
        base =  app.config['SERVER_NAME']
        #print app.config
        if app.config['APPLICATION_ROOT'] is not None:
            base += app.config['APPLICATION_ROOT']
    else:
        base = '127.0.0.1:5000'
    #print base
    return base

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = make_dicts

    # hack
    g._baseurl = get_base_url()
    #print g._baseurl
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def get_branches():
    return query_db("SELECT branch_name FROM git_branches")

@app.teardown_appcontext
def close_connection(exception):
    print "Teardown DB"
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def commits_over_time(branch):

    cpm = generate_monthly_commit_data(query_db, branch)
    changes = generate_month_change_data(query_db, branch)
    commit_tod = generate_commit_time_of_day(query_db, branch)

    week_days = ['Monday',
                 'Tuesday',
                 'Wednesday',
                 'Thursday',
                 'Friday',
                 'Saturday',
                 'Sunday']

    graphs = [
        dict(
            data=[
                dict(
                    x=[x for x in sorted(cpm.keys())],
                    y=[cpm[x] for x in sorted(cpm.keys())],
                    type='bar'
                ),
            ],
            layout=dict(
                title='Commits Over Time'
            )
        ),
        dict(
            data=[
                dict(
                    x = [x for x in sorted(changes.keys())],
                    y = [changes[x]['additions'] for x in sorted(changes.keys())],
                    type ='bar',
                    name = 'Code Additions',
                    marker=dict(color='rgb(0,255,0)')
                ),
                dict(
                    x=[x for x in sorted(changes.keys())],
                    y=[changes[x]['deletions'] for x in sorted(changes.keys())],
                    type='bar',
                    name = 'Code Deletions',
                    marker=dict(color='rgb(255,0,0)')
                )
            ],
            layout=dict(
                title='Changes Over Time',
                barmode='stack'
            )
        ),
        dict(
            data = [
                dict(
                    x = week_days,
                    y =  [commit_tod[x]['0-1'] for x in week_days],
                    name = '0am-2am',
                    type = 'bar'
                ),
                dict(
                    x=week_days,
                    y=[commit_tod[x]['2-3'] for x in week_days],
                    name='2am-4am',
                    type='bar'
                ),
                dict(
                    x=week_days,
                    y=[commit_tod[x]['4-5'] for x in week_days],
                    name='4am-6am',
                    type='bar'
                ),
                dict(
                    x=week_days,
                    y=[commit_tod[x]['6-7'] for x in week_days],
                    name='6am-8am',
                    type='bar'
                ),
                dict(
                    x=week_days,
                    y=[commit_tod[x]['8-9'] for x in week_days],
                    name='8am-10am',
                    type='bar'
                ),
                dict(
                    x=week_days,
                    y=[commit_tod[x]['10-11'] for x in week_days],
                    name='10am-12pm',
                    type='bar'
                ),
                dict(
                    x=week_days,
                    y=[commit_tod[x]['12-13'] for x in week_days],
                    name='12pm-2pm',
                    type='bar'
                ),
                dict(
                    x=week_days,
                    y=[commit_tod[x]['14-15'] for x in week_days],
                    name='2pm-4pm',
                    type='bar'
                ),
                dict(
                    x=week_days,
                    y=[commit_tod[x]['16-17'] for x in week_days],
                    name='4pm-6pm',
                    type='bar'
                ),
                dict(
                    x=week_days,
                    y=[commit_tod[x]['18-19'] for x in week_days],
                    name='6pm-8pm',
                    type='bar'
                ),
                dict(
                    x=week_days,
                    y=[commit_tod[x]['20-21'] for x in week_days],
                    name='8pm-10pm',
                    type='bar'
                ),
                dict(
                    x=week_days,
                    y=[commit_tod[x]['22-23'] for x in week_days],
                    name='10pm-12am',
                    type='bar'
                ),
            ],
            layout=dict(
                title='Commit Punchcard',
                barmode='stack'
            )
        )

    ]

    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    ids = ['Commits over time','Changes over time', 'Commit Punchcard']

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    return ids,graphJSON

@app.route('/branch/<branch>')
def branch_index(branch):
    branches = get_branches()

    ids, graphJSON = commits_over_time(branch)

    return render_template('branch.html',   branches = branches,
                                            branch = branch,
                                            branch_insight = generate_branch_insight(query_db, branch),
                                            ids = ids,
                                            graphJSON = graphJSON)

@app.route('/')
def index():

    db = get_db()

    g._baseurl = get_base_url()

    branches = get_branches()
    return render_template('index.html', branches = branches)

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    print app.json_encoder
    app.run(debug=True)