
# Container for commit identification.

from FileCommitData import FileCommitData
import datetime

class CommitData():


    def __init__(self, commiter = '', commit_hash='', date = None,
                 files_changed=[], additions=0, deletions=0):
        self.commiter = commiter
        self.commit_hash = commit_hash
        self.date = date
        #self.merge_id = None
        self.files_changed = files_changed

        self.totalAdditions = additions
        self.totalDeletions = deletions



    def __repr__(self):
        return 'CommitData(%r,%r,%r,%r,%r,%r)' % (self.commiter,
                                                  self.commit_hash,
                                                  self.date,
                                                  self.files_changed,
                                                  self.totalAdditions,
                                                  self.totalDeletions)



if __name__ == '__main__':

    x = CommitData('me','1234',datetime.datetime.today(),[FileCommitData('myfile','1','-')],100,200)

    print x

    y = repr(x)

    print y

    z = eval(y)

    print z

    import json

    print json.dumps(x)