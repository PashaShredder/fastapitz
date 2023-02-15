from fastapi import APIRouter, Depends, HTTPException
from api.auth import schema, crud
from api.utils import cryptoUtil, jwtUtil, constantUtil
from fastapi.security import OAuth2PasswordRequestForm



router = APIRouter(
    prefix="/api/v1"
)

@router.post("/auth/register", response_model=schema.UserList)
async def register(user: schema.UserCreate):
    #  check user exist
    result = await crud.find_exist_user(user.email)
    if result:
        raise HTTPException(status_code=404, detail="User already registered.")

    # create new user
    user.password = cryptoUtil.hash_password(user.password)
    await crud.save_user(user)
    return {**user.dict()}

@router.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    result = await crud.find_exist_user(form_data.username)
    if not result:
        raise HTTPException(status_code=404, detail="User not found.")

    user = schema.UserCreate(**result)
    verified_password = cryptoUtil.verify_password(form_data.password, user.password)
    if not verified_password:
        raise HTTPException(status_code=404, detail="Incorrect username or password")

    access_token_expire = jwtUtil.timedelta(minutes=constantUtil.ACCESS_TOKEN_EXPIRE_MINUT)
    access_token = await jwtUtil.create_access_token(
        data={"sub": form_data.username},
        expires_delta=access_token_expire
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_info":{
            "email":user.email,
            "fullname":user.fullname
        }
    }
