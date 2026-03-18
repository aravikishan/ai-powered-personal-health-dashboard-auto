from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Database setup
DATABASE_URL = "sqlite:///./health_dashboard.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)

class HealthMetric(Base):
    __tablename__ = "health_metrics"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String)
    value = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user = relationship("User")

class Insight(Base):
    __tablename__ = "insights"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User")

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Seed data
def seed_data():
    db = SessionLocal()
    if not db.query(User).first():
        user = User(name="John Doe", email="john@example.com", password_hash="hashed_password")
        db.add(user)
        db.commit()
        db.refresh(user)
        metric = HealthMetric(user_id=user.id, name="Weight", value=70.5)
        db.add(metric)
        insight = Insight(user_id=user.id, title="Stay Hydrated", description="Drink at least 8 glasses of water a day.")
        db.add(insight)
        db.commit()
    db.close()

seed_data()

# Routes
@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/profile", response_class=HTMLResponse)
async def read_profile(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})

@app.get("/data", response_class=HTMLResponse)
async def read_data_management(request: Request):
    return templates.TemplateResponse("data.html", {"request": request})

@app.get("/insights", response_class=HTMLResponse)
async def read_insights(request: Request):
    return templates.TemplateResponse("insights.html", {"request": request})

@app.get("/settings", response_class=HTMLResponse)
async def read_settings(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request})

@app.get("/api/metrics")
async def get_metrics():
    db = SessionLocal()
    metrics = db.query(HealthMetric).all()
    db.close()
    return metrics

@app.post("/api/data/upload")
async def upload_data():
    # Logic for uploading data
    return {"message": "Data uploaded successfully"}

@app.get("/api/insights")
async def get_insights():
    db = SessionLocal()
    insights = db.query(Insight).all()
    db.close()
    return insights

@app.get("/api/user/profile")
async def get_user_profile():
    db = SessionLocal()
    user = db.query(User).first()
    db.close()
    return user

@app.put("/api/user/profile")
async def update_user_profile():
    # Logic for updating user profile
    return {"message": "Profile updated successfully"}
