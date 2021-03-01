import boto3
from botocore.exceptions import ClientError
import os
import csv


TARGET_IMAGE_SIZE = 832

destination_bucket = 'jron-lehtipiste'
destination_folder = 'sku110k-resized/{}/annotations/'.format(TARGET_IMAGE_SIZE)


input_path = '/tmp/input/'
output_path = '/tmp/output/'

if not os.path.exists(input_path):
    os.mkdir(input_path)
if not os.path.exists(output_path):
    os.mkdir(output_path)


s3_client = boto3.client('s3')


def resize(image_path, resized_path):

    with Image.open(image_path) as image:

        resized_image = image.resize((TARGET_IMAGE_SIZE, TARGET_IMAGE_SIZE), Image.ANTIALIAS)
        resized_image.save(resized_path)


def lambda_handler(event, context):

    for record in event['Records']:

        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        file_name = os.path.split(key)[1]
        file_input_path = os.path.join(input_path, file_name)
        file_output_path = os.path.join(output_path, 'resized-' + file_name)

        try:
            s3_client.download_file(bucket, key, file_input_path)

            with open("random.csv") as csvfile:  
                data = csv.DictReader(csvfile)
                for row in data:
                    print(row['A'])

            s3_client.upload_file(
                file_output_path, 
                destination_bucket, 
                os.path.join(destination_folder, 'resized-' + file_name)
                )

        except ClientError as e:
            print(e)
 