#!/usr/bin/env python

import sqlite3

import os
import pygal
from flask import Flask, render_template, session, g
from flask_bootstrap import Bootstrap
from git_insight_generator import generate_branch_insight

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
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def get_branches():
    print query_db("SELECT branch_name FROM git_branches")
    return query_db("SELECT branch_name FROM git_branches")

@app.teardown_appcontext
def close_connection(exception):
    print "Teardown DB"
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/charts/bar.svg')
def generate_chart():


    chart = pygal.Bar()
    chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])
    #chart = chart.render_data_uri()

    return chart.render_response()


@app.route('/branch/<branch>')
def branch_index(branch):
    branches = get_branches()

    return render_template('branch.html', branches = branches, branch = branch, branch_insight = generate_branch_insight(query_db, branch) )


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