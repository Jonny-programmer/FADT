from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import crud, schemas
from ..dependencies import get_db_session, oauth2_scheme

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(oauth2_scheme)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db_session)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db_session)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db_session)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)
