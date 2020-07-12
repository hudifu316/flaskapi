from datetime import datetime
from flask_marshmallow import Marshmallow
from flask_marshmallow.fields import fields
from sqlalchemy_utils import UUIDType
from src.database import db
import uuid

from src.models.activity import ActivitySchema
from src.models.trip import TripSchema

ma = Marshmallow()


class PlanModel(db.Model):
    __tablename__ = 'plans'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    trips = db.relationship("TripModel", backref="plans")
    activities = db.relationship("ActivityModel", backref="plans")

    traveler_id = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(255), nullable=True)
    uuid = db.Column(UUIDType(binary=False), nullable=True, default=uuid.uuid4())
    insertTime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updateTime = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, name, traveler_id):
        self.name = name
        self.traveler_id = traveler_id
        self.trips = []
        self.activities = []

    def __repr__(self):
        return '<PlanModel {}:{}>'.format(self.id, self.name)


class PlanSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PlanModel

    traveler_id = fields.Integer()
    name = fields.String()
    uuid = fields.String()
    trips = fields.List(fields.Nested(TripSchema))
    activities = fields.List(fields.Nested(ActivitySchema))
