from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, ultis, oauth2
from ..database import getDatabase
from sqlalchemy.orm import Session

router = APIRouter (
    prefix = "/vote"
)

@router.post ("/", status_code = status.HTTP_201_CREATED)
def vote (vote: schemas.Votes, database: Session = Depends (getDatabase), user = Depends (oauth2.get_current_user)):
    post = database.query (models.Post).filter (models.Post.id == vote.post_id).first ()
    if not post:
        raise HTTPException (status_code = status.HTTP_404_NOT_FOUND
                            , detail = "the post is not exist")
    data_vote = database.query (models.Votes).filter (models.Votes.post_id == vote.post_id, models.Votes.user_id == user.id)
    found_vote = data_vote.first ()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException (status_code = status.HTTP_409_CONFLICT
                                 , detail = "this post has been voted by yourself")
        new_vote = models.Votes (
            user_id = user.id,
            post_id = vote.post_id
        )
        database.add (new_vote)
        database.commit ()
        return {"message": "successfully voting"}
    else:
        if not found_vote:
            raise HTTPException (status_code = status.HTTP_404_NOT_FOUND
                                 , detail = "vote is not existed for deleting")
        data_vote.delete (synchronize_session = False)
        database.commit ()
        return {"message": "successfully unvoting"}