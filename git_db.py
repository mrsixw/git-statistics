import sqlite3
from collections import OrderedDict
from contextlib import closing
from datetime import date, timedelta, datetime
from os import remove, listdir
from os.path import isfile
from git_data_processor import generate_branch_commit_data

_GIT_SCHEMA = '''
PRAGMA foreign_keys = ON;

CREATE TABLE git_branches(
    branch_id                     INTEGER PRIMARY KEY
  , branch_name                   TEXT
  , git_url                       TEXT
);

CREATE TABLE git_commit(
    commit_hash                   TEXT UNIQUE NOT NULL PRIMARY KEY
  , committer                     TEXT
  , commit_date                   TEXT
  , commit_messge                 TEXT
  , branch_id                     INTEGER NOT NULL
  , FOREIGN KEY (branch_id)       REFERENCES git_branches(branch_id)
);

CREATE TABLE file(
    file_id                       INTEGER PRIMARY KEY
  , file_path                     TEXT UNIQUE NOT NULL
);

CREATE TABLE commit_file(
    commit_hash                   TEXT
  , file_id                       INTEGER
  , additions                     TEXT
  , deletions                     TEXT
  , FOREIGN KEY(commit_hash)      REFERENCES git_commit(commit_hash)
  , FOREIGN KEY(file_id)          REFERENCES file(file_id)
  , PRIMARY KEY(commit_hash, file_id)
);
'''


class GitDB(object):


    def __init__(self, db_file = None):

        if db_file is None:
            self._dbFile = './database/git_repo_data.db'
        else:
            self._dbFile = db_file
        # check if we have a database, if not create it
        self._createDB(False)

    def _connect(self):
        """
        Connects to sqlite database and returns back the connection object
        """
        conn = sqlite3.connect(self._dbFile)
        conn.row_factory = sqlite3.Row
        # conn.text_factory = str
        return conn

    def _createDB(self, force = False):
        """
        Creates a database, if needed
        """
        if force or not isfile(self._dbFile):
            try:
                remove(self._dbFile)
            except OSError:
                print "Could not remove %s", self._dbFile

            with closing(self._connect()) as conn:
                conn.executescript(_GIT_SCHEMA)


    def _add_branch(self, branch = None, repo_url = None):
        with closing(self._connect()) as conn:
            conn.execute('''
                        INSERT INTO  git_branches(branch_name, git_url) VALUES (?, ?);
                         ''',
                         (branch, repo_url))
            conn.commit()

    def _get_branch_id(self, branch = None):
        with closing(self._connect()) as conn:
            cur = conn.execute('''
                               SELECT branch_id from git_branches WHERE branch_name = ?;
                               '''
                               , (branch,))
            return cur.fetchone()[0]


    def _add_file(self, file = None):
        with closing(self._connect()) as conn:
            conn.execute('''
                        INSERT OR IGNORE INTO file(file_path) VALUES (?);
                         ''',
                         (file,))
            conn.commit()

    def _get_file_id(self, file = None):
        with closing(self._connect()) as conn:
            cur = conn.execute('''
                               SELECT file_id from file WHERE file_path = ?;
                               '''
                               , (file,))
            return cur.fetchone()[0]


    def addData(self, data, date = date.today()):
        """
        Takes a list of Defect Records and adds them to the database
        """
        with closing(self._connect()) as conn:

            _insert_query='''
            INSERT OR REPLACE INTO defect_record (defect_id, headline, state, severity, priority, target_fix_phase,
                                        target_fix_version, feature, confidence, origin_system, origin_system_colloquial_name, submit_date, team, product_owner, external_bug_id, customer_severity)
                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            '''
            conn.executemany(_insert_query,
                             [(record.defectId, record.headline, record.state, record.severity,
                               record.priority, record.targetFixPhase, record.targetFixVersion, record.feature,
                               record.confidence, record.originSystem, record.originSystemColloqialName,
                               record.submitDate, record.team, record.productOwner, record.externalBugID,
                               record.customerSeverity) for record in data])

            conn.executemany('''
                            INSERT or REPLACE into defect_date (defect_id, date, state, severity, priority, target_fix_phase, target_fix_version, customer_severity) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            ''',
                             [(record.defectId, date, record.state, record.severity, record.priority,
                               record.targetFixPhase, record.targetFixVersion, record.customerSeverity) for record in
                              data])

            conn.commit()






if __name__ == '__main__':
    db = GitDB()
    db._createDB(True)

    directories = listdir('./data')

    for dir in directories:
        print dir
        db._add_branch(dir,'')

        branch_id = db._get_branch_id(dir)
        print branch_id


        commits = generate_branch_commit_data(dir)

        for commit in commits.keys():
            for file in commits[commit].files_changed:
                db._add_file(file.file)
                #print db._get_file_id(file.file)
