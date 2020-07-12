from flask_restx import Namespace, fields, Resource, reqparse, inputs

from src.apis.location import location
from src.apis.transportation import transportation
from src.models.trip import TripModel, TripSchema
from src.database import db

trip_namespace = Namespace('trips', description='旅行プランの中で行程を表す')
trip = trip_namespace.model('TripModel', {
    'id': fields.Integer(
        required=False,
        description='行程のID',
        example=0
    ),
    'plan_id': fields.Integer(
        required=False,
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
        example='2020-01-01T00:00:00+09:00'
    ),
    'arrival_date': fields.DateTime(
        required=False,
        description='到着時刻',
        example='2099-12-31T23:59:59+09:00'
    ),
    'transportation': fields.Nested(transportation)
})


@trip_namespace.route('/')
class TripList(Resource):
    # TripModelを利用して結果をパースしてリストで返す
    @trip_namespace.marshal_list_with(trip)
    def get(self):
        """
        Trip一覧取得
        - すべての行程の一覧情報を返す
        - 行程情報には出発地、到着地、交通手段がネスト構造で返却される
        """
        return TripModel.query.all()

    @trip_namespace.marshal_with(trip)
    @trip_namespace.expect(trip, validate=True)
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
        ## 注意事項
        idは登録時に自動採番されるため不要
        FK表記のあるパラメタはFK制約のため、関連テーブルにレコードが存在しないとエラーとなる
        """
        parser = reqparse.RequestParser()
        parser.add_argument('plan_id', type=int, help='FK')
        parser.add_argument('departure_location_id', type=int, help='FK')
        parser.add_argument('destination_location_id', type=int, help='FK')
        parser.add_argument('order', type=int)
        parser.add_argument('departure_date', type=inputs.datetime_from_iso8601)
        parser.add_argument('arrival_date', type=inputs.datetime_from_iso8601)
        parser.add_argument('transportation_id', type=int)

        args = parser.parse_args()
        trip_insert = TripModel(
            args.plan_id,
            args.departure_location_id,
            args.destination_location_id,
            args.order,
            args.departure_date,
            args.arrival_date,
            args.transportation_id)
        db.session.add(trip_insert)
        db.session.commit()
        res = TripSchema().dump(trip_insert)
        return res, 201


@trip_namespace.route('/<int:id>')
@trip_namespace.doc(params={'id': 'id of trip'})
class TripController(Resource):
    # TripModelモデルを利用して結果をパースして単体で返す
    @trip_namespace.marshal_with(trip)
    def get(self, id):
        """
        Trip詳細取得
        - {int:id}で指定された行程の情報を返す
        - 行程情報には出発地、到着地、交通手段がネスト構造で返却される
        """
        # ただし1個も見つからなかったら404を返す
        return TripModel.query.filter(TripModel.id == id).first_or_404()

    def delete(self, id):
        """
        Trip削除
        - {int:id}で指定された行程を削除する
        - FK制約の影響は未確認
        """
        # 見つからなかったときの処理してないけど許して
        target_trip = TripModel.query.filter(TripModel.id == id).first()
        db.session.delete(target_trip)
        db.session.commit()
        return {'message': 'Success'}, 200
