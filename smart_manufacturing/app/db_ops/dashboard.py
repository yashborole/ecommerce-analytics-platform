from sqlalchemy import func
from app import models
from app.database import SessionLocal


def get_kpis(plant_id: int):
    try:
        db = SessionLocal()
        total_production = db.query(
            func.coalesce(func.sum(models.Production.units_produced), 0)
        ).filter(models.Production.plant_id == plant_id).scalar()

        total_machines = db.query(models.Machine).filter(
            models.Machine.plant_id == plant_id
        ).count()

        active_machines = db.query(models.Machine).filter(
            models.Machine.plant_id == plant_id,
            models.Machine.status == "Running"
        ).count()

        downtime_machines = db.query(models.Machine).filter(
            models.Machine.plant_id == plant_id,
            models.Machine.status == "Maintenance"
        ).count()

        efficiency = round((active_machines / total_machines * 100), 1) if total_machines > 0 else 0.0

        active_alerts = db.query(models.Alert).filter(
            models.Alert.plant_id == plant_id,
            models.Alert.is_active == True
        ).count()

        return {
            "total_production": total_production,
            "active_machines": active_machines,
            "total_machines": total_machines,
            "efficiency": efficiency,
            "active_alerts": active_alerts,
            "downtime_machines": downtime_machines,
        }
    except Exception as e:
        return {"error": str(e)}


def get_recent_activity(plant_id: int, limit: int = 10):
    try:
        db = SessionLocal()
        logs = db.query(models.ActivityLog).filter(
            models.ActivityLog.plant_id == plant_id
        ).order_by(models.ActivityLog.timestamp.desc()).limit(limit).all()
        return logs
    except Exception as e:
        return {"error": str(e)}


def get_active_alerts(plant_id: int):
    try:
        db = SessionLocal()
        alerts = db.query(models.Alert).filter(
            models.Alert.plant_id == plant_id,
            models.Alert.is_active == True
        ).order_by(models.Alert.created_at.desc()).all()
        return alerts
    except Exception as e:
        return {"error": str(e)}
