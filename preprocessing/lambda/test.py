import boto3
from botocore.exceptions import ClientError
from PIL import Image


TARGET_IMAGE_SIZE = 832

destination_bucket = 'jron-lehtipiste'
destination_folder = 'sku110k-resized/{}/'.format(TARGET_IMAGE_SIZE)


input_path = './input/'
output_path = './output/'

session = boto3.Session(profile_name='solita-sandbox')
s3_client = session.client('s3')

def resize(image_path, resized_path):
    with Image.open(image_path) as image:
        resized_image = image.resize((TARGET_IMAGE_SIZE, TARGET_IMAGE_SIZE), Image.ANTIALIAS)
        resized_image.save(resized_path)

event = {
  "Records": [
    {
      "eventVersion": "2.0",
      "eventSource": "aws:s3",
      "awsRegion": "eu-west-1",
      "eventTime": "1970-01-01T00:00:00.000Z",
      "eventName": "ObjectCreated:Put",
      "userIdentity": {
        "principalId": "EXAMPLE"
      },
      "requestParameters": {
        "sourceIPAddress": "127.0.0.1"
      },
      "responseElements": {
        "x-amz-request-id": "EXAMPLE123456789",
        "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH"
      },
      "s3": {
        "s3SchemaVersion": "1.0",
        "configurationId": "testConfigRule",
        "bucket": {
          "name": "jron-sku110k",
          "ownerIdentity": {
            "principalId": "EXAMPLE"
          },
          "arn": "arn:aws:s3:::jron-sku110k"
        },
        "object": {
          "key": "images/test_1048.jpg",
          "size": 1024,
          "eTag": "0123456789abcdef0123456789abcdef",
          "sequencer": "0A1B2C3D4E5F678901"
        }
      }
    }
  ]
}

for record in event['Records']:

    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']
    image_name = key.split('/')[-1]

    print()
    print(bucket)
    print(key)
    print(image_name)
    print(input_path + image_name)
    print()

    # with open(input_path + image_name, 'wb') as f:
    #     s3_client.download_file(bucket, key, input_path + image_name)

    try:
        response = s3_client.download_file(bucket, key, input_path + image_name)
    except ClientError as e:
        print(e)

    resize(input_path + image_name, output_path + 'resized-' + image_name)
    
    try:
        response = s3_client.upload_file(output_path + 'resized-' + image_name, destination_bucket, destination_folder + image_name )
    except ClientError as e:
        print(e)

