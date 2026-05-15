from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List, Optional
from app.database import engine, get_db, Base
from app.models import User, Note
from app.schemas import (
    UserCreate, UserLogin, Token, NoteCreate, NoteUpdate, 
    NoteResponse, NoteShare, NotePinToggle
)
from app.auth import (
    get_password_hash, verify_password, create_access_token, 
    get_current_user
)
from app.config import get_settings

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Notes API",
    description="A secure notes management API with sharing capabilities",
    version="1.0.0"
)

settings = get_settings()

@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {"message": "User created successfully", "email": db_user.email}

@app.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    return register(user, db)

@app.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/notes", response_model=List[NoteResponse])
def get_notes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Note).filter(
        (Note.owner_id == current_user.id) | (Note.shared_with.any(id=current_user.id))
    )
    
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (Note.title.ilike(search_pattern)) | (Note.content.ilike(search_pattern))
        )
    
    notes = query.order_by(Note.is_pinned.desc(), Note.updated_at.desc()).offset(skip).limit(limit).all()
    return notes

@app.get("/notes/{id}", response_model=NoteResponse)
def get_note(id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == id).first()
    
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    
    if note.owner_id != current_user.id and current_user not in note.shared_with:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    return note

@app.post("/notes", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(
    note: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_note = Note(**note.dict(), owner_id=current_user.id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@app.put("/notes/{id}", response_model=NoteResponse)
def update_note(
    id: int,
    note: NoteUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_note = db.query(Note).filter(Note.id == id).first()
    
    if not db_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    
    if db_note.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owner can update")
    
    for key, value in note.dict().items():
        setattr(db_note, key, value)
    
    db.commit()
    db.refresh(db_note)
    return db_note

@app.delete("/notes/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_note = db.query(Note).filter(Note.id == id).first()
    
    if not db_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    
    if db_note.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owner can delete")
    
    db.delete(db_note)
    db.commit()
    return None

@app.post("/notes/{id}/share")
def share_note(
    id: int,
    share_data: NoteShare,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_note = db.query(Note).filter(Note.id == id).first()
    
    if not db_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    
    if db_note.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owner can share")
    
    share_user = db.query(User).filter(User.email == share_data.share_with_email).first()
    if not share_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if share_user.id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot share with yourself")
    
    if share_user in db_note.shared_with:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Note already shared with this user")
    
    db_note.shared_with.append(share_user)
    db.commit()
    
    return {"message": f"Note shared successfully with {share_data.share_with_email}"}

@app.post("/notes/{id}/pin")
def toggle_pin_note(
    id: int,
    pin_data: NotePinToggle,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_note = db.query(Note).filter(Note.id == id).first()
    
    if not db_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    
    if db_note.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owner can pin/unpin")
    
    db_note.is_pinned = pin_data.is_pinned
    db.commit()
    
    action = "pinned" if pin_data.is_pinned else "unpinned"
    return {"message": f"Note {action} successfully"}

@app.get("/search")
def search_notes(
    q: str = Query(..., min_length=1),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    search_pattern = f"%{q}%"
    notes = db.query(Note).filter(
        ((Note.owner_id == current_user.id) | (Note.shared_with.any(id=current_user.id))) &
        ((Note.title.ilike(search_pattern)) | (Note.content.ilike(search_pattern)))
    ).order_by(Note.updated_at.desc()).all()
    
    return [NoteResponse.from_orm(note) for note in notes]

@app.get("/openapi.json")
def get_openapi():
    return app.openapi()

@app.get("/about")
def about():
    return {
        "name": "Varshith",
        "email": "varshithg2004@gmail.com",
        "my_features": {
            "Pin Notes": "Users can pin important notes to keep them at the top of their list. This helps with quick access to frequently used notes.",
            "Full-text Search": "Implemented search functionality across note titles and content with query parameter support.",
            "Pagination": "Added skip and limit parameters to the GET /notes endpoint for efficient data loading.",
            "Comprehensive Validation": "All endpoints have proper input validation, error handling, and security checks.",
            "Note Sharing": "Users can share notes with other users via email, enabling collaboration."
        }
    }

@app.get("/")
def root():
    return {"message": "Notes API is running", "docs": "/docs"}
