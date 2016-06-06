from flask.json import JSONEncoder
from FileCommitData import FileCommitData
from CommitData import CommitData

class GitStatsFlaskJSONEncoder(JSONEncoder):


    def default(self, o):

        if isinstance(o, FileCommitData):
            return ''
        elif isinstance(o, CommitData):
            return ''
        else:
            JSONEncoder.default(self, o)
