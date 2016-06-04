
# Container for commit identification.

class CommitData(object):


    def __init__(self):
        self.commiter = ''
        self.commit_hash = ''
        self.date = None
        self.merge_id = None
        self.files_changed = []