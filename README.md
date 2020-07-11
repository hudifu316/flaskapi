# flaskapi

# 使い方

- Dockerをインストールしていることを確認
  ```
  % docker --version
  ```
  Docker version 19.03.8, build afacb8b
  
  ```
  % docker-compose --version
  ```
  docker-compose version 1.25.5, build 8a1c60f6

- Docker-composeで起動
  ```
  % docker-compose up -d
  ```
  Creating network "matatabi_default" with the default driver<BR>
  Creating matatabi_db_1  ... done<BR>
  Creating matatabi_api_1 ... done

- ブラウザでアクセス確認
  `http://localhost:5000/`

- DBの初期化
  ```
  % docker-compose exec api flask db init
  % docker-compose exec api flask db migrate
  % docker-compose exec api flask db upgrade
  ```
  エラーが出ないことを確認。
  
  `flask db init`は初回のみ実施する。（migrationsディレクトリがすでにあると言われたらスキップして問題ない）
  
  `flask db migrate`でエラーがでる場合は`migrations/versions`にある.pyスクリプトに以下Import文を追加してみる
  ```
  import sqlalchemy_utils
  ```
  
- 一応正しくテーブルが反映できていることを確認
  ```
  % docker-compose exec db mysql -u root -p
  > use matatabi;
  > show tables;
  ```  

   --------------------
   | Tables_in_matatabi |
   |--------------------|
   | activities         |
   | alembic_version    |
   | locations          |
   | plans              |
   | transportation     |
   | trips              |
    --------------------
    6 rows in set (0.00 sec)

- 各APIが正しく応答するか確認する
  ```
  % curl -X GET "http://localhost:5000/plans/" -H "accept: application/json"
  ```

  [SwaggerUI](http://localhost:5000)から直接確認してもよい。
  

# ドキュメンテーション

[ER図](https://app.diagrams.net/?title=ERDiagram.drawio#Uhttps%3A%2F%2Fraw.githubusercontent.com%2Fhudifu316%2Fflaskapi%2Fmaster%2Fdoc%2FERDiagram.drawio)
