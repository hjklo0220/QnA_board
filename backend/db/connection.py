from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "mysql+pymysql://root:1234@127.0.0.1:3306/project"

engine = create_engine(DATABASE_URL)

SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()

