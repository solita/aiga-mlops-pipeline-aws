import os
from PIL import Image


TARGET_IMAGE_SIZE = 416

input_path = '/opt/ml/processing/input/images/'
output_path = '/opt/ml/processing/output/resized_images/{}/images/'.format(TARGET_IMAGE_SIZE)


num_processed = 0
image_names = os.listdir(input_path)
for name in image_names:
    
    try:
        # load original image
        orig_image = Image.open(input_path + name)

        # resize image to target resolution
        resized_image = orig_image.resize((TARGET_IMAGE_SIZE, TARGET_IMAGE_SIZE), Image.ANTIALIAS)

        # save image
        resized_image.save(output_path + name)

        # display progress
        num_processed += 1
        if num_processed%50 == 0:
          print('Processed {} out of {} images'.format(num_processed, len(image_names)))

    except:
        print("Processing failed for:", name)

print('Processed {} out of {} images'.format(num_processed, len(image_names)))
