
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

class LoginRequest(BaseModel):
    username: str
    password: str

from fastapi import Request


@router.post("/login")
def login(request: LoginRequest, fastapi_req: Request):
    settings = fastapi_req.app.state.container.settings
    expected_user = settings.server.admin_username
    expected_pass = settings.server.admin_password
    
    if request.username == expected_user and request.password == expected_pass:
        return {"token": "aiseo-admin-session-token"}
    
    raise HTTPException(status_code=401, detail="Invalid credentials")
