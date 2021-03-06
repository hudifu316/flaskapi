from flask_restx import Namespace, fields, Resource, reqparse
from src.models.transportation import TransportationModel, TransportationSchema
from src.database import db

transportation_namespace = Namespace('transportation', description='Transportationのエンドポイント')
transportation = transportation_namespace.model('TransportationModel', {
    'id': fields.Integer(
        readonly=True,
        required=False,
        description='交通手段のID',
        example=0
    ),
    'transportation': fields.String(
        required=False,
        description='交通手段名',
        example='新幹線なごみ'
    ),
    'image_url': fields.String(
        required=False,
        description='参考画像のURL',
        example='https://upload.wikimedia.org/wikipedia/commons/5/5a/JRshikoku_tetsudo_hobby_train_kiha32_3.jpg'
    )
})


@transportation_namespace.route('/')
class TransportationList(Resource):
    # TransportationModelを利用して結果をパースしてリストで返す
    @transportation_namespace.marshal_list_with(transportation, envelope='transportation')
    def get(self):
        """
        Transportation一覧取得
        """
        return TransportationModel.query.all()

    @transportation_namespace.marshal_with(transportation)
    @transportation_namespace.expect(transportation)
    def post(self):
        """
        Transportation登録
        ## 入力値
        - transportation : 交通手段（varchar255）
        - image_url : 参考画像URL（varchar255）
        ## 注意事項
        idは登録時に自動採番されるため不要
        """
        parser = reqparse.RequestParser()
        parser.add_argument('transportation', type=str)
        parser.add_argument('image_url', type=str)

        args = parser.parse_args()
        transportation_insert = TransportationModel(args.transportation, args.image_url)
        db.session.add(transportation_insert)
        db.session.commit()
        res = TransportationSchema().dump(transportation_insert)
        return res, 201


@transportation_namespace.route('/<int:id>')
@transportation_namespace.doc(params={'id': 'id of transportation'})
class TransportationController(Resource):
    # TransportationModelモデルを利用して結果をパースして単体で返す
    @transportation_namespace.marshal_with(transportation)
    def get(self, id):
        """
        Transportation詳細
        """
        # ただし1個も見つからなかったら404を返す
        return TransportationModel.query.filter(TransportationModel.id == id).first_or_404()

    def delete(self, id):
        """
        Transportation削除
        """
        # 見つからなかったときの処理してないけど許して
        target_transportation = TransportationModel.query.filter(TransportationModel.id == id).first()
        db.session.delete(target_transportation)
        db.session.commit()
        return {'message': 'Success'}, 200
