from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Optional
import uuid
import os
from dotenv import load_dotenv
from datetime import date

# Import for Google OAuth verification
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Debugging: Print GOOGLE_CLIENT_ID to ensure it's loaded correctly
print(f"GOOGLE_CLIENT_ID: {os.getenv('GOOGLE_CLIENT_ID')}")

# Enable CORS for frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session Middleware for OAuth
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY", "mysecret"),
    same_site="lax",
    https_only=False  # Set to True in production
)

# Database setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    occupation = Column(String, nullable=True)
    income = Column(String, nullable=True)
    demographics = Column(String, nullable=True)
    affiliated_organization = Column(String, nullable=True)
    birthdate = Column(Date, nullable=True)

class Grant(Base):
    __tablename__ = "grants"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    deadline = Column(Date)
    documents_needed = Column(String)
    steps_to_apply = Column(String)
    link = Column(String)

class AppliedGrant(Base):
    __tablename__ = "applied_grants"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(Integer)
    grant_id = Column(String)
    status = Column(Integer)
    current_status = Column(String)

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Data Models
class ApplyGrantRequest(BaseModel):
    grant_id: str

class UpdateGrantStatusRequest(BaseModel):
    grant_id: str
    status: int
    currentStatus: str

class UserProfileRequest(BaseModel):
    occupation: Optional[str] = None
    income: Optional[str] = None
    demographics: Optional[str] = None
    affiliated_organization: Optional[str] = None
    birthdate: Optional[date] = None  # Changed to date

class CheckProfileResponse(BaseModel):
    profileExists: bool

# Authentication Endpoint
@app.post("/auth")
async def auth(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    token = data.get('token')
    if not token:
        raise HTTPException(status_code=400, detail="Token not provided.")
    try:
        print(f"Received Token: {token}")  # Debugging line

        # Verify the token with Google's OAuth2 API
        id_info = id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            os.getenv("GOOGLE_CLIENT_ID")
        )
        print(f"ID Info: {id_info}")  # Debugging line

        # Extract user info
        user_email = id_info['email']
        user_name = id_info.get('name', '')
        # Check if user exists in DB
        user = db.query(User).filter(User.email == user_email).first()
        if not user:
            user = User(email=user_email, name=user_name)
            db.add(user)
            db.commit()
            db.refresh(user)
        # Store user info in session
        request.session['user'] = {'email': user_email, 'name': user_name}
        return {"message": "Login successful", "user": {'email': user_email, 'name': user_name}}
    except ValueError as ve:
        print(f"Token verification failed: {ve}")  # Debugging line
        # Invalid token
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        print(f"Unexpected error during authentication: {e}")  # Debugging line
        raise HTTPException(status_code=500, detail="Internal server error")

# Dependency to get the current user
async def get_current_user(request: Request, db: Session = Depends(get_db)):
    user_info = request.session.get('user')
    if not user_info:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    user = db.query(User).filter(User.email == user_info["email"]).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# Logout Endpoint
@app.get("/logout")
async def logout(request: Request):
    request.session.pop('user', None)
    return {"message": "Logged out successfully"}

# Grants Endpoint
@app.get("/grants")
def get_grants(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    grants = db.query(Grant).all()
    return grants

# Apply Grant Endpoint
@app.post("/apply-grant")
def apply_grant(request: ApplyGrantRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    grant = db.query(Grant).filter(Grant.id == request.grant_id).first()
    if grant:
        applied_grant = AppliedGrant(
            id=str(uuid.uuid4()),
            user_id=current_user.id,
            grant_id=grant.id,
            status=10,  # Initial status set to 10%
            current_status="Application Submitted"
        )
        db.add(applied_grant)
        db.commit()
        db.refresh(applied_grant)
        return {"message": "Application submitted successfully.", "appliedGrant": applied_grant}
    else:
        raise HTTPException(status_code=404, detail="Grant not found.")

# Get Applied Grants Endpoint
@app.get("/applied-grants")
def get_applied_grants(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    applied_grants = db.query(AppliedGrant).filter(AppliedGrant.user_id == current_user.id).all()
    return applied_grants

# Update Grant Status Endpoint
@app.put("/update-grant-status")
def update_grant_status(request: UpdateGrantStatusRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    grant = db.query(AppliedGrant).filter(AppliedGrant.id == request.grant_id, AppliedGrant.user_id == current_user.id).first()
    if grant:
        grant.status = request.status
        grant.current_status = request.currentStatus
        db.commit()
        return {"message": "Grant status updated successfully.", "updatedGrant": grant}
    else:
        raise HTTPException(status_code=404, detail="Applied grant not found.")

class EmailRequest(BaseModel):
    email: str

# Check Profile Endpoint
@app.post("/auth/check-profile", response_model=CheckProfileResponse)
def check_profile(request: EmailRequest, db: Session = Depends(get_db)):
    current_user = db.query(User).filter(User.email == request.email).first()
    # Define what constitutes a complete profile
    required_fields = [
        current_user.occupation,
        current_user.income,
        current_user.demographics,
        current_user.affiliated_organization,
        current_user.birthdate,
    ]
    # Check if all required fields are filled
    profile_exists = all(field is not None and field != "" for field in required_fields)
    return {"profileExists": profile_exists}

# Update User Profile Endpoint
@app.post("/update-profile")
def update_user_profile(request: UserProfileRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == current_user.id).first()
    if user:
        if request.occupation is not None:
            user.occupation = request.occupation
        if request.income is not None:
            user.income = request.income
        if request.demographics is not None:
            user.demographics = request.demographics
        if request.affiliated_organization is not None:
            user.affiliated_organization = request.affiliated_organization
        if request.birthdate is not None:
            user.birthdate = request.birthdate
        db.commit()
        db.refresh(user)
        return {"message": "Profile updated successfully.", "user": user}
    else:
        raise HTTPException(status_code=404, detail="User not found.")

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
