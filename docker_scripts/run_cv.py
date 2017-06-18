#!/usr/bin/env python
import argparse
import json
import math
import os

import cv2
import numpy as np


parser = argparse.ArgumentParser(description='Acript for analyzing digital images vwith OpenCV')
parser.add_argument('image', help='image to process')
parser.add_argument('--paramaters', '-p', nargs='+', default=['all'], help='parameters to be calculated')
args = parser.parse_args()

image_path = os.path.join(os.sep, 'data', args.image)
image = cv2.imread(image_path)

# Get file size.
file_size = os.stat(image_path).st_size

# Get blurriness.
# Source: http://www.pyimagesearch.com/2015/09/07/blur-detection-with-opencv/
def variance_of_laplacian(image):
    """compute the Laplacian of the image and then return the focus
    measure, which is simply the variance of the Laplacian."""
    return cv2.Laplacian(image, cv2.CV_64F).var()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurriness = variance_of_laplacian(gray)

# Get histogram.

def weighted_avg_and_std(hist):
    """Return the weighted average and standard deviation."""
    values = np.arange(256)
    average = np.average(values, weights=hist)
    variance = np.average((values-average)**2, weights=hist)
    return (average, math.sqrt(variance))

hist = cv2.calcHist([image],[0],None,[256],[0,256]).flatten()
brightnes_average, brightnes_stddev = weighted_avg_and_std(hist)


print(json.dumps({
    'blurriness': round(blurriness, 2),
    'histogram': {
        'brightnes_average': round(brightnes_average, 2),
        'brightnes_stddev': round(brightnes_stddev, 2),
    },
    'file_size': file_size,
}))
