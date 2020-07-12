from flask_restx import Namespace, fields, Resource, reqparse

from src.apis.activity import activity
from src.apis.trip import trip
from src.models.plan import PlanModel, PlanSchema
from src.database import db


plan_namespace = Namespace('plans', description='一つの旅行全体のプランを表す')
plan = plan_namespace.model('PlanModel', {
    'id': fields.Integer(
        required=False,
        description='旅行プランのID',
        example=0
    ),
    'traveler_id': fields.Integer(
        required=False,
        description='旅行プランを作ったユーザのID',
        example=1
    ),
    'name': fields.String(
        required=False,
        description='旅行プランのタイトル',
        example='北北西の旅'
    ),
    'uuid': fields.String(
        required=False,
        description='リンクシェア用のUUID',
        example='XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
    ),
    'trips': fields.List(fields.Nested(trip)),
    'activities': fields.List(fields.Nested(activity))
})


@plan_namespace.route('/')
class PlanList(Resource):
    # PlanModelを利用して結果をパースしてリストで返す
    @plan_namespace.marshal_list_with(plan)
    def get(self):
        """
        Plan一覧取得
        - すべての旅行プランの一覧情報を返す
        - 旅行プランには各行程とアクティビティがネスト構造で返却される
        """
        return PlanModel.query.all()

    @plan_namespace.marshal_with(plan)
    @plan_namespace.expect(plan, validate=True)
    def post(self):
        """
        Plan登録
        - 旅行プランの登録はプラン名と登録ユーザIDのみをPostする
        - プランIDとUUIDは自動採番されるため不要
        - 行程とアクティビティの一覧は登録時は無視される
        """
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help='plan name')
        parser.add_argument('traveler_id', type=int)

        args = parser.parse_args()
        plan_insert = PlanModel(args.name, args.traveler_id)
        db.session.add(plan_insert)
        db.session.commit()
        res = PlanSchema().dump(plan_insert)
        return res, 201


@plan_namespace.route('/<int:id>')
@plan_namespace.doc(params={'id': 'id of plan'})
class PlanController(Resource):
    # PlanModelモデルを利用して結果をパースして単体で返す
    @plan_namespace.marshal_with(plan)
    def get(self, id):
        """
        Plan詳細詳細取得
        - {int:id}で指定された旅行プランの情報を返却する
        """
        # ただし1個も見つからなかったら404を返す
        return PlanModel.query.filter(PlanModel.id == id).first_or_404()

    def delete(self, id):
        """
        Plan削除
        - {int:id}で指定された旅行プランを削除する
        """
        # 見つからなかったときの処理してないけど許して
        target_plan = PlanModel.query.filter(PlanModel.id == id).first()
        db.session.delete(target_plan)
        db.session.commit()
        return {'message': 'Success'}, 200
