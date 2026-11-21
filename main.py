from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Service
from schemas import ServiceCreate, ServiceResponse

# Crear la tabla en Neon si todavía no existe
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Services API")


# ====================================
# GET: 
# ====================================
@app.get("/services", response_model=list[ServiceResponse])
def get_service(db: Session = Depends(get_db)):
    service = db.query(Service).all()
    return service


# ====================================
# GET: 
# ====================================
@app.get("/services/{service_id}", response_model=ServiceResponse)
def get_service(
   service_id: int,
    db: Session = Depends(get_db)
):
    service = db.query(Service).filter(
        Service.id == service_id
    ).first()

    if service is None:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    return service


# ====================================
# POST: 
# ====================================
@app.post("/services", response_model=ServiceResponse, status_code=201)
def create_service(
    data: ServiceCreate,
    db: Session = Depends(get_db)
):
    # Validar que el correo no esté registrado
    existing = db.query(Service).filter(
        Service.price == data.price
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Price already registered"
        )

    service = Service(
        name=data.name,
        price=data.price,
        description=data.description
    )

    db.add(service)
    db.commit()
    db.refresh(service)

    return service

