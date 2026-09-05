from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field, conint
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    community_id: Optional[int] = None
    image_url: Optional[AnyHttpUrl] = None
    video_url: Optional[AnyHttpUrl] = None

class PostCreate(PostBase):
    pass


class UserOut(BaseModel):  
    id: int
    email: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class FollowStatus(BaseModel):
    following: bool
    follower_count: int
    following_count: int


class CommunityCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=500)


class CommunityOut(BaseModel):
    id: int
    name: str
    slug: str
    description: str
    creator_id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class MessageCreate(BaseModel):
    content: str = Field(min_length=1, max_length=2000)


class MessageOut(BaseModel):
    id: int
    conversation_id: int
    sender_id: int
    content: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ConversationCreate(BaseModel):
    user_id: int


class ConversationOut(BaseModel):
    id: int
    user_one_id: int
    user_two_id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class NotificationOut(BaseModel):
    id: int
    recipient_id: int
    actor_id: Optional[int]
    type: str
    entity_type: str
    entity_id: Optional[int]
    payload: str
    is_read: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ReplyCreate(BaseModel):
    content: str = Field(min_length=1, max_length=2000)
    parent_id: Optional[int] = None


class ReplyOut(BaseModel):
    id: int
    post_id: int
    parent_id: Optional[int]
    owner_id: int
    content: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
    

class Post(PostBase):
    id: int          
    created_at: datetime
    owner_id:int
    owner:UserOut

    model_config = ConfigDict(from_attributes=True)

class PostOut(BaseModel):
    Post: Post
    votes: int

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):    
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):  
    post_id: int
    dir: conint(ge=0, le=1)   # type: ignore


