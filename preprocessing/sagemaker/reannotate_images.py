import boto3
from botocore.exceptions import ClientError
from PIL import Image
import pandas as pd
import os


TARGET_IMAGE_SIZE = 832

input_path = '/opt/ml/processing/input/'
output_path = '/opt/ml/processing/output/resized_images/{}/annotations/'.format(TARGET_IMAGE_SIZE)


columns = ['file_name', 'x1', 'y1', 'x2', 'y2', 'class', 'image_width', 'image_height']

for group in ['train', 'val', 'test']:

    with open("annotations_" + group + ".csv", 'r') as csvfile:

        data = csv.DictReader(csvfile, field_names=columns)

        for row in data:

            x_center = row['x1'] + row['x2'] / 2.0
            y_center = row['y1'] + row['y2'] / 2.0
            obj_width = row['x2'] - row['x1']
            obj_height = row['y2'] - row['y1']

            x = x_center / row['image_width']
            y = y_center / row['image_height']
            w = obj_width / row['image_width']
            h = obj_height / row['image_height']

            output_row = f'0 {round(x, 8)} {round(y, 8)} {round(w, 8)} {round(h, 8)}\n'

            image_name, _ = os.path.splitext(row['file_name'])

            with open(image_name + '.txt', 'a') as output_file:
                output_file.write(output_row)
