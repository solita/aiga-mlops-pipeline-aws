import os
import PIL

# specify target image size
TARGET_IMAGE_SIZE = 832


input_path = '/opt/ml/processing/input/images/'
#output_path = '/opt/ml/processing/output/{}/'.format(str(TARGET_IMAGE_SIZE))
output_path = '/opt/ml/processing/output/images'


# counts number of processed images
num_processed = 0

image_names = os.listdir(input_path)
for name in image_names:
    
    try:
        # load original image
        orig_image = Image.open(input_path + name)

        # resize image to target resolution
        resized_image = orig_image.resize((TARGET_IMAGE_SIZE, TARGET_IMAGE_SIZE), PIL.Image.ANTIALIAS)

        # save image
        resized_image.save(output_path + name)

        # display progress
        num_processed += 1
        if num_processed%50 == 0:
          print('processed {} out of {} images'.format(num_processed, len(image_names)))

    except:
        pass

print('processed {} out of {} images'.format(num_processed, len(image_names)))