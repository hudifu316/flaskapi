from datetime import datetime

from flask_marshmallow import Marshmallow
from flask_marshmallow.fields import fields

from src.database import db

ma = Marshmallow()


class TripModel(db.Model):
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True)

    plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'), nullable=True)
    plan = db.relationship('PlanModel')

    departure_location_id = db.Column(db.Integer, nullable=True)
    destination_location_id = db.Column(db.Integer, nullable=True)
    order = db.Column(db.Integer, nullable=True)
    departure_date = db.Column(db.DateTime, nullable=True)
    arrival_date = db.Column(db.DateTime, nullable=True)
    transportation_id = db.Column(db.Integer, nullable=True)

    insertTime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updateTime = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, plan_id, departure_location_id, destination_location_id, order, departure_date, arrival_date, transportation_id):
        self.plan_id = plan_id
        self.departure_location_id = departure_location_id
        self.destination_location_id = destination_location_id
        self.order = order
        self.departure_date = departure_date
        self.arrival_date = arrival_date
        self.transportation_id = transportation_id

    def __repr__(self):
        return '<TripModel {}>'.format(self.id)


class TripSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TripModel

    departure_location_id = fields.Integer()
    destination_location_id = fields.Integer()
    order = fields.Integer()
    departure_date = fields.DateTime('%Y-%m-%dT%H:%M:%S')
    arrival_date = fields.DateTime('%Y-%m-%dT%H:%M:%S')
    transportation_id = fields.Integer()
