from flask import Flask
from flask_restx import Api

from src.apis.plan import plan_namespace
from src.apis.trip import trip_namespace
from src.database import init_db


def create_app():
    app = Flask(__name__)
    app.config.from_object('src.config.Config')

    init_db(app)

    api = Api(
        title='Matatabi API',
        version='1.0',
        description='Matatabi Trip Planning API'
    )
    api.init_app(app)
    api.add_namespace(plan_namespace)
    api.add_namespace(trip_namespace)

    return app


app = create_app()
