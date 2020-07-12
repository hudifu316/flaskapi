from flask_restx import Namespace, fields, Resource, reqparse
from src.models.activity import ActivityModel, ActivitySchema
from src.database import db

activity_namespace = Namespace('activities', description='旅行プランの中でアクティビティを表す')
activity = activity_namespace.model('ActivityModel', {
    'id': fields.Integer(
        required=False,
        description='アクティビティのID',
        example=0
    ),
    'plan_id': fields.Integer(
        required=False,
        description='旅行プランのID（FK）',
        example=1
    ),
    'activity': fields.String(
        required=False,
        description='アクティビティの名称',
        example='ねこと遊ぶ'
    ),
    'image_url': fields.String(
        required=False,
        description='アクティビティの参考画像',
        example='https://pbs.twimg.com/media/Ecm58xSUwAEXDYq?format=jpg'
    ),
    'order': fields.Integer(
        required=False,
        description='旅行プランの中での並び順',
        example=20
    )
})


@activity_namespace.route('/')
class ActivityList(Resource):
    # ActivityModelを利用して結果をパースしてリストで返す
    @activity_namespace.marshal_list_with(activity)
    def get(self):
        """
        Activity一覧取得
        """
        return ActivityModel.query.all()

    @activity_namespace.marshal_with(activity)
    @activity_namespace.expect(activity, validate=True)
    def post(self):
        """
        Activity登録
        ## 入力値
        - plan_id(FK)
        - activity : アクティビティの名称(varchar255)
        - image_url : 参考画像URL（varchar255）
        - order : 旅行プランの中での並び順
        ## 注意事項
        idは登録時に自動採番されるため不要
        FK表記のあるパラメタはFK制約のため、関連テーブルにレコードが存在しないとエラーとなる
        """
        parser = reqparse.RequestParser()
        parser.add_argument('plan_id', type=int)
        parser.add_argument('activity', type=str)
        parser.add_argument('image_url', type=str)
        parser.add_argument('order', type=int)

        args = parser.parse_args()
        activity_insert = ActivityModel(args.plan_id, args.activity, args.image_url, args.order)
        db.session.add(activity_insert)
        db.session.commit()
        res = ActivitySchema().dump(activity_insert)
        return res, 201


@activity_namespace.route('/<int:id>')
@activity_namespace.doc(params={'id': 'id of activity'})
class ActivityController(Resource):
    # ActivityModelモデルを利用して結果をパースして単体で返す
    @activity_namespace.marshal_with(activity)
    def get(self, id):
        """
        Activity詳細
        """
        # ただし1個も見つからなかったら404を返す
        return ActivityModel.query.filter(ActivityModel.id == id).first_or_404()

    def delete(self, id):
        """
        Activity削除
        """
        # 見つからなかったときの処理してないけど許して
        target_activity = ActivityModel.query.filter(ActivityModel.id == id).first()
        db.session.delete(target_activity)
        db.session.commit()
        return {'message': 'Success'}, 200
