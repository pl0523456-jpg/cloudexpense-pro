import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///cloudexpense.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # AWS / S3 configuration
    AWS_REGION = os.getenv("AWS_REGION", "ap-southeast-1")
    AWS_S3_BUCKET = os.getenv(
        "AWS_S3_BUCKET",
        "cloudexpense-pro-receipts-925127010057"
    )
    AWS_PROFILE = os.getenv("AWS_PROFILE", "cloudexpense")
