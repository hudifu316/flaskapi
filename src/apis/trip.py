import json

from flask import request
from flask_restx import Namespace, fields, Resource, abort
from marshmallow import pprint

from src.apis.location import location
from src.apis.transportation import transportation
from src.models.trip import TripModel, TripSchema
from src.database import db

trip_namespace = Namespace('trips', description='旅行プランの中で行程を表す')
trip = trip_namespace.model('TripModel', {
    'id': fields.Integer(
        readonly=True,
        required=False,
        description='行程のID',
        example=0
    ),
    'plan_id': fields.Integer(
        required=True,
        description='旅行プランのID（FK）',
        example=1
    ),
    'departure_location': fields.Nested(location),
    'destination_location': fields.Nested(location),
    'order': fields.Integer(
        required=False,
        description='旅行プランの中での並び順',
        example=10
    ),
    'departure_date': fields.DateTime(
        required=False,
        description='出発時刻',
        example='2020-01-01T00:00:00'
    ),
    'arrival_date': fields.DateTime(
        required=False,
        description='到着時刻',
        example='2099-12-31T23:59:59'
    ),
    'transportation': fields.Nested(transportation)
})


@trip_namespace.route('/')
class TripList(Resource):
    # TripModelを利用して結果をパースしてリストで返す
    @trip_namespace.marshal_list_with(trip, envelope='trips')
    def get(self):
        """
        Trip一覧取得
        - すべての行程の一覧情報を返す
        - 行程情報には出発地、到着地、交通手段がネスト構造で返却される
        """
        return TripModel.query.all()

    @trip_namespace.marshal_with(trip)
    @trip_namespace.expect(trip)
    def post(self):
        """
        Trip登録
        ## 入力値
        - plan_id（FK）
        - departure_location_id（FK）
        - destination_location_id（FK）
        - order : 旅行プランの中での並び順
        - departure_date
        - arrival_date
        - transportation_id（FK）
        """
        schema = TripSchema()
        req = json.loads(request.data)
        trip_insert = schema.load(req)
        pprint(trip_insert)

        if trip_insert.id is not None:
            return abort(400, "Already exist ID. Failed to INSERT")

        db.session.add(trip_insert)
        db.session.commit()

        return trip_insert, 201


@trip_namespace.route('/<int:trip_id>')
@trip_namespace.doc(params={'trip_id': 'id of trip'})
class TripController(Resource):
    # TripModelモデルを利用して結果をパースして単体で返す
    @trip_namespace.marshal_with(trip)
    def get(self, trip_id):
        """
        Trip詳細取得
        - {int:id}で指定された行程の情報を返す
        - 行程情報には出発地、到着地、交通手段がネスト構造で返却される
        """
        return TripModel.query.get(trip_id) or abort(404)

    def delete(self, trip_id):
        """
        Trip削除
        - {int:id}で指定された行程を削除する
        - FK制約の影響は未確認
        """
        target_trip = TripModel.query.get(trip_id)
        if target_trip is None:
            return abort(404)

        db.session.delete(target_trip)
        db.session.commit()
        return {'message': 'Delete Success'}, 200
