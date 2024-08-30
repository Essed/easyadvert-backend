from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.__init__ import DeviceBase, DeviceCreate, DeviceUpdate
from dependency import get_current_user_from_token

from db.dals import DeviceDAL
from db.session import get_db

device_router = APIRouter()


@device_router.post("/")
async def create_device(device: DeviceCreate, current_user: DeviceBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    device_dal = DeviceDAL(db)
    return await device_dal.create(
        account_id=device.account_id,
        name=device.name,
        last_ip=device.last_ip,
        user_agent=device.user_agent
    )


@device_router.get("/{device_id}")
async def read_device(device_id: int, current_user: DeviceBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    device_dal = DeviceDAL(db)
    db_device = await device_dal.get(device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device


@device_router.get("/", response_model=list[DeviceBase])
async def read_devices(account_id: int, current_user: DeviceBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    device_dal = DeviceDAL(db)
    devices = await device_dal.get_all(account_id)
    return devices


@device_router.put("/{device_id}")
async def update_device(device_id: int, device: DeviceUpdate, current_user: DeviceBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    device_dal = DeviceDAL(db)
    db_device = await device_dal.update(
        device_id=device_id,
        name=device.name,
        last_ip=device.last_ip,
        user_agent=device.user_agent
    )
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device


@device_router.delete("/{device_id}")
async def delete_device(device_id: int, current_user: DeviceBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    device_dal = DeviceDAL(db)
    db_device = await device_dal.delete(device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")