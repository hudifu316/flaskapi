from datetime import datetime
from flask_marshmallow.fields import fields

from src.database import db
from src.models import ma


class TransportationModel(db.Model):
    __tablename__ = 'transportation'

    id = db.Column(db.Integer, primary_key=True)

    transportation = db.Column(db.String(255), nullable=True)
    image_url = db.Column(db.String(255), nullable=True)

    insertTime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updateTime = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return '<TransportationModel {}>'.format(self.id)


class TransportationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TransportationModel
        load_instance = True
        sqla_session = db.session

    id = fields.Integer()
    transportation = fields.String()
    image_url = fields.String()
