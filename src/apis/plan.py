from flask_restful import Resource, reqparse, abort
from flask import jsonify
from src.models.plan import PlanModel, PlanSchema
from src.database import db

class PlanListAPI(Resource):
  def __init__(self):
    self.reqparse = reqparse.RequestParser()
    self.reqparse.add_argument('name', required=True)
    self.reqparse.add_argument('state', required=True)
    super(PlanListAPI, self).__init__()

  def get(self):
    results = PlanModel.query.all()
    jsonData = PlanSchema(many=True).dump(results)
    return jsonify({'items': jsonData})

  def post(self):
    args = self.reqparse.parse_args()
    plan = PlanModel(args.name, args.state)
    db.session.add(plan)
    db.session.commit()
    res = PlanSchema().dump(plan)
    return res, 201


class PlanAPI(Resource):
  def __init__(self):
    self.reqparse = reqparse.RequestParser()
    self.reqparse.add_argument('name')
    self.reqparse.add_argument('state')
    super(PlanAPI, self).__init__()


  def get(self, id):
    plan = db.session.query(PlanModel).filter_by(id=id).first()
    if plan is None:
      abort(404)

    res = PlanSchema().dump(plan)
    return res


  def put(self, id):
    plan = db.session.query(PlanModel).filter_by(id=id).first()
    if plan is None:
      abort(404)
    args = self.reqparse.parse_args()
    for name, value in args.items():
      if value is not None:
        setattr(plan, name, value)
    db.session.add(plan)
    db.session.commit()
    return None, 204


  def delete(self, id):
    plan = db.session.query(PlanModel).filter_by(id=id).first()
    if plan is not None:
      db.session.delete(plan)
      db.session.commit()
    return None, 204
