from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL')

# Creating the engine and session maker for the database connection
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    logger.info("Database engine successfully created.")
except Exception as e:
    logger.error(f"Error creating database engine: {e}")
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency function to get the database session
def get_db():
    db = SessionLocal()
    try:
        logger.info("Database session started.")
        yield db
    except Exception as e:
        logger.error(f"Error in database session: {e}")
        raise
    finally:
        db.close()
        logger.info("Database session closed.")
