import boto3
import os
import sys
import uuid
from PIL import Image
import PIL.Image
     
s3_client = boto3.client('s3')

class Size:
  def __init__(self, width, height):
    self.width = width
    self.height = height
     
def resize_image(image_path, resized_path, width, height):
    with Image.open(image_path) as image:
        image.thumbnail((width, height),PIL.Image.ANTIALIAS)
        image.save(resized_path)

def thumb(bktOri, bktDest, keyFile, size):
    
    dimension = getSize(size)

    localFile           = '/tmp/{}{}'.format(uuid.uuid4(), keyFile)
    localFileResized    = '/tmp/resized-{}'.format(keyFile)
    s3_client.download_file(bktOri, keyFile, localFile)
    resize_image(localFile, localFileResized, dimension.width, dimension.height)
    s3_client.upload_file(localFileResized, bktDest, keyFile.replace('_O_', '_'+size+'_'))
    


def getSize(size):
    return {
        'P': Size(72 ,54),
        'V': Size(172 ,130),
        'S': Size(260 ,195),
        'M': Size(485 ,363),
        'G': Size(640 ,480),
        'B': Size(800 ,600),
        'W': Size(1920 ,1080),
    }[size]

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        thumb(bucket, 'bucket-store-simdv1', key, 'P')
        thumb(bucket, 'bucket-store-simdv1', key, 'V')
        thumb(bucket, 'bucket-store-simdv1', key, 'S')
        thumb(bucket, 'bucket-store-simdv1', key, 'M')
        thumb(bucket, 'bucket-store-simdv1', key, 'G')
        thumb(bucket, 'bucket-store-simdv1', key, 'B')
        thumb(bucket, 'bucket-store-simdv1', key, 'W')

        s3_client.delete_object(Bucket=bucket, Key=key)

