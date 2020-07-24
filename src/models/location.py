from datetime import datetime
from flask_marshmallow.fields import fields

from src.database import db
from src.models import ma


class LocationModel(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)

    location = db.Column(db.String(256), nullable=True)
    address = db.Column(db.String(256), nullable=True)
    image_url = db.Column(db.String(256), nullable=True)

    insertTime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updateTime = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return '<LocationModel {}:{}>'.format(self.id, self.location)


class LocationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = LocationModel
        load_instance = True
        sqla_session = db.session

    id = fields.Integer()
    location = fields.String()
    address = fields.String()
    image_url = fields.String()
