import boto3, botocore
from decouple import config
from werkzeug.utils import secure_filename

s3 = boto3.client(
    "s3",
    aws_access_key_id=config('AWS_ACCESS_KEY'),
    aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY')
)


def upload_file_to_s3(file, acl="public-read"):
    filename = secure_filename(file.filename)
    try:
        s3.upload_fileobj(
            file,
            config('AWS_BUCKET_NAME'),
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        print("Error: ", e)
        return e
    
    return file.filename