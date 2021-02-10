import boto3
from botocore.exceptions import ClientError
from PIL import Image


TARGET_IMAGE_SIZE = 832

destination_bucket = 'jron-lehtipiste'
destination_folder = 'sku110k-resized/{}/'.format(TARGET_IMAGE_SIZE)


input_path = '/tmp/'
output_path = '/tmp/'

s3_client = boto3.client('s3')


def resize(image_path, resized_path):
    with Image.open(image_path) as image:
        resized_image = image.resize((TARGET_IMAGE_SIZE, TARGET_IMAGE_SIZE), Image.ANTIALIAS)
        resized_image.save(resized_path)


def lambda_handler(event, context):

    for record in event['Records']:

        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        image_name = key.split('/')[-1]

        try:
            s3_client.download_file(bucket, key, input_path + image_name)

            resize(input_path + image_name, output_path + 'resized-' + image_name)

            s3_client.upload_file(output_path + 'resized-' + image_name, destination_bucket, destination_folder + 'resized-' + image_name )

        except ClientError as e:
            print(e)
