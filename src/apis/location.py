from flask_restx import Namespace, fields, Resource, reqparse, inputs
from src.models.location import LocationModel, LocationSchema
from src.database import db

location_namespace = Namespace('locations', description='Locationのエンドポイント')
location = location_namespace.model('LocationModel', {
    'id': fields.Integer(
        required=False,
        description='場所のID',
        example=0
    ),
    'location': fields.String(
        required=False,
        description='場所の名前',
        example='大都会'
    ),
    'address': fields.String(
        required=False,
        description='場所の住所',
        example='岡山市北区大供一丁目1番1号'
    ),
    'image_url': fields.String(
        required=False,
        description='参考画像のURL',
        example='https://www.city.okayama.jp/design_img/head_id.png'
    )
})


@location_namespace.route('/')
class LocationList(Resource):
    # LocationModelを利用して結果をパースしてリストで返す
    @location_namespace.marshal_list_with(location)
    def get(self):
        """
        Location一覧取得
        """
        return LocationModel.query.all()

    @location_namespace.marshal_with(location)
    @location_namespace.expect(location, validate=True)
    def post(self):
        """
        Location登録
        ## 入力値
        - location : 場所名（varchar255）
        - address : 住所・所在地（varchar255）
        - image_url : 参考画像URL（varchar255）
        ## 注意事項
        idは登録時に自動採番されるため不要
        """
        parser = reqparse.RequestParser()
        parser.add_argument('location', type=str)
        parser.add_argument('address', type=str)
        parser.add_argument('image_url', type=str)

        args = parser.parse_args()
        location_insert = LocationModel(args.location, args.address, args.image_url)
        db.session.add(location_insert)
        db.session.commit()
        res = LocationSchema().dump(location_insert)
        return res, 201


@location_namespace.route('/<int:id>')
@location_namespace.doc(params={'id': 'id of location'})
class LocationController(Resource):
    # LocationModelモデルを利用して結果をパースして単体で返す
    @location_namespace.marshal_with(location)
    def get(self, id):
        """
        Location詳細
        """
        # ただし1個も見つからなかったら404を返す
        return LocationModel.query.filter(LocationModel.id == id).first_or_404()

    def delete(self, id):
        """
        Location削除
        """
        # 見つからなかったときの処理してないけど許して
        target_location = LocationModel.query.filter(LocationModel.id == id).first()
        db.session.delete(target_location)
        db.session.commit()
        return {'message': 'Success'}, 200
