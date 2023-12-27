from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

# Define the SQLAlchemy engine and connect to the SQLite database
engine = create_engine('sqlite:///ipd.db', echo=False)  # Set echo=False to suppress SQL output

# Define a base class for declarative models
Base = declarative_base()

# Define the IP model
class Ip(Base):
    __tablename__ = 'ip'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip_address = Column(String, nullable=False)
    checked = Column(Boolean, default=False)  #  it's a boolean column

# Create the table in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
