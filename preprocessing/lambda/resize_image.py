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


def reannotate(image_name, input_path, output_path, TARGET_IMAGE_SIZE):

    columns = ['image_name','x1','y1','x2','y2','class','image_width','image_height']
    annotations = pd.read_csv(input_path + 'annotations.csv', names=columns)
    annotations = annotations[annotations['image_name'] == image_name]

    new_height = annotations['image_height'].values[0] / TARGET_IMAGE_SIZE
    new_width = annotations['image_width'].values[0] / TARGET_IMAGE_SIZE

    for i in range(len(annotations)):

        new_x1 = annotations.x1[i] / new_width
        new_x2 = annotations.x2[i] / new_width

        new_y1 = annotations.y1[i] / new_height
        new_y2 = annotations.y2[i] / new_height

        # object's width and height scaled to [0,1] relative to image size
        obj_width = round((new_x2 - new_x1) / TARGET_IMAGE_SIZE, 8)
        obj_height = round((new_y2 - new_y1) / TARGET_IMAGE_SIZE, 8)

        # object's center coordinates scaled to [0,1] relative to image size
        center_x = round(new_x1 / TARGET_IMAGE_SIZE + obj_width / 2, 8)
        center_y = round(new_y1 / TARGET_IMAGE_SIZE + obj_height / 2, 8)

        # create new record for object
        obj = '0 {} {} {} {}\n'.format(center_x, center_y, obj_width, obj_height)

        with open(output_path + 'annotations_' + image_name[:-4] + '.txt', 'a') as f:
            f.write(obj)


def lambda_handler(event, context):

    for record in event['Records']:

        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        image_name = key.split('/')[-1]

        try:
            s3_client.download_file(bucket, key, input_path + image_name)

            if image_name[:5] == 'train': 
                s3_client.download_file(bucket, 'annotations/annotations_train.csv', input_path + 'annotations.csv')
            elif image_name[:3] == 'val': 
                s3_client.download_file(bucket, 'annotations/annotations_val.csv', input_path + 'annotations.csv')
            elif image_name[:4] == 'test': 
                s3_client.download_file(bucket, 'annotations/annotations_test.csv', input_path + 'annotations.csv')
            else:
                print('Invalid image name:', image_name)

            resize(input_path + image_name, output_path + 'resized-' + image_name)
            reannotate(image_name, input_path, output_path, TARGET_IMAGE_SIZE)

            s3_client.upload_file(
                output_path + 'resized-' + image_name, 
                destination_bucket, 
                destination_folder + 'images/' + 'resized-' + image_name
                )
            s3_client.upload_file(
                output_path + 'annotations_' + image_name[:-4] + '.txt', 
                destination_bucket, 
                destination_folder + 'annotations/' + + 'annotations_' + image_name[:-4] + '.txt'
                )

        except ClientError as e:
            print(e)
 