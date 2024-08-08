from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base

class Post (Base):
    __tablename__ = "posts"

    id = Column (Integer, primary_key= True, nullable = False)
    title = Column (String, nullable = False)
    content = Column (String, nullable = False)
    published = Column (Boolean, server_default = "TRUE", nullable= False)
    created_at = Column (TIMESTAMP(timezone=True), server_default=text("now()"), nullable = False)
    owner_id = Column (Integer, ForeignKey ("users.id", ondelete = "CASCADE"), nullable= False)

    owner = relationship ("User")

class User (Base):
    __tablename__ = "users"

    id = Column (Integer, primary_key = True, nullable = False)
    email = Column (String, unique = True, nullable = False)
    password = Column (String, nullable = False)
    created_at = Column (TIMESTAMP(timezone=True), server_default=text("now()"), nullable = False)
    is_loggin = Column (Boolean, server_default = "FALSE", nullable = False)

class TokenJWT (Base):
    __tablename__ = "expired_token"

    # owner_id = Column (Integer, ForeignKey ("users.id", ondelete = "CASCADE"), nullable = False, primary_key = True)
    expired_token = Column (String, nullable = False, primary_key = True)

class Votes (Base):
    __tablename__ = "votes"

    user_id = Column (Integer, ForeignKey ("users.id", ondelete = "CASCADE"), primary_key = True, nullable = False)
    post_id = Column (Integer, ForeignKey ("posts.id", ondelete = "CASCADE"), primary_key = True, nullable = False)
    