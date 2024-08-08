from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import getDatabase
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

router = APIRouter (
    prefix = "/post" # all the router has prefix = /post
                    # such as, /allPost => mean: http://127.0.0.1:8000/post/allPost
)

@router.get ("/allPost", response_model = List [schemas.responsePostModel_VoteExtra]) # because the allPost is in the list form
                                                                                      # other repsone is in class form
def getAllPosts (database: Session = Depends (getDatabase), user = Depends (oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # the URL: http://prefixURL/allPost?limit=10&skip=0 (user can change the 10 and 0, replace them by another number)
    # the search paramter is optional, you do not need to provide the value for it
    # to indicate the space in the query parameter, use %20 => http://prefixURL/allPost?limit=10&skip=0&search=beach%20florida
    # here is the example of getting someone post wiht the number post from skip to limit (offset and limit in the SQL)

    allPosts = database.query (
        models.Post, func.count (models.Votes.post_id).label ("vote")
        ).outerjoin (
            models.Votes,
            models.Post.id == models.Votes.post_id
        ).group_by (
            models.Post.id
        ).filter (
            models.Post.owner_id == user.id, 
            models.Post.content.contains (search)
        ).limit (limit).offset (skip).all ()

  
    for post in allPosts :
        print (post)
    
    if len (allPosts) < skip:
        raise HTTPException (status_code = status.HTTP_204_NO_CONTENT
                             , detail = "there are not enough post you want")
    if len (allPosts) == 0:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,
                             detail = "not find the data ")
    return allPosts


@router.get ("/{id}", status_code = status.HTTP_200_OK, response_model = schemas.responsePostModel_VoteExtra)
def getPostAtID (id: int, database: Session = Depends (getDatabase), user = Depends (oauth2.get_current_user)):
    the_post = database.query (models.Post, func.count (models.Votes.post_id).label ("vote"))
    the_post = the_post.outerjoin (models.Votes, models.Post.id == models.Votes.post_id
                           ).group_by (models.Post.id).filter (models.Post.id == id).first ()

    if not the_post:
        raise HTTPException (status_code = status.HTTP_404_NOT_FOUND,
                             detail = "can not find the post with id {}".format(id))
    
    post: schemas.responsePostModel_VoteExtra = the_post
    
    if post.Post.owner.email != user.email:
        raise HTTPException (status_code = status.HTTP_403_FORBIDDEN
                             , detail = "the post is not yours")
    
    return post


@router.post ("/createPost", status_code = status.HTTP_201_CREATED, response_model = schemas.responsePostModel)
def createOnePost (post: schemas.createdPost ,database: Session = Depends (getDatabase), user = Depends (oauth2.get_current_user)):

    def checkPost (newPost: schemas.createdPost) -> bool:
        if newPost.title == "" or newPost.content == "":
            return False
        return True
    
    if not checkPost (post):
        raise HTTPException (status_code = status.HTTP_400_BAD_REQUEST,
                             detail = "the post is not created")
    # newPost = models.Post (title = post.title, content = post.content, published = post.published)
    newPost = models.Post (**post.dict ())
    newPost.owner_id = user.id
    database.add (newPost)
    database.commit ()
    database.refresh (newPost)
    return newPost



@router.delete ("/deletePost/{id}", status_code = status.HTTP_200_OK)
def deletePostAtID (id: int, database: Session = Depends (getDatabase), user_name = Depends (oauth2.get_current_user)):
    deletedPost = database.query (models.Post).filter (models.Post.id == id)
    if deletedPost.first () == None:
        raise HTTPException (status_code = status.HTTP_404_NOT_FOUND,
                             detail = "the post is not exist")
    if deletedPost.first().owner_id != user_name.id:
        raise HTTPException (status_code = status.HTTP_403_FORBIDDEN
                             , detail = "the post is not yours")
    deletedPost.delete (synchronize_session = False)
    database.commit ()
    return {"message": "the post with id {} is deleted".format (id)}


@router.put ("/update/{id}", status_code = status.HTTP_200_OK)
def updatePostAtID (id: int, post: schemas.updatedPost, database: Session = Depends (getDatabase), user_name =  Depends(oauth2.get_current_user)):
    allpost = database.query (models.Post).filter (models.Post.id == id)
    currentPost = allpost.first ()
    if currentPost == None:
        raise HTTPException (status_code = status.HTTP_404_NOT_FOUND,
                             detail = "the post is not available for updating")
    if currentPost.owner_id != user_name.id:
        raise HTTPException (status_code = status.HTTP_403_FORBIDDEN
                             , detail = "the post is not yours")
    allpost.update (post.dict (), synchronize_session = False)
    database.commit ()
    return {"message": "successful"}


# @router.get ("/common", status_code = status.HTTP_200_OK, response_model = schemas.responsePostModel)
# def getThePopularPost (database: Session = Depends (getDatabase)):
#     response_post = schemas.responsePostModel
    