from sqlalchemy import Column, Integer, String
from database.db import Base

class UserData(Base):
    __tablename__ = "user_data"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)

class UserAgentOutputs(Base):
    __tablename__ = "user_agent_outputs"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    thread_id = Column(String, nullable=False)

    launch_metrics_specialist_agent_output: str = Column(String, default="")
    market_sentiment_specialist_agent_output: str = Column(String, default="")
    product_launch_analyst_agent_output: str = Column(String, default="")