from sqlalchemy import Column, String, Boolean, Float, Integer, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey('user_roles.id'), nullable=False)
    subject_type_id = Column(Integer, ForeignKey('subject_types.id'), nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=False)


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    account_name = Column(String, nullable=False)
    account_secret = Column(String, nullable=False)
    created_at = Column(String, nullable=False)


class Auth(Base):
    __tablename__ = 'auth'

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    device_id = Column(Integer, ForeignKey('devices.id'), nullable=False)
    timestamp = Column(String, default=datetime.now())
    token = Column(String, nullable=False)



class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    name = Column(String, nullable=False)
    last_ip = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)



class UserRole(Base):
    __tablename__ = 'user_roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

class SubjectType(Base):
    __tablename__ = 'subject_types'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)


class Platform(Base):
    __tablename__ = 'platforms'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    url = Column(String, nullable=True)


class AnnouncementType(Base):
    __tablename__ = 'announcement_types'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)


class AdFormat(Base):
    __tablename__ = 'ad_formats'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)



class Announcement(Base):
    __tablename__ = 'announcements'

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date_publish = Column(DateTime, default=datetime.now)
    count_views = Column(Integer, default=0)
    title = Column(String, nullable=False)
    main_photo = Column(String, nullable=True)
    description = Column(String, nullable=True)
    attachments = Column(String, nullable=True)
    price = Column(Float, nullable=True)
    type_id = Column(Integer, ForeignKey('announcement_types.id'), nullable=False)
    platform_id = Column(Integer, ForeignKey('platforms.id'), nullable=False)
    format_id = Column(Integer, ForeignKey('ad_formats.id'), nullable=False)


