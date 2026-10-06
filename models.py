from sqlalchemy import Column, String
from database import Base


class DeviceDB(Base):

    __tablename__ = "devices"

    device_id = Column(String, primary_key=True)
    name = Column(String)
    site = Column(String)