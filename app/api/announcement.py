from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.__init__ import AnnouncementBase, AnnouncementCreate, AnnouncementUpdate, UserBase
from dependency import get_current_user_from_token

from db.dals import AnnouncementDAL
from db.session import get_db

announcement_router = APIRouter()



@announcement_router.post("/")
async def create_announcement(announcement: AnnouncementCreate, current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    announcement_dal = AnnouncementDAL(db)
    return await announcement_dal.create(
        owner_id=current_user.id,
        type_id=announcement.type_id,
        platform_id=announcement.platform_id,
        format_id=announcement.format_id,
        title=announcement.title,
        description=announcement.description,
        attachments=announcement.image_url,
        price=announcement.price,
        main_photo=announcement.url_photo
    )


@announcement_router.get("/{announcement_id}")
async def read_announcement(announcement_id: int, current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    announcement_dal = AnnouncementDAL(db)
    db_announcement = await announcement_dal.get(announcement_id)
    if db_announcement is None:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return db_announcement


@announcement_router.get("/")
async def read_announcements(current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    announcement_dal = AnnouncementDAL(db)
    announcements = await announcement_dal.get_all()
    return announcements


@announcement_router.put("/{announcement_id}")
async def update_announcement(announcement_id: int, announcement: AnnouncementUpdate, current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    announcement_dal = AnnouncementDAL(db)
    db_announcement = await announcement_dal.update(
        announcement_id,
        title=announcement.title,
        description=announcement.description,
        main_photo=announcement.url_photo,
        attachments=announcement.image_url,
        price=announcement.price
    )
    if db_announcement is None:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return db_announcement


@announcement_router.delete("/{announcement_id}")
async def delete_announcement(announcement_id: int, current_user: UserBase = Depends(get_current_user_from_token), db: AsyncSession = Depends(get_db)):
    announcement_dal = AnnouncementDAL(db)
    db_announcement = await announcement_dal.delete(announcement_id)
    if db_announcement is None:
        raise HTTPException(status_code=404, detail="Announcement not found")