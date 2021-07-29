import os
import platform
from faker import Factory
import csv
import boto3
from botocore.exceptions import ClientError

print("Loading function")
print(f"Python {platform.python_version()}")

BUCKET = os.getenv("BUCKET_NAME")
KEY = os.getenv("KEY_NAME")
s3 = boto3.resource("s3")


def sample_csv(temp_file_path):
    try:
        with open(temp_file_path, "w") as f:
            writer = csv.writer(f)

            fake_us = Factory.create()
            fake_jp = Factory.create()

            for i in range(100):
                row = [
                    fake_us.date_time(),
                    fake_us.uuid4(),
                    fake_jp.name(),
                    fake_jp.email(),
                    fake_jp.phone_number(),
                    fake_jp.address(),
                    fake_us.word(),
                    fake_jp.company(),
                ]
                writer.writerow(row)
        return
    except IOError as e:
        print(e)
        raise FileWriteError("ファイル作成できず・・・")


def s3_upload(temp_file_path, bucket, key):

    s3_object = s3.Object(bucket, key)
    s3_object.put(Body=open(temp_file_path, "rb"))


def lambda_handler(event, context):
    try:
        temp_file_path = "/tmp/sample.csv"
        sample_csv(temp_file_path)
        s3_upload(temp_file_path, BUCKET, KEY)
        return {"bucket": BUCKET, "key": KEY}
    except FileWriteError:
        return {"bucket": None, "key": None}
    except ClientError as e:
        code = e.response["Error"]["Code"]
        if code == "NoSuchBucket":
            return {"bucket": None, "key": None}
    except Exception as e:
        print(e)


class FileWriteError(IOError):
    """file create error"""

    pass
