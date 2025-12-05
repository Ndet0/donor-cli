from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ---------------------------------------------------------
# 1. Create the Base class for all our ORM models
# ---------------------------------------------------------
Base = declarative_base()

# ---------------------------------------------------------
# 2. Create the SQLite database engine
# ---------------------------------------------------------
# This creates a file called donor.db in our project folder
DATABASE_URL = "sqlite:///donor.db"

engine = create_engine(DATABASE_URL, echo=False)

# ---------------------------------------------------------
# 3. Create a session factory
# ---------------------------------------------------------
SessionLocal = sessionmaker(bind=engine)
