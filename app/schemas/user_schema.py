from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID

# Esquema para CREAR un usuario. 
# Nota: EmailStr valida automáticamente que el texto tenga formato de correo (@ y .com)
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# Esquema para RESPONDER. 
# Nunca, bajo ninguna circunstancia, devolvemos la contraseña en la respuesta.
class UserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)