import sqlite3
from contextlib import closing
from os import remove, listdir
from os.path import isfile
from git_commit_file_processor import generate_branch_commit_data

_GIT_SCHEMA = '''
PRAGMA foreign_keys = ON;

CREATE TABLE git_branches(
    branch_id                     INTEGER PRIMARY KEY
  , branch_name                   TEXT
  , git_url                       TEXT
);

CREATE TABLE git_commit(
    commit_hash                   TEXT NOT NULL
  , committer                     TEXT
  , commit_date                   TEXT
  , branch_id                     INTEGER NOT NULL
  , FOREIGN KEY (branch_id)       REFERENCES git_branches(branch_id)
  , PRIMARY KEY (commit_hash, branch_id)
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
            self._dbFile = '../database/git_repo_data.db'
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


    def _add_commit(self,   commit_hash = None,
                            committer = None,
                            commit_date = None,
                            commit_message = '',
                            branch_id = None):
        with closing(self._connect()) as conn:
            conn.execute('''
                        INSERT OR IGNORE INTO git_commit(commit_hash, committer, commit_date, commit_message, branch_id) VALUES (?, ?, ?, ?, ?);
                         ''',
                         (commit_hash, committer, commit_date, commit_message, branch_id))
            conn.commit()


    def _add_commit_file_link(self, commit_hash = None, file_id = None, additions = None, deletions = None):
        with closing(self._connect()) as conn:
            conn.execute('''
                        INSERT OR IGNORE INTO commit_file(commit_hash, file_id, additions, deletions) VALUES (?, ?, ?, ?);
                         ''',
                         (commit_hash, file_id, additions, deletions))
            conn.commit()




if __name__ == '__main__':
    db = GitDB()
    db._createDB(True)

    directories = listdir('../data')

    for dir in directories:
        print dir
        db._add_branch(dir,'')

        branch_id = db._get_branch_id(dir)
        print branch_id


        commits = generate_branch_commit_data(dir)
        print len(commits)
        for commit in commits.keys():
            print commits[commit].commit_hash
            #print len(commits[commit].files_changed)

            db._add_commit(commits[commit].commit_hash,
                           commits[commit].commiter,
                           commits[commit].date,
                           '',
                           branch_id)


            for file in commits[commit].files_changed:
                #print file.file
                db._add_file(file.file)
                file_id = db._get_file_id(file.file)

                db._add_commit_file_link(commits[commit].commit_hash,
                                         file_id,
                                         file.additions,
                                         file.deletions)
