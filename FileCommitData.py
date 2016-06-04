class FileCommitData:
    # intended to track a files commit data. An instance of this class should track all the data
    # for a file within a given commit.

    def __init__(self, file='', additions=0, deletions=0):
        self.file = file
        self.additions = additions
        self.deletions = deletions
        if self.additions == '-' and self.deletions == '-':
            self.deletions = 0
            self.additions = 0
            self.binary = True
        else:
            self.binary = False


    def __hash__(self):
        return int(self.commit, 16)

    def __eq__(self, other):
        return other == self.commit

    def __ne__(self, other):
        return other != self.commit
