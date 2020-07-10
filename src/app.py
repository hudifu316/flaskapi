from flask import Flask, jsonify
from flask_restful import Api
from src.database import init_db
from src.apis.plan import PlanListAPI, PlanAPI

def create_app():

  app = Flask(__name__)
  app.config.from_object('src.config.Config')

  init_db(app)

  api = Api(app)
  api.add_resource(PlanListAPI, '/plans')
  api.add_resource(PlanAPI, '/plans/<id>')

  return app

app = create_app()
