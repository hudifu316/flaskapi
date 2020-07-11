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
  
  
# ドキュメンテーション

[ER図](https://app.diagrams.net/?title=ERDiagram.drawio#Uhttps%3A%2F%2Fraw.githubusercontent.com%2Fhudifu316%2Fflaskapi%2Fmaster%2Fdoc%2FERDiagram.drawio)
