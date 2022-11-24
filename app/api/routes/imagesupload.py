from fastapi import Depends, status, HTTPException, APIRouter, UploadFile, File
from sqlalchemy.orm import Session
from app.api.database import get_db
from app.api import model, schema, utils, oauth2, config
from .. utils import random_with_N_digits

router = APIRouter(
    prefix="/images",
    tags=['ImageUpload']
)

import os
import boto3
import logging

from botocore.client import BaseClient
from botocore.exceptions import ClientError
from starlette.responses import JSONResponse


AWS_ACCESS_KEY_ID = config.settings.aws_access_key_id
AWS_SECRET_KEY = config.settings.aws_secret_key
AWS_S3_BUCKET_NAME = config.settings.aws_s3_bucket_name
REGION_NAME='ap-south-1'

image_url_substring = f"https://{AWS_S3_BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/"


def s3() -> BaseClient:
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name='ap-south-1')
    return s3_client


def upload_file_to_bucket(s3_client, file_obj, bucket, folder, object_name=None):
    if object_name is None:
        object_name = file_obj

    # Upload the file
    try:
        # with open("files", "rb") as f:
        s3_client.upload_fileobj(file_obj, bucket, f"{folder}/{object_name}")
    except ClientError as e:
        logging.error(e)
        return False
    return True




@router.post("/random-image", status_code=201)
async def post_upload_profile_image(file_obj: UploadFile = File(...),db:Session= Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    ran = str(random_with_N_digits(6))
    upload_obj = upload_file_to_bucket(s3_client=s3(),
                                       file_obj=file_obj.file,
                                       bucket=AWS_S3_BUCKET_NAME,
                                       folder=f"images/{ran}",  # To Be updated
                                       object_name=file_obj.filename)
    if upload_obj:
        download_url = image_url_substring+f"images/{ran}/" +str(file_obj.filename)
        download_url = download_url.split()
        download_url = "+".join(download_url)
        return {"image_url": download_url}
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="File could not be uploaded")

@router.post("/profile", status_code=201)
async def post_upload_profile_image(file_obj: UploadFile = File(...),
    db:Session= Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    upload_obj = upload_file_to_bucket(s3_client=s3(),
                                       file_obj=file_obj.file,
                                       bucket=AWS_S3_BUCKET_NAME,
                                       folder=f"{current_user.id}/profile_image",  # To Be updated
                                       object_name=file_obj.filename)
    if upload_obj:
        download_url = image_url_substring+f"{current_user.id}/profile_image/" +str(file_obj.filename)
        download_url = download_url.split()
        download_url = "+".join(download_url)

        data_query = db.query(model.UserProfile).filter(model.UserProfile.user_id==current_user.id)
        if data_query.first():
            data_query.update({"image_url": download_url},synchronize_session=False)
            db.commit()
        return JSONResponse(content="Object has been uploaded to bucket successfully",
                            status_code=status.HTTP_201_CREATED)
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="File could not be uploaded")



@router.post("", status_code=201)
async def post_images(file_obj: UploadFile = File(...),db:Session= Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    upload_obj = upload_file_to_bucket(s3_client=s3(),
                                       file_obj=file_obj.file,
                                       bucket=AWS_S3_BUCKET_NAME,
                                       folder=f"{current_user.id}/images",  # To Be updated
                                       object_name=file_obj.filename)
    if upload_obj:
        download_url = image_url_substring+f"{current_user.id}/images/" +str(file_obj.filename)
        download_url = download_url.split()
        download_url = "+".join(download_url)
        data = model.Post(user_id=current_user.id, content=download_url)
        db.add(data)
        db.commit()
        return JSONResponse(content="Object has been uploaded to bucket successfully",
                            status_code=status.HTTP_201_CREATED)
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="File could not be uploaded")


@router.put("/{image_id}", status_code=201)
async def post_upload_profile_image(image_id:int, file_obj: UploadFile = File(...),db:Session= Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    upload_obj = upload_file_to_bucket(s3_client=s3(),
                                       file_obj=file_obj.file,
                                       bucket=AWS_S3_BUCKET_NAME,
                                       folder=f"{current_user.id}/images",  # To Be updated
                                       object_name=file_obj.filename)
    if upload_obj:
        download_url = image_url_substring+f"{current_user.id}/images/" +str(file_obj.filename)
        download_url = download_url.split()
        download_url = "+".join(download_url)
        data_query = db.query(model.Post).filter(model.Post.id==image_id)
        try:
            data_query.update({"image_url": download_url},synchronize_session=False)
        except:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Image could not be updated")
        db.commit()
        return JSONResponse(content="Image has been updated to bucket successfully",
                            status_code=status.HTTP_201_CREATED)
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Image could not be uploaded")

@router.get("/uploaded")
def uploaded_images(db:Session= Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    data = db.query(model.Post).filter(model.Post.user_id==current_user.id,
        model.Post.is_deleted==False).all()
    return data


# @router.delete("/image/{image_id}")
# def delete_image(image_id:int,db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#     data_query = db.query(model.Image).filter(
#         model.Image.id == image_id,
#         model.Image.user_id == current_user.id
#         )
#     if data_query.first():
#         data_query.update({"is_deleted": True}, synchronize_session=False)
#         db.commit()
#         return {"message":"Success"}
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#         detail="image not found")


