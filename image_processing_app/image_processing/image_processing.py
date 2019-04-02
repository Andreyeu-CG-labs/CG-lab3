from shutil import copyfile

import cv2
import imageio
import math
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

from image_processing_app.image_processing.utils import apply_operation, \
    equalize_channel, hsv_to_rgb


def update_image(form_data):
    copyfile('image_processing_app/static/image.png',
             'image_processing_app/static/current_image.png')
    image = Image.open('image_processing_app/static/current_image.png')
    image_array = np.asarray(image.convert('L'))
    result_array = image_array.copy()

    if form_data['add_constant']:
        apply_operation(
            lambda pixel: pixel + form_data['add_constant'],
            result_array
        )
    if form_data['multiply_constant']:
        apply_operation(
            lambda pixel: pixel * form_data['multiply_constant'],
            result_array
        )
    if form_data['power_transform']:
        max_pixel = result_array.max()
        apply_operation(
            lambda pixel: 255 * ((pixel / max_pixel)
                                 ** form_data['power_transform']),
            result_array
        )
    if form_data['logarithmic_transformation']:
        max_pixel = result_array.max()
        apply_operation(
            lambda pixel: 255 * math.log(1 + pixel) / math.log(1 + max_pixel),
            result_array
        )
    if form_data['negative']:
        max_pixel = result_array.max()
        apply_operation(
            lambda pixel: 255 - pixel,
            result_array
        )
    if form_data['linear_contrasting']:
        max_pixel = result_array.max()
        min_pixel = result_array.min()
        apply_operation(
            lambda pixel: 255 * (pixel - min_pixel) / (max_pixel - min_pixel),
            result_array
        )

    if any([value for option, value in form_data.items()
            if option != 'histogram_equalization']):
        imageio.imwrite('image_processing_app/static/current_image.png',
                        result_array)

    if form_data['histogram_equalization'] == 'rgb':
        equalize_rgb_histogram()
    elif form_data['histogram_equalization'] == 'hsv':
        equalize_brightness_histogram()


def equalize_rgb_histogram():
    image = Image.open('image_processing_app/static/current_image.png')
    image_array = np.asarray(image)
    result_array = image_array.copy()

    for i in range(3):
        equalize_channel(result_array, i)

    imageio.imwrite('image_processing_app/static/current_image.png',
                    result_array)


def equalize_brightness_histogram():
    image = Image.open('image_processing_app/static/current_image.png')
    image_array = np.asarray(image.convert('HSV'))
    result_array = image_array.copy()

    equalize_channel(result_array, 2)

    hsv_to_rgb(result_array)

    imageio.imwrite('image_processing_app/static/current_image.png',
                    result_array)


def update_histograms():
    update_brightness_histogram()
    update_rgb_histogram()


def update_brightness_histogram():
    img = cv2.imread('image_processing_app/static/current_image.png', 0)
    plt.hist(img.ravel(), 256, [0, 256])
    plt.xlim([0, 256])
    plt.savefig('image_processing_app/static/brightness_histogram.png',
                bbox_inches='tight')
    plt.close()


def update_rgb_histogram():
    img = cv2.imread('image_processing_app/static/current_image.png')
    color = ('b', 'g', 'r')
    for i, col in enumerate(color):
        histr = cv2.calcHist([img], [i], None, [256], [0, 256])
        plt.plot(histr, color=col)
        plt.xlim([0, 256])
    plt.savefig('image_processing_app/static/rgb_histogram.png',
                bbox_inches='tight')
    plt.close()
