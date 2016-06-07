#!/usr/bin/env python

from flask import Flask, request, render_template, session
from flask_bootstrap import Bootstrap
import os
from git_data_processor import generate_branch_insight
from flask_json_serialiser import GitStatsFlaskJSONEncoder
import pygal

app = Flask(__name__)
app.json_encoder = GitStatsFlaskJSONEncoder
Bootstrap(app)

def get_base_url():
    if app.config['SERVER_NAME'] is not None:
        base =  app.config['SERVER_NAME']
        print app.config
        if app.config['APPLICATION_ROOT'] is not None:
            base += app.config['APPLICATION_ROOT']
    else:
        base = '127.0.0.1:5000'
    print base
    return base


@app.route('/charts/bar.svg')
def generate_chart():

    print '**************'
    print session['branch_insight']
    print '**************'

    chart = pygal.Bar()
    chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])
    #chart = chart.render_data_uri()

    return chart.render_response()


@app.route('/branch/<branch>')
def branch_index(branch):

    session['current_branch'] = branch
    session['branch_insight'] = generate_branch_insight(branch)

    return render_template('branch.html', branch_data = generate_branch_insight(branch))

@app.route('/')
def index():

    # list the branches
    branches = os.listdir('data')
    print branches
    session['branches'] = branches
    session['server_base_url'] = get_base_url()


    return render_template('index.html')

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    print app.json_encoder
    app.run(debug=True)