class FileCommitData:
    # intended to track a files commit data. An instance of this class should track all the data
    # for a file within a given commit.

    def __init__(self, commit=""):
        self.hunks = {}
        self.commit = commit


    def __hash__(self):
        return int(self.commit, 16)

    def __eq__(self, other):
        return other == self.commit

    def __ne__(self, other):
        return other != self.commit
