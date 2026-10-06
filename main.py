from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import engine, SessionLocal
from models import Base, DeviceDB

Base.metadata.create_all(bind=engine)


app = FastAPI()

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

class Device(BaseModel):
    device_id: str
    name: str
    site: str

devices = []

@app.get("/")
def home():
    return {
        "message": "Smart BMS API is running"
    }

@app.get("/api/v1/devices")
def get_devices(
    db: Session = Depends(get_db)
):

    devices = db.query(DeviceDB).all()

    return devices

@app.get("/api/v1/devices/{device_id}")
def get_device(device_id: str):

    for device in devices:
        if device.device_id == device_id:
            return device

    raise HTTPException(
        status_code=404,
        detail="Device not found"
    )
@app.get("/api/v1/telemetry")
def get_telemetry(device_id: str, limit: int = 10):

    return {
        "device_id": device_id,
        "limit": limit
    }
@app.post("/api/v1/devices")
def create_device(
    device: Device,
    db: Session = Depends(get_db)
):

    new_device = DeviceDB(
        device_id=device.device_id,
        name=device.name,
        site=device.site
    )

    db.add(new_device)

    db.commit()

    db.refresh(new_device)

    return new_device