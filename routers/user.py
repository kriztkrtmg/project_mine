from fastapi import APIRouter
from models.user_model import createUserModel, dataResponse, loginUserModel
from services.user_service import userServiceClass

router = APIRouter(prefix="/auth", tags=["User"])

@router.post("/register", response_model=dataResponse)
async def user_register(data : createUserModel):
    return await userServiceClass().register_user(data)

@router.post("/login", response_model=dataResponse)
async def user_login(data : loginUserModel):
    return await userServiceClass().login_user(data)