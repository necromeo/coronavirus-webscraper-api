# FastAPI Api to get the results from the Sqlite DB
from typing import List

from fastapi import Depends, FastAPI, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
import locale, logging
from writeDB import write_to_db

# from . import crud, models, schemas
import model
from model import Country
from database import SessionLocal, engine

model.Base.metadata.create_all(bind=engine)

locale.setlocale(locale.LC_ALL, '')
logging.info(locale.getlocale())

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home(
    skip: int = 0,
    db: Session = Depends(get_db),
):
    countries = db.query(Country).all()
    return countries


@app.get('/update')
def updateDB(background_tasks: BackgroundTasks):
    background_tasks.add_task(write_to_db)
    logging.info('Database is being updated...')
    return {'message': 'Database is being updated...'}


@app.get('/{country_name}')
def country(country_name, db: Session = Depends(get_db)):
    cn = country_name.title()
    if country_name == 'usa':
        cn = 'USA'
    country = db.query(Country).filter_by(country=cn).first()
    logging.info(country)
    if country is None:
        raise HTTPException(
            status_code=404, detail=f"{country_name} does not exist"
        )

    return country
