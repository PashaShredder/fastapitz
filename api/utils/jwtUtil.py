import jwt
from datetime import datetime, timedelta
from api.utils import constantUtil

async def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=constantUtil.ACCESS_TOKEN_EXPIRE_MINUT)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, constantUtil.SECRET_KEY, algorithm=constantUtil.ALGORITHM_HS256)