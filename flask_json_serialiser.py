from flask.json import JSONEncoder
from FileCommitData import FileCommitData
from FileCommitDataSchema import FileCommitDataSchema
from CommitData import CommitData

class GitStatsFlaskJSONEncoder(JSONEncoder):


    def default(self, o):

        if isinstance(o, FileCommitData):
            schema = FileCommitDataSchema()

            #print schema.dump(o)

            return schema.dump(o)

        elif isinstance(o, CommitData):
            return ''
        else:
            JSONEncoder.default(self, o)
