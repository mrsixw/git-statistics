class FileCommitData(object):
    # intended to track a files commit data. An instance of this class should track all the data
    # for a file within a given commit.

    def __init__(self, file='', additions='0', deletions='0'):
        self.file = file
        self.additions = additions
        self.deletions = deletions
        if self.additions == '-' and self.deletions == '-':
            self.deletions = 0
            self.additions = 0
            self.binary = True
        else:
            self.binary = False

    def __repr__(self):
        return 'FileCommitData(%r,%r,%r)' % (self.file, self.additions, self.deletions)

    def __str__(self):
        return 'File: %s (additions: %s, deletions %s, binary %s)' % (self.file,
                                                                      self.additions,
                                                                      self.deletions,
                                                                      self.binary)

if __name__ == '__main__':

    x = FileCommitData('myfile','1','-')

    print x

    y = repr(x)

    print y

    z = eval(y)

    import json
    print json.dumps(x)

    print z