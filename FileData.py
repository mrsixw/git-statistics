# File data store. This will hold all the instances we know where a file has changed

class FileData:

    def __init__(self, filename=None):
        self.filename = filename
        self.commits = set()

    def __str__(self):
        return "File %s (%s) had changed in %d commits and %d lines added %d lines deleted" % (self.filename, self.getFileExtension() ,
                                                                                         self.getNumberOfCommits(),
                                                                                         self.getNumLinesChanged()[0],
                                                                                         self.getNumLinesChanged()[1])

    def __repr__(self):
        return "FileData(%r)" % (self.filename)


    def getFileExtension(self):
        last_dot_pos = self.filename.rfind('.')
        return self.filename[last_dot_pos+1:]

    def getNumberOfCommits(self):
        return len(self.commits)

    def getCommits(self):
        return list(self.commits)

    def getNumLinesChanged(self):
        additons, deletions = 0, 0

        for commit in self.commits:
            additions, deletions = additons + commit.additions, deletions + commit.deletions

        return (additions, deletions)

    def getTabulateListFormat(self):
        return [self.filename, self.getFileExtension(), self.getNumberOfCommits(), self.getNumLinesChanged()[0], self.getNumLinesChanged()[1]]