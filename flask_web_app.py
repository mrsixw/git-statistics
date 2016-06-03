#!/usr/bin/env python

from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)
Bootstrap(app)

def get_base_url():
    base =  app.config['SERVER_NAME']
    print app.config
    if app.config['APPLICATION_ROOT'] is not None:
        base += app.config['APPLICATION_ROOT']
    print base
    return base


@app.route('/branch/<branch>')
def branch_index(branch):

    commits = os.listdir('data/'+branch)
    print commits

    branches = os.listdir('data')
    print branches

    for commit in commits:
        full_file_path = 'data/%s/%s' % (branch, commit)
        with open(full_file_path,'r') as f:
            lines = f.readlines()
            #print lines

    data_dict = dict()
    data_dict['earliest_commit'] = 1
    data_dict['latest_commit'] = 10

    print "Total commits %d" % (len(commits))

    return render_template('branch.html', branches = branches, branch = branch, commits = commits, data_dict = data_dict)

@app.route('/')
def index():

    # list the branches
    branches = os.listdir('data')
    print branches

    return render_template('index.html', server_base = get_base_url() ,branches = branches)

if __name__ == '__main__':
    app.run(debug=True)