from marshmallow import Schema, fields


class FileCommitDataSchema(Schema):
    file = fields.Str()
    additions = fields.Int()
    deletions = fields.Int()
