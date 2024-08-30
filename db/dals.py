from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.models import User, Announcement, Device

class UserDAL:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, name, email, role_id, subject_type_id, password_hash):
        db_user = User(
            name=name, 
            email=email,
            role_id=role_id,
            subject_type_id=subject_type_id,
            password_hash=password_hash
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def get(self, user_id: int):
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_all(self):
        result = await self.db.execute(
            select(User)
        )
        return result.scalars().all()

    async def get_by_email(self, email: str):
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def update(self, user_id: int, user: User):
        db_user = await self.get(user_id)
        if db_user is None:
            return None
        
        update_data = user.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def delete(self, user_id: int):
        db_user = await self.get(user_id)
        if db_user is None:
            return None
        
        await self.db.delete(db_user)
        await self.db.commit()
        return db_user


class AnnouncementDAL:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, owner_id: int, type_id: int, platform_id: int, format_id: int, title: str, 
                     description: str = None, main_photo: str = None, attachments: str = None, price: float = None):
        db_announcement = Announcement(
            owner_id=owner_id,
            type_id=type_id,
            platform_id=platform_id,
            format_id=format_id,
            title=title,
            description=description,
            main_photo=main_photo,
            attachments=attachments,
            price=price
        )
        self.db.add(db_announcement)
        await self.db.commit()
        await self.db.refresh(db_announcement)
        return db_announcement

    async def get(self, announcement_id: int):
        result = await self.db.execute(select(Announcement).where(Announcement.id == announcement_id))
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100):
        result = await self.db.execute(
            select(Announcement)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def update(self, announcement_id: int, title: str = None, description: str = None, main_photo: str = None, attachments: str = None, price: float = None):
        db_announcement = await self.get(announcement_id)
        if db_announcement is None:
            return None
        
        if title is not None:
            db_announcement.title = title
        if description is not None:
            db_announcement.description = description
        if main_photo is not None:
            db_announcement.main_photo = main_photo
        if attachments is not None:
            db_announcement.attachments = attachments
        if price is not None:
            db_announcement.price = price
        
        self.db.add(db_announcement)
        await self.db.commit()
        await self.db.refresh(db_announcement)
        return db_announcement

    async def delete(self, announcement_id: int):
        db_announcement = await self.get(announcement_id)
        if db_announcement is None:
            return None
        
        await self.db.delete(db_announcement)
        await self.db.commit()
        return db_announcement


class DeviceDAL:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, account_id: int, name: str, last_ip: str = None, user_agent: str = None):
        db_device = Device(
            account_id=account_id,
            name=name,
            last_ip=last_ip,
            user_agent=user_agent
        )
        self.db.add(db_device)
        await self.db.commit()
        await self.db.refresh(db_device)
        return db_device

    async def get(self, device_id: int):
        result = await self.db.execute(select(Device).where(Device.id == device_id))
        return result.scalar_one_or_none()

    async def get_all(self, account_id: int):
        result = await self.db.execute(
            select(Device)
            .where(Device.account_id == account_id)
        )
        return result.scalars().all()

    async def update(self, device_id: int, name: str = None, last_ip: str = None, user_agent: str = None):
        db_device = await self.get(device_id)
        if db_device is None:
            return None
        
        if name is not None:
            db_device.name = name
        if last_ip is not None:
            db_device.last_ip = last_ip
        if user_agent is not None:
            db_device.user_agent = user_agent
        
        self.db.add(db_device)
        await self.db.commit()
        await self.db.refresh(db_device)
        return db_device

    async def delete(self, device_id: int):
        db_device = await self.get(device_id)
        if db_device is None:
            return None
        
        await self.db.delete(db_device)
        await self.db.commit()
        return db_device