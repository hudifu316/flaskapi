from datetime import datetime

from flask_marshmallow import Marshmallow
from flask_marshmallow.fields import fields

from src.database import db

ma = Marshmallow()


class ActivityModel(db.Model):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)

    plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'), nullable=True)
    plan = db.relationship('PlanModel')

    activity = db.Column(db.String(255), nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    order = db.Column(db.Integer, nullable=True)

    insertTime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updateTime = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, plan_id, activity, image_url, order):
        self.plan_id = plan_id
        self.activity = activity
        self.image_url = image_url
        self.order = order

    def __repr__(self):
        return '<ActivityModel {}:{}>'.format(self.id, self.name)


class ActivitySchema(ma.SQLAlchemySchema):
    class Meta:
        model = ActivityModel

    activity = fields.String()
    image_url = fields.String()
    order = fields.Integer()
