class FileCommitData:
    # intended to track a files commit data. An instance of this class should track all the data
    # for a file within a given commit.

    def __init__(self, additions=0, deletions=0, commit=""):
        self.additions = additions
        self.deletions = deletions
        self.commit = commit


    def __hash__(self):
        return int(self.commit, 16)

    def __eq__(self, other):
        return other == self.commit

    def __ne__(self, other):
        return other != self.commit
