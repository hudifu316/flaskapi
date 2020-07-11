from flask_restx import Namespace, fields, Resource, reqparse
from src.models.plan import PlanModel, PlanSchema
from src.database import db

plan_namespace = Namespace('plan', description='Planのエンドポイント')
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
    )
})


@plan_namespace.route('/')
class PlanList(Resource):
    # PlanModelを利用して結果をパースしてリストで返す
    @plan_namespace.marshal_list_with(plan)
    def get(self):
        """
        Plan一覧取得
        """
        return PlanModel.query.all()

    @plan_namespace.marshal_with(plan)
    @plan_namespace.expect(plan, validate=True)
    def post(self):
        """
        Plan登録
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
class PlanController(Resource):
    # PlanModelモデルを利用して結果をパースして単体で返す
    @plan_namespace.marshal_with(plan)
    def get(self, id):
        """
        Plan詳細
        """
        # ただし1個も見つからなかったら404を返す
        return PlanModel.query.filter(id == id).first_or_404()

    def delete(self, id):
        """
        Plan削除
        """
        # 見つからなかったときの処理してないけど許して
        target_plan = PlanModel.query.filter(id == id).first()
        db.session.delete(target_plan)
        return {'message': 'Success'}, 200
