# File data store. This will hold all the instances we know where a file has changed

class FileData:

    def __init__(self, filename=None):
        self.filename = filename
        self.num_hunks = 0
        self.commits = set()

    def __str__(self):
        return "File %s (%s) had %d hunks changed in %d commits" % (self.filename, self.getFileExtension() , self.num_hunks, len(self.commits))

    def __repr__(self):
        return "FileData(%r)" % (self.filename)


    def getFileExtension(self):
        last_dot_pos = self.filename.rfind('.')
        return self.filename[last_dot_pos+1:]
