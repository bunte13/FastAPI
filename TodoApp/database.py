from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://fastapi_955a_user:CpE0JBLDBJtOnHZhpFUqfQe7sza9ztHQ@dpg-cr683nij1k6c739d8prg-a.frankfurt-postgres.render.com/fastapi_955a"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() #object of the database