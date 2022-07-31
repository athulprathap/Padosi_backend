from api.utils.dbUtil import database
from api.posts import schemas as posts_schemas
from api.auth import schemas as auth_schemas
from typing import Optional


# create a function to store the post deatils in the database with owner_id as parameter

def create_post(
    request: posts_schemas.PostCreate,
    currentUser: auth_schemas.UserList
    ):

    # create a new post in the database
    query = "INSERT INTO post VALUES (nextval('post_id_seq'), title:, content:, owner_id:, created_at:, published:, now() at time zone 'UTC', now() at time zone 'UTC', '1'))"
    database.execute(query, values = {'title': request.title, 'content': request.content, 'owner_id': currentUser.id, 'published': request.published })
    