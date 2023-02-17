# todo_FastAPI
## 以下の手順で立ち上げ!
poetryのインストール
```
docker-compose run --entrypoint "poetry install" todo-app
```
パッケージ更新
```
docker compose build --no-cache
```
docker起動
```
docker compose up
```
DB作成
```
docker compose exec todo-app poetry run python -m api.migrate_db
```
DB接続
```
docker compose exec db mysql todo
```
## APIドキュメント
http://localhost:8000/docs
