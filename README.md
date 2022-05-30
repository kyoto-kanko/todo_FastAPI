# todo_FastAPI
## 以下の手順で立ち上げ
パッケージ更新
```
docker compose build --no-cache
```
DB作成
```
docker compose exec todo-app poetry run python -m api.migrate_db
```
docker立ち上げ
```
docker compose up
```
DB接続
```
docker compose exec db mysql todo
```
## APIドキュメント
http://localhost:8000/docs
