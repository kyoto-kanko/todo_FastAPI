from sqlalchemy import create_engine

from api.models.task import Base

username = "root"
host = "db"
port = 3306
database = "todo"
charset_type = "utf8"

DB_URL = f"mysql+pymysql://{username}@{host}:{port}/{database}?charset={charset_type}"
engine = create_engine(DB_URL, echo=True)


def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()
