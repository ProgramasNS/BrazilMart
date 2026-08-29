from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')

if not db_url: 
    raise ValueError('Database not found!')

engine = create_engine(db_url)

Base = declarative_base()

session = sessionmaker(bind=engine)
