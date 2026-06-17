from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    plants = relationship("Plant", secondary="user_plants", back_populates="users")

user_plants = Table(
    "user_plants",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("plant_id", Integer, ForeignKey("plants.id"), primary_key=True),
)

class Plant(Base):
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    location = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    users = relationship("User", secondary="user_plants", back_populates="plants")
    machines = relationship("Machine", back_populates="plant")
    productions = relationship("Production", back_populates="plant")
    activity_logs = relationship("ActivityLog", back_populates="plant")
    alerts = relationship("Alert", back_populates="plant")


class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    machine_type = Column(String(100), nullable=True)
    status = Column(String(50), default="Stopped")  # Running, Stopped, Maintenance
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    plant = relationship("Plant", back_populates="machines")
    productions = relationship("Production", back_populates="machine")


class Production(Base):
    __tablename__ = "productions"

    id = Column(Integer, primary_key=True, index=True)
    units_produced = Column(Integer, default=0)
    target_units = Column(Integer, default=0)
    date = Column(DateTime(timezone=True), server_default=func.now())
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    machine_id = Column(Integer, ForeignKey("machines.id"), nullable=False)

    plant = relationship("Plant", back_populates="productions")
    machine = relationship("Machine", back_populates="productions")


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    event = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)  # Running, Completed, Maintenance
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    plant = relationship("Plant", back_populates="activity_logs")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String(255), nullable=False)
    severity = Column(String(50), default="info")  # info, warning, critical
    is_active = Column(Boolean, default=True)
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    plant = relationship("Plant", back_populates="alerts")