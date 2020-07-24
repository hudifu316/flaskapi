from datetime import datetime
from flask_marshmallow.fields import fields

from src.database import db
from src.models import ma


class ActivityModel(db.Model):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)

    plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'), nullable=True)
    plan = db.relationship('PlanModel', back_populates="activities")

    activity = db.Column(db.String(255), nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    order = db.Column(db.Integer, nullable=True)

    insertTime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updateTime = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return '<ActivityModel {}:{}>'.format(self.id, self.activity)


class ActivitySchema(ma.SQLAlchemySchema):
    class Meta:
        model = ActivityModel
        load_instance = True
        sqla_session = db.session

    id = fields.Integer()
    plan_id = fields.Integer()
    activity = fields.String()
    image_url = fields.String()
    order = fields.Integer()
