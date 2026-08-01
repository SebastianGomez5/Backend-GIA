from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import user_schema
from app.services import user_service
from app.db.session import get_db
from app.api import deps
from app.db import models

router = APIRouter()


@router.post("/register", response_model=user_schema.UserResponse)
def register_user(
    user: user_schema.UserCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint público de registro. NO requiere autenticación,
    ya que es el punto de entrada para nuevos usuarios.
    """
    # Verificamos que el correo no esté ya registrado
    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Ya existe una cuenta registrada con este correo."
        )

    return user_service.create_user(db=db, user=user)


@router.get("/me", response_model=user_schema.UserResponse)
def read_user_me(current_user: models.User = Depends(deps.get_current_user)):
    # Simplemente devolvemos el usuario que ya fue validado por el token
    return current_user

@router.put("/me/name", response_model=user_schema.UserResponse)
def update_name(
    name_data: user_schema.UserNameUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    if not name_data.name.strip():
        raise HTTPException(status_code=400, detail="El nombre no puede estar vacío.")

    updated_user = user_service.update_name(db, current_user.id, name_data.name.strip())
    return updated_user

@router.put("/me/password")
def update_password(
    password_data: user_schema.UserPasswordUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    success = user_service.update_password(db, current_user.id, password_data)
    if not success:
        raise HTTPException(status_code=400, detail="La contraseña actual es incorrecta.")
    return {"mensaje": "Contraseña actualizada exitosamente."}