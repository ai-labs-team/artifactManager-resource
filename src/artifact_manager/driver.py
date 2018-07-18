import boto3
import botocore
import json

class s3():

    client = {}

    def __init__(self, access_key, secret_access_key, region_name):
        """
            Login to s3 and store the login object
            
            Keyword arguments:
            access_key -- the aws access key
            secret_access_key -- the aws secret key
            region_name -- region name
        """
        self.client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_access_key,
            region_name=region_name,
        )

    def s3_download(self, bucket_name, key, options):
        """
            download a text file from s3 and return the contents
            
            Keyword arguments:
            bucket_name -- the name of the bucket
            key -- the key, path, to the file on s3
        """
        encoding = 'utf-8'
        if 'encoding' in options:
            encoding = options['encoding']

        text = ""
        try:
            obj = self.client.get_object(Bucket=bucket_name, Key=key)
            text = obj['Body'].read().decode(encoding)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise
        return text

    def s3_upload(self, bucket_name, file, key):
        """
            Upload a file to s3

            Keyword arguments:
            bucket_name -- the name of the bucket
            file -- the file content to be uploaded
            key -- the upload target
        """
        content_type = ''
        if 'html' in key:
            content_type = 'text/html'
        elif 'js' in key:
            content_type = 'application/javascript'
        elif 'png' in key:
            content_type = 'image/png'
        elif 'jpeg' in key:
            content_type = 'image/jpeg'

        if len(content_type) > 0:
            self.client.put_object(Key=key, Body=file, Bucket=bucket_name, ContentType=content_type)
        else:
            self.client.put_object(Key=key, Body=file, Bucket=bucket_name)
