# File data store. This will hold all the instances we know where a file has changed

class FileData:

    def __init__(self, filename=None):
        self.filename = filename
        self.num_hunks = 0
        self.commits = set()

    def __str__(self):
        return "File %s had %d hunks changed in %d commits (%s)" % (self.filename, self.num_hunks, len(self.commits),
                                                                    ", ".join(self.commits))

    def __repr__(self):
        return "FileData(%r)" % (self.filename)

