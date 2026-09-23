"""
s3_util.py
-----------
Handles all AWS S3 interactions for the Face ID Medical System.
Face images are the "source of truth" in S3; the local
data/registered_faces folder is just a temporary cache that
DeepFace needs (it can only compare against local files).

SETUP BEFORE USING THIS FILE:
1. Create an S3 bucket in the AWS Console.
2. Create an IAM user with ONLY s3:PutObject, s3:GetObject,
   s3:ListBucket permissions on that bucket (least privilege).
3. Generate an Access Key ID + Secret Access Key for that user.
4. Set them as environment variables (never hardcode them):
     Windows (PowerShell):
       setx AWS_ACCESS_KEY_ID "your-access-key"
       setx AWS_SECRET_ACCESS_KEY "your-secret-key"
     Mac/Linux:
       export AWS_ACCESS_KEY_ID="your-access-key"
       export AWS_SECRET_ACCESS_KEY="your-secret-key"
5. pip install boto3
6. Update BUCKET_NAME and REGION below to match your bucket.
"""

import os
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# ---- Configuration: update these two values ----
BUCKET_NAME = "faceid-medical-yourname"   # <-- change to your actual bucket name
REGION = "ap-south-1"                     # <-- change to your bucket's region

_s3_client = None


def get_s3_client():
    """Create (once) and return the boto3 S3 client.
    Credentials are picked up automatically from environment variables."""
    global _s3_client
    if _s3_client is None:
        _s3_client = boto3.client("s3", region_name=REGION)
    return _s3_client


def is_s3_configured():
    """Quick check so the app can fall back to local-only mode
    if AWS isn't set up (useful for offline demo safety)."""
    return bool(os.environ.get("AWS_ACCESS_KEY_ID") and os.environ.get("AWS_SECRET_ACCESS_KEY"))


def upload_face_to_s3(local_path, s3_key):
    """Upload a local face image to S3. Returns the s3_key on success,
    or None if the upload failed (caller should fall back to local path)."""
    try:
        client = get_s3_client()
        client.upload_file(local_path, BUCKET_NAME, s3_key)
        print(f"[S3] Uploaded {local_path} -> s3://{BUCKET_NAME}/{s3_key}")
        return s3_key
    except (ClientError, NoCredentialsError) as e:
        print(f"[S3] Upload failed, continuing with local file only: {e}")
        return None


def download_face_from_s3(s3_key, local_path):
    """Download a single face image from S3 to a local path."""
    client = get_s3_client()
    client.download_file(BUCKET_NAME, s3_key, local_path)
    return local_path


def download_all_faces(local_dir):
    """Download every registered face from S3 into a local folder
    so DeepFace has fresh local copies to compare against.
    If S3 isn't reachable, silently skip (local cache is used instead)."""
    os.makedirs(local_dir, exist_ok=True)
    try:
        client = get_s3_client()
        paginator = client.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=BUCKET_NAME, Prefix="registered_faces/"):
            for obj in page.get("Contents", []):
                s3_key = obj["Key"]
                filename = os.path.basename(s3_key)
                if filename:  # skip the "folder" placeholder key itself
                    local_path = os.path.join(local_dir, filename)
                    client.download_file(BUCKET_NAME, s3_key, local_path)
        print("[S3] Synced registered faces from S3.")
    except (ClientError, NoCredentialsError) as e:
        print(f"[S3] Could not sync from S3, using local cache instead: {e}")
