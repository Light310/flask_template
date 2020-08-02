from datetime import datetime
from config import db, ma

class ExampleObject(db.Model):
    __tablename__ = 'example_object'
    example_object_id = db.Column(db.Integer, primary_key=True)
    field1 = db.Column(db.String(32))
    field2 = db.Column(db.String(32))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ExampleObjectSchema(ma.ModelSchema):
    class Meta:
        model = ExampleObject
        sqla_session = db.session  