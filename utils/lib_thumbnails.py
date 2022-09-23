from keras.preprocessing.image import img_to_array, load_img

import os
import numpy as np
from PIL import Image

def extract_thumbnails(container_path, thumb_path):
    path, dirs, files = next(os.walk(container_path))
    file_count = len(files)
    print("Extracting frames %s from containers: %s" % (file_count*25, file_count))

    print("Processing...")
    # Thumbnail Size
    cropx = 160
    cropy = 90
    
    frameNumber = 0

    # load all images in a directory
    for imageName in os.listdir(container_path):
        starty = 0
        startx = 0

        filename = os.path.splitext(imageName)[0] #filename without extention

        im = np.array(Image.open(os.path.join(container_path, imageName)))
        for i in range(25):
        
            crop = im[starty:starty+cropy, startx:startx+cropx,:]
            Image.fromarray(crop).save(os.path.join(thumb_path, str(filename))+"_%1d.jpg" % (i+1))

            startx = startx + cropx
            if i == 4:
                startx = 0
                starty = starty + cropy
            elif (i == 9):
                startx = 0
                starty = starty + cropy
            elif (i == 14):
                startx = 0
                starty = starty + cropy
            elif (i == 19):
                startx = 0
                starty = starty + cropy

        frameNumber = frameNumber + 1
    print("containers_path %s : thumbanils_path %s" % (container_path, thumb_path))
    print('thumbails extraction process completed')

#Process an image that we can pass to our networks.
def process_image(image, target_shape):
    """Given an image, process it and return the array."""
    # Load the image.
    h, w, _ = target_shape
    image = load_img(image, target_size=(h, w))

    # Turn it into numpy, normalize and return.
    img_arr = img_to_array(image)
    x = (img_arr / 255.).astype(np.float32)

    return x
