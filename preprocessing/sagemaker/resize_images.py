import os
from PIL import Image


TARGET_IMAGE_SIZE = 832

input_path = '/opt/ml/processing/input/images/'
output_path = '/opt/ml/processing/output/resized_images/{}/images/'.format(TARGET_IMAGE_SIZE)

if not os.path.exists(output_path):
    os.makedirs(output_path)


num_processed = 0
image_names = os.listdir(input_path)
for name in image_names:
    
    try:
        orig_image = Image.open(input_path + name)
        resized_image = orig_image.resize((TARGET_IMAGE_SIZE, TARGET_IMAGE_SIZE), Image.ANTIALIAS)
        resized_image.save(output_path + name)

        num_processed += 1
        if num_processed%50 == 0:
          print('Processed {} out of {} images'.format(num_processed, len(image_names)))

    except OSError as e:
        print("Processing failed for the file", name + ':', e)

print('Processed {} out of {} images'.format(num_processed, len(image_names)))
