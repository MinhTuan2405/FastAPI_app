from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, ultis, oauth2
from ..database import getDatabase
from sqlalchemy.orm import Session


router = APIRouter (
    prefix = "/user"# all the router has prefix = /user
                    # such as, /createUser => mean: http://127.0.0.1:8000/user/createUser
)

@router.post ("/createUser", status_code = status.HTTP_201_CREATED, response_model = schemas.responseUserModel)
def createUser (newUser: schemas.User, database: Session = Depends (getDatabase)):

    def checkUser (user: schemas.User):
        if user.email == "" or user.password == "":
            return False
        return True
    
    if not checkUser (newUser):
        raise HTTPException (status_code = status.HTTP_406_NOT_ACCEPTABLE, 
                             detail = "can not create with blank information")
    
    hashed_password = ultis.hashingPassword (newUser.password)
    newUser.password = hashed_password

    new_user = models.User (**newUser.dict ())
    database.add (new_user)
    database.commit ()
    database.refresh (new_user)
    return new_user

@router.put ("/updateEmail", status_code = status.HTTP_200_OK)
def changeTheUserInfor_USERNAME (newUser: schemas.updateUserEmail, database: Session = Depends (getDatabase), user = Depends (oauth2.get_current_user)):
    try:
        changedUser = database.query (models.User).filter (models.User.id == user.id).first ()
        changedUser.email = newUser.new_email
        database.commit ()
        return {"message": "change the email successful"}
    except:
        raise HTTPException (status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                             , detail = "can not change the user email")
    
@router.put ("/updatePassword", status_code = status.HTTP_200_OK)
def changeTheUserInfor_PASSWORD (newUserPassword: schemas.updateUserPassword, database: Session = Depends (getDatabase), user = Depends (oauth2.get_current_user)):
    try:
        newHashPassword = newUserPassword.new_password
        newHashPassword = ultis.hashingPassword (newHashPassword)
        currentUser = database.query (models.User).filter (models.User.id == user.id).first ()
        currentUser.password = newHashPassword
        database.commit ()
        return {"message": "change the password successful"}
    except:
        raise HTTPException (status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                             , detail = "can not change the password of the user")


@router.get ("/{id}", status_code = status.HTTP_200_OK, response_model = schemas.responseUserModel)
def getUserByID (id: int, database: Session = Depends (getDatabase)):
    user = database.query (models.User).filter (models.User.id == id).first ()
    if not user:
        raise HTTPException (status_code = status.HTTP_404_NOT_FOUND,
                             detail = "user is not exist")
    return user