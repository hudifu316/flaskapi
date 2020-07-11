from datetime import datetime
from flask_marshmallow import Marshmallow
from flask_marshmallow.fields import fields
from sqlalchemy_utils import UUIDType
from src.database import db
import uuid

ma = Marshmallow()


class TripModel(db.Model):
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True)

    plan_id = db.Column(db.Integer, nullable=True)
    departure_location_id = db.Column(db.Integer, nullable=True)
    destination_location_id = db.Column(db.Integer, nullable=True)
    order = db.Column(db.Integer, nullable=True)
    departure_date = db.Column(db.DateTime, nullable=True)
    arrival_date = db.Column(db.DateTime, nullable=True)

    insertTime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updateTime = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, plan_id, departure_location_id, destination_location_id, order, departure_date, arrival_date):
        self.plan_id = plan_id
        self.departure_location_id = departure_location_id
        self.destination_location_id = destination_location_id
        self.order = order
        self.departure_date = departure_date
        self.arrival_date = arrival_date

    def __repr__(self):
        return '<TripModel {}>'.format(self.id)


class TripSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TripModel

    plan_id = fields.Integer()
    departure_location_id = fields.Integer()
    destination_location_id = fields.Integer()
    order = fields.Integer()
    departure_date = fields.DateTime('%Y-%m-%dT%H:%M:%S')
    arrival_date = fields.DateTime('%Y-%m-%dT%H:%M:%S')
