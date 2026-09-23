# Faceid_medical
# Face ID Medical System — Setup Guide

## Install dependencies
```
pip install opencv-python deepface reportlab cryptography boto3
```

## AWS setup (for the S3 cloud storage feature)
1. Create an S3 bucket in the AWS Console (e.g. `faceid-medical-yourname`).
2. Create an IAM user with only these permissions on that bucket:
   `s3:PutObject`, `s3:GetObject`, `s3:ListBucket`
3. Generate an Access Key ID + Secret Access Key for that user.
4. Set them as environment variables (never hardcode keys in code):
   - Windows (PowerShell): `setx AWS_ACCESS_KEY_ID "..."` and `setx AWS_SECRET_ACCESS_KEY "..."`
   - Mac/Linux: `export AWS_ACCESS_KEY_ID="..."` and `export AWS_SECRET_ACCESS_KEY="..."`
5. Open `s3_util.py` and set `BUCKET_NAME` and `REGION` to match your bucket.


## Run it
```
python main.py
```

e
   (free-tier resources can expire).
