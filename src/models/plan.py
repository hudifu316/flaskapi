import uuid

from datetime import datetime
from flask_marshmallow.fields import fields
from sqlalchemy_utils import UUIDType
from src.database import db

from src.models import ma
from src.models.activity import ActivitySchema
from src.models.trip import TripSchema


class PlanModel(db.Model):
    __tablename__ = 'plans'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    trips = db.relationship("TripModel", back_populates="plan", cascade='all, delete, delete-orphan')
    activities = db.relationship("ActivityModel", back_populates='plan', cascade='all, delete, delete-orphan')

    traveler_id = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(255), nullable=True)
    uuid = db.Column(UUIDType(binary=False), nullable=True, default=uuid.uuid4())
    insertTime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updateTime = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return '<PlanModel {}:{}>'.format(self.id, self.name)


class PlanSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PlanModel
        load_instance = True
        sqla_session = db.session

    id = fields.Integer()
    traveler_id = fields.Integer()
    name = fields.String()
    uuid = fields.String()
    trips = fields.Nested(TripSchema, many=True)
    activities = fields.Nested(ActivitySchema, many=True)
