#!/usr/bin/env python

import sqlite3

import os
import plotly
import json
from flask import Flask, render_template, session, g
from flask_bootstrap import Bootstrap
from git_insight_generator import generate_branch_insight, generate_monthly_commit_data, generate_month_change_data



DATABASE = './database/git_repo_data.db'

app = Flask(__name__)
Bootstrap(app)

def get_base_url():
    if app.config['SERVER_NAME'] is not None:
        base =  app.config['SERVER_NAME']
        #print app.config
        if app.config['APPLICATION_ROOT'] is not None:
            base += app.config['APPLICATION_ROOT']
    else:
        base = '127.0.0.1:5000'
    print base
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
    print g._baseurl
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
        )

    ]

    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    ids = ['Commits over time','Changes over time']

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