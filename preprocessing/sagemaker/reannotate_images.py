import os
import csv


TARGET_IMAGE_SIZE = 832

input_path = '/opt/ml/processing/input/annotations/'
output_path = '/opt/ml/processing/output/{}/annotations/'.format(TARGET_IMAGE_SIZE)

if not os.path.exists(output_path):
    os.makedirs(output_path)


columns = ['file_name', 'x1', 'y1', 'x2', 'y2', 'class', 'image_width', 'image_height']

for group in ['train', 'val', 'test']:

    input_file = "annotations_" + group + ".csv"
    with open(os.path.join(input_path, input_file), 'r', newline='') as csvfile:

        data = csv.DictReader(csvfile, fieldnames=columns)

        for row in data:

            x_center = int(row['x1']) + int(row['x2']) / 2.0
            y_center = int(row['y1']) + int(row['y2']) / 2.0
            obj_width = int(row['x2']) - int(row['x1'])
            obj_height = int(row['y2']) - int(row['y1'])

            x = round(x_center / int(row['image_width']), 8)
            y = round(y_center / int(row['image_height']), 8)
            w = round(obj_width / int(row['image_width']), 8)
            h = round(obj_height / int(row['image_height']), 8)

            output_row = f'0 {x} {y} {w} {h}\n'

            image_name, _ = os.path.splitext(row['file_name'])
            output_file = image_name + '.txt'

            with open(os.path.join(output_path, output_file), 'a') as output_file:
                output_file.write(output_row)
