import boto3
from botocore.exceptions import ClientError
from PIL import Image
import pandas as pd
import os


TARGET_IMAGE_SIZE = 832

destination_bucket = 'jron-lehtipiste'
destination_folder = 'sku110k-resized/{}/'.format(TARGET_IMAGE_SIZE)


input_path = '/tmp/input/'
output_path = '/tmp/output/'
os.mkdir(input_path)
os.mkdir(output_path)

s3_client = boto3.client('s3')


def resize(image_path, resized_path):

    with Image.open(image_path) as image:

        resized_image = image.resize((TARGET_IMAGE_SIZE, TARGET_IMAGE_SIZE), Image.ANTIALIAS)
        resized_image.save(resized_path)


def reannotate(file_name, input_path, output_path, TARGET_IMAGE_SIZE):

    columns = ['file_name', 'x1', 'y1', 'x2', 'y2', 'class', 'image_width', 'image_height']
    annotations = pd.read_csv(input_path + 'annotations.csv', names=columns)
    annotations = annotations[annotations['file_name'] == file_name]

    with open("random.csv") as csvfile:  
        data = csv.DictReader(csvfile)
        for row in data:
            print(row['A'])

    new_height = annotations['image_height'].values[0] / TARGET_IMAGE_SIZE
    new_width = annotations['image_width'].values[0] / TARGET_IMAGE_SIZE

    for i in range(len(annotations)):

        new_x1 = annotations['x1'].iloc[i] / new_width
        new_x2 = annotations['x2'].iloc[i] / new_width

        new_y1 = annotations['y1'].iloc[i] / new_height
        new_y2 = annotations['y2'].iloc[i] / new_height

        # object's width and height scaled to [0,1] relative to image size
        obj_width = round((new_x2 - new_x1) / TARGET_IMAGE_SIZE, 8)
        obj_height = round((new_y2 - new_y1) / TARGET_IMAGE_SIZE, 8)

        # object's center coordinates scaled to [0,1] relative to image size
        center_x = round(new_x1 / TARGET_IMAGE_SIZE + obj_width / 2, 8)
        center_y = round(new_y1 / TARGET_IMAGE_SIZE + obj_height / 2, 8)

        # create new record for object
        obj = '0 {} {} {} {}\n'.format(center_x, center_y, obj_width, obj_height)

        with open(output_path + 'annotations_' + os.path.splitext(file_name)[0] + '.txt', 'a') as f:
            f.write(obj)


def lambda_handler(event, context):

    for record in event['Records']:

        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        file_name = os.path.split(key)[1]

        try:
            s3_client.download_file(bucket, key, os.path.join(input_path, file_name))

            if file_name[:5] == 'train': 
                s3_client.download_file(bucket, 'annotations/annotations_train.csv', input_path + 'annotations.csv')
            elif file_name[:3] == 'val': 
                s3_client.download_file(bucket, 'annotations/annotations_val.csv', input_path + 'annotations.csv')
            elif file_name[:4] == 'test': 
                s3_client.download_file(bucket, 'annotations/annotations_test.csv', input_path + 'annotations.csv')
            else:
                print('Invalid file name:', file_name)

            obj = s3.get_object(Bucket='bucket', Key='key')
            df = pd.read_csv(obj['Body'])

            resize(input_path + file_name, output_path + 'resized-' + file_name)
            reannotate(file_name, input_path, output_path, TARGET_IMAGE_SIZE)

            s3_client.upload_file(
                output_path + 'resized-' + file_name, 
                destination_bucket, 
                destination_folder + 'images/' + 'resized-' + file_name
                )
            s3_client.upload_file(
                output_path + 'annotations_' + os.path.splitext(file_name)[0] + '.txt', 
                destination_bucket, 
                destination_folder + 'annotations/' + 'annotations_' + os.path.splitext(file_name)[0] + '.txt'
                )

        except ClientError as e:
            print(e)
 