from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import schemas, crud
from ..dependencies import get_db_session, oauth2_scheme

router = APIRouter(
    prefix="/items",
    tags=["items"],
    # dependencies=[Depends(oauth2_scheme)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
