from datetime import datetime
from flask_marshmallow import Marshmallow
from flask_marshmallow.fields import fields
from sqlalchemy_utils import UUIDType
from src.database import db
import uuid

ma = Marshmallow()


class PlanModel(db.Model):
    __tablename__ = 'plans'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    traveler_id = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(255), nullable=True)
    uuid = db.Column(UUIDType(binary=False), nullable=True, default=uuid.uuid4())
    insertTime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updateTime = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, name, traveler_id=0):
        self.name = name
        self.traveler_id = traveler_id

    def __repr__(self):
        return '<PlanModel {}:{}>'.format(self.id, self.uuid)


class PlanSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PlanModel

    traveler_id = fields.Integer()
    name = fields.String()
