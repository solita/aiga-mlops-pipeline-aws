import os


TARGET_IMAGE_SIZE = 832

input_path = '/opt/ml/processing/input/'
output_path = '/opt/ml/processing/output/resized_images/{}/annotations/'.format(TARGET_IMAGE_SIZE)

if not os.path.exists(output_path):
    os.makedirs(output_path)


columns = ['file_name', 'x1', 'y1', 'x2', 'y2', 'class', 'image_width', 'image_height']

for group in ['train', 'val', 'test']:

    with open("annotations_" + group + ".csv", 'r') as csvfile:

        data = csv.DictReader(csvfile, field_names=columns, newline='')

        for row in data:

            x_center = int(row['x1']) + int(row['x2']) / 2.0
            y_center = int(row['y1']) + int(row['y2']) / 2.0
            obj_width = int(row['x2']) - int(row['x1'])
            obj_height = int(row['y2']) - int(row['y1'])

            x = x_center / int(row['image_width'])
            y = y_center / int(row['image_height'])
            w = obj_width / int(row['image_width'])
            h = obj_height / int(row['image_height'])

            output_row = f'0 {round(x, 8)} {round(y, 8)} {round(w, 8)} {round(h, 8)}\n'

            image_name, _ = os.path.splitext(row['file_name'])

            with open(image_name + '.txt', 'a') as output_file:
                output_file.write(output_row)
