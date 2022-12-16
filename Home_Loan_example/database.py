from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

conn_string = "postgresql://postgres:password@localhost/database_name"

engine=create_engine("postgresql://postgres:password@localhost/database_name",
    echo=True
)

Base=declarative_base()

SessionLocal = sessionmaker(bind=engine)
