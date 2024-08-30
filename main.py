from fastapi import FastAPI
import uvicorn
from app.api.user import user_router
from app.api.announcement import announcement_router
from app.api.login import login_router
from app.api.device import device_router
from fastapi.routing import APIRouter


app = FastAPI()

app_router = APIRouter()

app_router.include_router(user_router, prefix="/user", tags=['user'])
app_router.include_router(announcement_router, prefix="/announcement", tags=['announcement'])
app_router.include_router(login_router, prefix="/login", tags=['login'])
app_router.include_router(device_router, prefix="/device", tags=['device'])

app.include_router(app_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)