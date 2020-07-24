import json

from flask import request
from flask_restx import Namespace, fields, Resource, abort
from marshmallow import pprint

from src.apis.activity import activity
from src.apis.trip import trip
from src.models.plan import PlanModel, PlanSchema
from src.database import db


plan_namespace = Namespace('plans', description='一つの旅行全体のプランを表す')
plan = plan_namespace.model('PlanModel', {
    'id': fields.Integer(
        readonly=True,
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
        readonly=True,
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
    @plan_namespace.marshal_list_with(plan, envelope='plans')
    def get(self):
        """
        Plan一覧取得
        - すべての旅行プランの一覧情報を返す
        - 旅行プランには行程とアクティビティがネスト構造で返却される
        """
        return PlanModel.query.all()

    @plan_namespace.marshal_with(plan, code=201)
    @plan_namespace.expect(plan, validate=True)
    def post(self):
        """
        Plan登録
        ## 入力値
        - name : プラン名（varchar255）
        - traveler_id（いまTravelersテーブルがないので、任意のIDでOK）
        ## 注意事項
        idとuuidは登録時に自動採番されるため不要
        行程とアクティビティの一覧は登録時は無視される(暫定)
        """
        req = json.loads(request.data)
        schema = PlanSchema()

        plan_insert = schema.load(req)
        pprint(plan_insert)
        if plan_insert.id is not None:
            return abort(400, "Already exist ID. Failed to INSERT")
        elif plan_insert.uuid is not None:
            return abort(400, "Already exist UUID. Failed to INSERT")

        db.session.add(plan_insert)
        db.session.commit()

        return plan_insert, 201


@plan_namespace.route('/<int:plan_id>')
@plan_namespace.doc(params={'plan_id': 'プランIDで検索'})
class PlanController(Resource):
    # PlanModelモデルを利用して結果をパースして単体で返す
    @plan_namespace.marshal_with(plan)
    def get(self, plan_id):
        """
        Plan詳細取得
        - {int:plan_id}で指定された旅行プランの情報を返す
        - 旅行プランには行程とアクティビティがネスト構造で返却される
        """
        return PlanModel.query.get(plan_id) or abort(404)

    def delete(self, plan_id):
        """
        Plan削除
        - {int:plan_id}で指定された旅行プランを削除する
        - FK制約の影響は未確認
        """
        delete_plan = PlanModel.query.get(plan_id)
        if delete_plan is None:
            return abort(404)

        db.session.delete(delete_plan)
        db.session.commit()
        return {'message': 'Delete Success'}, 200

    @plan_namespace.marshal_with(plan, code=201)
    @plan_namespace.expect(plan)
    def put(self, plan_id):
        """
        Plan変更
        - {int:Plan_id}で指定された旅行プランを変更する
        - 旅行プランに含まれる行程を追加する場合はTripsAPIを使うこと
        - 旅行プランに含まれるアクティビティを追加する場合はActivityAPIを使うこと
        """
        req = json.loads(request.data)
        schema = PlanSchema()

        update_plan = schema.load(req, instance=PlanModel.query.get(plan_id))
        if update_plan is None:
            return abort(404)

        pprint(update_plan)
        db.session.add(update_plan)
        db.session.commit()

        return update_plan, 201
