from sqlalchemy import CheckConstraint, Column, Integer, String, Boolean, TIMESTAMP, Table, text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

user_follows = Table(
    "user_follows",
    Base.metadata,
    Column("follower_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, index=True),
    Column("following_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, index=True),
    Column("created_at", TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()")),
    CheckConstraint("follower_id <> following_id", name="ck_user_follows_no_self_follow"),
)


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', default=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
    owner_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)  
    owner=relationship("User")


class User(Base):  
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
    followers = relationship(
        "User",
        secondary=user_follows,
        primaryjoin=id == user_follows.c.following_id,
        secondaryjoin=id == user_follows.c.follower_id,
        back_populates="following",
    )
    following = relationship(
        "User",
        secondary=user_follows,
        primaryjoin=id == user_follows.c.follower_id,
        secondaryjoin=id == user_follows.c.following_id,
        back_populates="followers",
    )


class Vote(Base):                    
    __tablename__ = "votes"          

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
