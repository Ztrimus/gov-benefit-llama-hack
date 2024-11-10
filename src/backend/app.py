from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from typing import Optional
import uuid
import os
from dotenv import load_dotenv
from datetime import date, datetime
from together import Together

# Import for Google OAuth verification
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from src.functions.crawl.web import get_matching_embedding, initialize_pinecone_index

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
    https_only=False,  # Set to True in production
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
    user_id = Column(
        Integer, ForeignKey("users.id")
    )  # Associate grants with a specific user
    user = relationship("User")  # Define relationship with User


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
    email: Optional[str] = None
    demographics: Optional[str] = None
    affiliated_organization: Optional[str] = None
    birthdate: Optional[str] = None  # Changed to date


class CheckProfileResponse(BaseModel):
    profileExists: bool


class CreateGrantRequest(BaseModel):
    name: str
    deadline: date
    documents_needed: str
    steps_to_apply: str
    link: str


class EmailRequest(BaseModel):
    email: str


# Authentication Endpoint
@app.post("/auth")
async def auth(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    token = data.get("token")
    if not token:
        raise HTTPException(status_code=400, detail="Token not provided.")
    try:
        print(f"Received Token: {token}")  # Debugging line

        # Verify the token with Google's OAuth2 API
        id_info = id_token.verify_oauth2_token(
            token, google_requests.Request(), os.getenv("GOOGLE_CLIENT_ID")
        )
        print(f"ID Info: {id_info}")  # Debugging line

        # Extract user info
        user_email = id_info["email"]
        user_name = id_info.get("name", "")
        # Check if user exists in DB
        user = db.query(User).filter(User.email == user_email).first()
        if not user:
            user = User(email=user_email, name=user_name)
            db.add(user)
            db.commit()
            db.refresh(user)
        # Store user info in session
        request.session["user"] = {"email": user_email, "name": user_name}
        return {
            "message": "Login successful",
            "user": {"email": user_email, "name": user_name},
        }
    except ValueError as ve:
        print(f"Token verification failed: {ve}")  # Debugging line
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        print(f"Unexpected error during authentication: {e}")  # Debugging line
        raise HTTPException(status_code=500, detail="Internal server error")


# Dependency to get the current user
async def get_current_user(request: Request, db: Session = Depends(get_db)):
    user_info = request.session.get("user")
    if not user_info:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    user = db.query(User).filter(User.email == user_info["email"]).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


# Logout Endpoint
@app.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return {"message": "Logged out successfully"}


# Grants Endpoint (for user-specific grants)
@app.post("/grants")
def get_grants(request: EmailRequest, db: Session = Depends(get_db)):
    current_user = db.query(User).filter(User.email == request.email).first()
    if current_user:
        user_info = f"""# USER INFO
        - Occupation: {current_user.occupation}
        - Income: {current_user.income}
        - Demographics: {current_user.demographics}
        - Affiliated Organization: {current_user.affiliated_organization}
        - Birthdate: {current_user.birthdate}
        """

        query = f"""What kind of benefits government offers to citizen having:
        {user_info}
        """

        pc = initialize_pinecone_index()
        results = get_matching_embedding(pc, query)

        prompt_with_relevant_data = f"""# RELEVANT KNOWLEDGE\n\n
        {"\n".join([match['metadata']['text'] for match in results["matches"]])}
        """

        prompt = f"""
        Tell user what kind of benefit they will have based on their information, relevant knowledge and your knowledge:
        {prompt_with_relevant_data}
        {user_info}
        Answer in bulleted points, and provide a link to the relevant government website.
        """

        client = Together()

        completion = client.chat.completions.create(
            model="meta-llama/Llama-3.2-3B-Instruct-Turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Provide clear, accessible information to help underprivileged citizens understand the government benefits they may qualify for. Present details on financial aid, healthcare, food assistance, housing, education, and disability support. Keep the information simple, organized, and free of jargon. Include eligibility criteria, application steps, and common documentation needed. Address any barriers, like language, digital literacy, and complex processes, with straightforward guidance.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        return {"content": completion.choices[0].message.content}
    else:
        raise HTTPException(status_code=404, detail="User not found.")


# Apply Grant Endpoint
@app.post("/apply-grant")
def apply_grant(
    request: ApplyGrantRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    grant = db.query(Grant).filter(Grant.id == request.grant_id).first()
    if grant:
        applied_grant = AppliedGrant(
            id=str(uuid.uuid4()),
            user_id=current_user.id,
            grant_id=grant.id,
            status=10,  # Initial status set to 10%
            current_status="Application Submitted",
        )
        db.add(applied_grant)
        db.commit()
        db.refresh(applied_grant)
        return {
            "message": "Application submitted successfully.",
            "appliedGrant": applied_grant,
        }
    else:
        raise HTTPException(status_code=404, detail="Grant not found.")


# Get Applied Grants Endpoint
@app.get("/applied-grants")
def get_applied_grants(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    applied_grants = (
        db.query(AppliedGrant).filter(AppliedGrant.user_id == current_user.id).all()
    )
    return applied_grants


# Update Grant Status Endpoint
@app.put("/update-grant-status")
def update_grant_status(
    request: UpdateGrantStatusRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    grant = (
        db.query(AppliedGrant)
        .filter(
            AppliedGrant.id == request.grant_id, AppliedGrant.user_id == current_user.id
        )
        .first()
    )
    if grant:
        grant.status = request.status
        grant.current_status = request.currentStatus
        db.commit()
        return {"message": "Grant status updated successfully.", "updatedGrant": grant}
    else:
        raise HTTPException(status_code=404, detail="Applied grant not found.")


# Check Profile Endpoint
@app.post("/auth/check-profile", response_model=CheckProfileResponse)
def check_profile(request: EmailRequest, db: Session = Depends(get_db)):
    current_user = db.query(User).filter(User.email == request.email).first()
    required_fields = [
        current_user.occupation,
        current_user.income,
        current_user.demographics,
        current_user.affiliated_organization,
        current_user.birthdate,
    ]
    profile_exists = all(field is not None and field != "" for field in required_fields)
    return {"profileExists": profile_exists}


# Create Grant Endpoint for Specific User
@app.post("/create-grant")
def create_grant(
    request: CreateGrantRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    new_grant = Grant(
        id=str(uuid.uuid4()),
        name=request.name,
        deadline=request.deadline,
        documents_needed=request.documents_needed,
        steps_to_apply=request.steps_to_apply,
        link=request.link,
        user_id=current_user.id,  # Assign the grant to the current user
    )
    db.add(new_grant)
    db.commit()
    db.refresh(new_grant)
    return {"message": "Grant created successfully.", "grant": new_grant}


# Update User Profile Endpoint
@app.post("/update-profile")
def update_user_profile(request: UserProfileRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if request.occupation is not None:
        user.occupation = request.occupation
    if request.income is not None:
        user.income = request.income
    if request.demographics is not None:
        user.demographics = request.demographics
    if request.affiliated_organization is not None:
        user.affiliated_organization = request.affiliated_organization
    if request.birthdate is not None:
        try:
            user.birthdate = datetime.strptime(request.birthdate, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Invalid birthdate format. Use YYYY-MM-DD."
            )
    db.commit()
    db.refresh(user)
    return {"message": "Profile updated successfully.", "user": user}


# Run the app
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
