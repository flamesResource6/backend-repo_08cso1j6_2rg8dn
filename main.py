import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import User, Course, Lesson, Enrollment, Session

app = FastAPI(title="Consultancy LMS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Helpers
class IdModel(BaseModel):
    id: str


def ensure_db():
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")


@app.get("/")
def read_root():
    return {"message": "Consultancy LMS Backend running"}


@app.get("/test")
def test_database():
    """Simple test to check DB connectivity and list a few collections"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": [],
    }
    try:
        ensure_db()
        response["database"] = "✅ Available"
        response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
        response["database_name"] = db.name if hasattr(db, "name") else "❌ Unknown"
        response["connection_status"] = "Connected"
        response["collections"] = db.list_collection_names()[:10]
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:120]}"
    return response


# Minimal CRUD endpoints
@app.post("/users", response_model=dict)
def create_user(payload: User):
    ensure_db()
    _id = create_document("user", payload)
    return {"id": _id}


@app.get("/users", response_model=List[dict])
def list_users():
    ensure_db()
    docs = get_documents("user", {}, limit=50)
    for d in docs:
        d["id"] = str(d.pop("_id"))
    return docs


@app.post("/courses", response_model=dict)
def create_course(payload: Course):
    ensure_db()
    _id = create_document("course", payload)
    return {"id": _id}


@app.get("/courses", response_model=List[dict])
def list_courses():
    ensure_db()
    docs = get_documents("course")
    for d in docs:
        d["id"] = str(d.pop("_id"))
    return docs


@app.post("/lessons", response_model=dict)
def create_lesson(payload: Lesson):
    ensure_db()
    _id = create_document("lesson", payload)
    return {"id": _id}


@app.get("/lessons", response_model=List[dict])
def list_lessons(course_id: Optional[str] = None):
    ensure_db()
    filter_dict = {"course_id": course_id} if course_id else {}
    docs = get_documents("lesson", filter_dict)
    for d in docs:
        d["id"] = str(d.pop("_id"))
    return docs


@app.post("/enrollments", response_model=dict)
def enroll(payload: Enrollment):
    ensure_db()
    _id = create_document("enrollment", payload)
    return {"id": _id}


@app.get("/enrollments", response_model=List[dict])
def list_enrollments(user_id: Optional[str] = None, course_id: Optional[str] = None):
    ensure_db()
    filter_dict = {}
    if user_id:
        filter_dict["user_id"] = user_id
    if course_id:
        filter_dict["course_id"] = course_id
    docs = get_documents("enrollment", filter_dict)
    for d in docs:
        d["id"] = str(d.pop("_id"))
    return docs


@app.post("/sessions", response_model=dict)
def create_session(payload: Session):
    ensure_db()
    _id = create_document("session", payload)
    return {"id": _id}


@app.get("/sessions", response_model=List[dict])
def list_sessions(consultant_id: Optional[str] = None, user_id: Optional[str] = None):
    ensure_db()
    filter_dict = {}
    if consultant_id:
        filter_dict["consultant_id"] = consultant_id
    if user_id:
        filter_dict["user_id"] = user_id
    docs = get_documents("session", filter_dict)
    for d in docs:
        d["id"] = str(d.pop("_id"))
    return docs


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
