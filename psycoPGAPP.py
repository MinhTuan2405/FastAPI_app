from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import psycopg
import time

app = FastAPI ()


databaseConfig = {
    'dbname': 'fastapi',
    'user': 'postgres',
    'password': 'minhtuan2405',
    'host': 'localhost',
    'port': 5432
}

try:
    with psycopg.connect(**databaseConfig) as conn:
        with conn.cursor() as cursor:
            print ("connect successfulll, congratulation duma tao connect duoc db rooiiiiiii")
            cursor.execute("SELECT * FROM product")
            result = cursor.fetchall()
            myData = result
            for row in myData:
                print(row)
except psycopg.OperationalError as op_error:
    print("Operational error: Could not connect to the database")
    print(op_error)
    time.sleep(2)
except Exception as error:
    print("An error occurred")
    print(error)
    time.sleep(2)

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int]

@app.get ("/login/user")
def root ():
    a = 100
    b = 10
    m = a + b
    return {m: "Phan Thi Hong Nhung"}

@app.get("/posts")
def get_post ():
    return {"data": "this is a post"}

@app.post ("/mediaPost")
def push_post ():
    title = "this is a title"
    content = "Hong Nhung"
    return "the media post has been posted" if content == "Hong Nhung" else "the post is not created"


@app.post ("/publicPost")
def pushPost (thePost: Post):
    successAnnouncement = "creating the post successfully, the post has been published"
    failAnnouncement = "creating the post successfully, the post is not published"
    print ("properties of the post: ")
    print (thePost)
    if thePost.published == True:
        return (successAnnouncement + '\n', thePost)
    else:
        return (failAnnouncement + '\n', thePost)



fake_items_db = [
    {
        "item_name": "Foo",
        "author": "david"
    }, 
    {   
        "item_name": "Bar",
        "author": "john"
    },
    {   
        "item_name": "Baz",
        "author": "linda"
    }
]

class itemInfor (BaseModel):
    name: str
    author: str


@app.get("/items")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

@app.get ('/item/{id}')
def get_item (id: int):
    if id < 0 or id >= len (fake_items_db):
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,
                             detail= "not find the material")
    return {"data": fake_items_db[id]}

@app.post ("/insertItem", status_code= status.HTTP_201_CREATED )
def insertItemIntoFakedb (item: itemInfor):
    print (item)
    print (item.model_dump())
    fake_items_db.append (item.model_dump ())
    # Response.status.HTTP_201_CREATED
    return {"insert successfull": fake_items_db}


@app.delete ("/item/{id}", status_code = status.HTTP_204_NO_CONTENT)
def removeItem (id: int):
    if id < 0 or id >= len (fake_items_db) or type (id) is str:
        raise HTTPException (status_code=status.HTTP_400_BAD_REQUEST,
                             detail= "can not complete the request")
    else:
        fake_items_db.remove (fake_items_db[id])
    return {"complete, current data": fake_items_db}



@app.put ("/item/{id}", status_code = status.HTTP_205_RESET_CONTENT)
def updateItem (id: int, newInfor: itemInfor):
    if id < 0 or id >= len (fake_items_db) or type (id) is str:
        raise HTTPException (status_code=status.HTTP_400_BAD_REQUEST,
                             detail= "can not complete the request")
    else:
        fake_items_db[id] = newInfor.model_dump ()
        
    return {"message: update completed": fake_items_db}

