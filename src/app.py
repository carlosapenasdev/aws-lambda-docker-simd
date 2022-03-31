import boto3
import os
import sys
import uuid
from PIL import Image
import PIL.Image
import re

regex = r"(_\w_)"

s3_client = boto3.client('s3')

class Size:
  def __init__(self, width, height):
    self.width = width
    self.height = height
    
def localImg(bktOri, keyFile):
    localFile           = '/tmp/{}'.format(keyFile)
    s3_client.download_file(bktOri, keyFile, localFile)
    return localFile

def thumbLocal(localFile, keyFile, size):
    dimension = getSize(size)
    local_resized = resize_local(localFile, size, dimension.width, dimension.height)
    s3_client.upload_file(local_resized, 'bucket-store-simdv1', re.sub(regex, '_'+size+'_', keyFile, 0, re.MULTILINE))
    return local_resized

def getSize(size):
    return {
        'W': Size(1920 ,1080),
        'B': Size(800 ,600),
        'G': Size(640 ,480),
        'M': Size(485 ,363),
        'S': Size(260 ,195),
        'V': Size(172 ,130),
        'P': Size(72 ,54),
    }[size]

def resize_local(localFile, size, width, height):
    local_resized = localFile.replace('_O_', '_'+size+'_')
    with Image.open(localFile) as image:
         image.thumbnail((width, height),PIL.Image.ANTIALIAS)
         image.save(local_resized)
    return local_resized

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        localFile = localImg(bucket, key)
        
        s3_client.upload_file(localFile, 'bucket-store-simdv1', key)
        s3_client.delete_object(Bucket=bucket, Key=key)

        localFile = thumbLocal(localFile, key, 'W')
        localFile = thumbLocal(localFile, key, 'B')
        localFile = thumbLocal(localFile, key, 'G')
        localFile = thumbLocal(localFile, key, 'M')
        localFile = thumbLocal(localFile, key, 'S')
        localFile = thumbLocal(localFile, key, 'V')
        localFile = thumbLocal(localFile, key, 'P')