from datetime import datetime
from flask_marshmallow.fields import fields

from src.database import db
from src.models import ma
from src.models.location import LocationSchema
from src.models.transportation import TransportationSchema


class TripModel(db.Model):
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True)

    plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'), nullable=True)
    plan = db.relationship('PlanModel', back_populates="trips")

    departure_location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=True)
    departure_location = db.relationship('LocationModel', foreign_keys=[departure_location_id], uselist=False)

    destination_location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=True)
    destination_location = db.relationship('LocationModel', foreign_keys=[destination_location_id], uselist=False)

    order = db.Column(db.Integer, nullable=True)
    departure_date = db.Column(db.DateTime, nullable=True)
    arrival_date = db.Column(db.DateTime, nullable=True)

    transportation_id = db.Column(db.Integer, db.ForeignKey('transportation.id'), nullable=True)
    transportation = db.relationship('TransportationModel', uselist=False)

    insertTime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updateTime = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return '<TripModel {}>'.format(self.id)


class TripSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TripModel
        load_instance = True
        sqla_session = db.session

    id = fields.Integer()
    plan_id = fields.Integer()
    departure_location = fields.Nested(LocationSchema)
    destination_location = fields.Nested(LocationSchema)
    order = fields.Integer()
    departure_date = fields.DateTime('%Y-%m-%dT%H:%M:%S')
    arrival_date = fields.DateTime('%Y-%m-%dT%H:%M:%S')
    transportation = fields.Nested(TransportationSchema)
