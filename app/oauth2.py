import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from . import schemas, models
from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from . database import getDatabase
from . config import settings
oauth2_scheme = OAuth2PasswordBearer (tokenUrl='login')

# secret key
SECRET_KEY = settings.secret_key
# algorithm
ALGORITHM = settings.algorithm
# expriration time
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expired_minutes

revoked_tokens = set ()

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token (token: str, credentials_expception, token_lake: Session = Depends (getDatabase)):
    try:
        payload = jwt.decode (token, SECRET_KEY, algorithms = [ALGORITHM])
        user_name: str = payload.get ("user_name")
        if user_name is None:
            raise credentials_expception
        token_data = schemas.TokenData(user_name_token = user_name)
    except InvalidTokenError:
        raise credentials_expception
    
    return token_data

def get_current_user (token: str = Depends (oauth2_scheme), database: Session = Depends (getDatabase)):
    all_token = database.query(models.TokenJWT).all ()
    for current_token in all_token:
        if token == current_token.expired_token:
            raise HTTPException (status_code = status.HTTP_400_BAD_REQUEST
                                 , detail = "token has been expired")
        
    credentials_exception = HTTPException (status_code = status.HTTP_401_UNAUTHORIZED
                                           , detail = "could not verify"
                                           , headers ={"WWW-Authenticate": "Bearer"})
    current_user =  verify_token (token, credentials_exception)
    user = database.query (models.User).filter (models.User.email == current_user.user_name_token).first ()
    return user 

