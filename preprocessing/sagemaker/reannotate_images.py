import boto3
from botocore.exceptions import ClientError
from PIL import Image
import pandas as pd
import os


TARGET_IMAGE_SIZE = 832

input_path = '/opt/ml/processing/input/'
output_path = '/opt/ml/processing/output/resized_images/{}/annotations/'.format(TARGET_IMAGE_SIZE)



columns = ['file_name', 'x1', 'y1', 'x2', 'y2', 'class', 'image_width', 'image_height']
annotations = pd.read_csv(input_path + 'annotations.csv', names=columns)
annotations = annotations[annotations['file_name'] == file_name]


for group in ['train', 'val', 'test']:
    with open("annotations_" + group + ".csv") as csvfile:

        data = csv.DictReader(csvfile)
        for row in data:

            row['image_height'] = row['image_height'] / TARGET_IMAGE_SIZE
            row['image_width'] = row['image_width'] / TARGET_IMAGE_SIZE

            row['x1'] = row['x1'] / row['image_width']
            row['x2'] = row['x2'] / row['image_width']
            row['y1'] = row['y1'] / row['image_height']
            row['y2'] = row['y2'] / row['image_height']



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




 