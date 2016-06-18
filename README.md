# git-statistics
Flask webapp to display statistics on branches in a git repo

The application works in multiple stages. There is a flask web application which displays results generated from a 
static database of git commits. The data held in the database is based in the `git diff --numstat` output which 
summarises files and a number of lines added and deleted on a per commit basis. 

Generation of the commit data is done via two utility scripts, `git_diff_file_generator.py` and `git_db.py`.

The former script execute to generate text files for all the commits within a given branch. This can then be fed into the
latter to generate a sqllite database for faster querying of the data in order to support the web app. At a future point these 
will be unified. 

The current architecture of the applications very deliberately have these two items separated. It is the intenect that the 
database and git commits be regenerated periodically on a batch process such as a cron job running nightly. At present,
the files will regenerate everything each time, but an optimisation to generate delta is a future enhancement. 


# Installation
Please the requirements.txt for a list of python modules required to run this aoplication. 

install with :
`pip install -r requirements.txt`

The application has been writtend for Python 2.7.10

# Execution

The flask web application can be launched via the file `flask_web_app.py`. Running this file will run 
the built in web server in debug mode. It is highly recommended that this be placed behind a "proper"
web front end like apache or nginx. 

`git_diff_file_generator.py` and `git_db.py` are expected to be run as command line utilities on a cron job. `git_diff_file_generator.py`
itself expects to generate a `data` directory under the root of where you application in hosted (the directory where this file resides). 
'git_db.py' expect to reuse this `data` directory to generate its sqlite data which will be located again under the root director 
and called `database/git_repo_data.db`

# Testing
Both parts of this application has be developed and tested on Mac OS X (10.11) El Capitan with Pycharm Professional hosting a virtual environemnt
running Python 2.7.10. The appliation has been deployed on Ubuntu Linux 15.10 behind an Apache Webserver via `mod_wsgi`.






