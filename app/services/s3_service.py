import boto3
from flask import current_app


def get_s3_client():
    """
    Create and return an S3 client using the configured AWS profile.
    """

    session = boto3.Session(
        profile_name=current_app.config["AWS_PROFILE"],
        region_name=current_app.config["AWS_REGION"]
    )

    return session.client("s3")


def upload_receipt(file_object, object_key, content_type=None):
    """
    Upload a receipt file to the configured S3 bucket.
    """

    s3 = get_s3_client()

    extra_args = {}

    if content_type:
        extra_args["ContentType"] = content_type

    s3.upload_fileobj(
        file_object,
        current_app.config["AWS_S3_BUCKET"],
        object_key,
        ExtraArgs=extra_args
    )

    return object_key


def delete_receipt(object_key):
    """
    Delete a receipt object from the configured S3 bucket.
    """

    s3 = get_s3_client()

    s3.delete_object(
        Bucket=current_app.config["AWS_S3_BUCKET"],
        Key=object_key
    )

def download_receipt(object_key):
    """
    Download a receipt object from the configured S3 bucket.
    """

    s3 = get_s3_client()

    response = s3.get_object(
        Bucket=current_app.config["AWS_S3_BUCKET"],
        Key=object_key
    )

    return response
