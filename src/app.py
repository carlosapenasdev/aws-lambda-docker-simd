import boto3
import os
import sys
import uuid
from PIL import Image
import PIL.Image
     
s3_client = boto3.client('s3')
     
def resize_image(image_path, resized_path, width, height):
    with Image.open(image_path) as image:
        image.thumbnail((width, height),PIL.Image.ANTIALIAS)
        image.save(resized_path)

def thumb(bktOri, bktDest, keyFile, width, height):
    localFile           = '/tmp/{}{}'.format(uuid.uuid4(), keyFile)
    localFileResized    = '/tmp/resized-{}'.format(keyFile)
    s3_client.download_file(bktOri, keyFile, localFile)
    resize_image(localFile, localFileResized, width, height)
    s3_client.upload_file(localFileResized, bktDest, "thumb-"+keyFile)
    s3_client.delete_object(Bucket=bktOri, Key=keyFile)

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key'] 
        
        thumb(bucket, 'bucket-store-simdv1', key, 128, 128)

