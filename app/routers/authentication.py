from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..database import getDatabase
from .. import schemas, models, ultis, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter ()

# authenitcate user by email and password through body request
@router.post ("/auth", status_code = status.HTTP_200_OK)
def login (user_credential: schemas.User, database: Session = Depends (getDatabase)):
    user = database.query (models.User).filter (models.User.email == user_credential.email).first ()
    
    if not user:
        raise HTTPException (status_code = status.HTTP_404_NOT_FOUND,
                             detail = "invalid credential")
    
    if not ultis.verify_password (user_credential.password, user.password):
        raise HTTPException (status_code = status.HTTP_404_NOT_FOUND,
                             detail = "invalid password")
    
    access_token = oauth2.create_access_token (data = {"user_id": user.id})
    
    return access_token

# check login through OAuth2PasswordRequestForm
@router.post ("/login", status_code = status.HTTP_200_OK, response_model = schemas.Token)
def login (user_credential: OAuth2PasswordRequestForm = Depends (), database: Session = Depends (getDatabase)):

    # structure of user_credential
    # username ~ email in the DB
    # password
    # => {
    #       "username": "name",
    #       "password": "pass"
    #    }
    user = database.query (models.User).filter (models.User.email == user_credential.username).first ()
    
    if not user:
        raise HTTPException (status_code = status.HTTP_403_FORBIDDEN,
                             detail = "invalid credential")
    
    if not ultis.verify_password (user_credential.password, user.password):
        raise HTTPException (status_code = status.HTTP_403_FORBIDDEN,
                             detail = "invalid password")
    update_command = text ("UPDATE users SET is_loggin = true WHERE id = {}".format (user.id))
    database.execute (update_command)
    database.commit ()
    
    access_token = oauth2.create_access_token (data = {"user_name": user.email})
    access_JWT_token = {"access_token": access_token, "token_type": "bearer"}
    return access_JWT_token

@router.put ("/logout", status_code = status.HTTP_200_OK)
def finishSession (token = Depends(oauth2.oauth2_scheme), database: Session = Depends (getDatabase), user = Depends (oauth2.get_current_user)):
    current_user = database.query (models.User).filter (models.User.id == user.id).first ()
    current_user.is_loggin = False
    database.commit ()
    
    revoked_token = models.TokenJWT (
        expired_token = token
    )
    database.add (revoked_token)
    database.commit ()
    return {"message" : "successfull"}
    

