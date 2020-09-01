import cv2
import os
import imutils
import numpy as np
from matplotlib import pyplot as plt
from imutils import contours
from skimage import measure
from PIL import Image


def find_dominant_color(filename):
    # Resizing parameters
    width, height = 600, 600
    image = Image.open(filename)
    # Get colors from image object
    pixels = image.getcolors(width * height)
    # Sort them by count number(first element of tuple)
    sorted_pixels = sorted(pixels, key=lambda t: t[0])
    # Get the most frequent color
    dominant_color = sorted_pixels[-1][1]
    return dominant_color


def find_defects(filename):
    # Read image
    filepath = os.path.join("app", "media", "images", filename)
    image = cv2.imread(filepath)
    lightImage = False

    # find threshold t1 and t2
    img = find_dominant_color(filepath)
    if img <= (45, 45, 45):
        t1, t2 = 67 * (1 - ((45 - (img)[0])) / 100), 90 * (1 - ((45 - (img)[0])) / 100)

    elif (img < (93, 93, 93)) & (img > (45, 45, 45)):
        image = cv2.resize(image, (600, 600))
        t1, t2 = 67 * (1 + (((img)[0]) - 45) / 100), 90 * ((1 + ((img)[0]) - 45) / 100)

    elif find_dominant_color(filepath) >= (93, 93, 93):
        lightImage = True
        image = cv2.resize(image, (600, 600))
        image = cv2.normalize(image, image, 0, 255, cv2.NORM_MINMAX)

    # apply filters
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gaussian = cv2.GaussianBlur(grey, (7, 7), 1)

    if lightImage:
        t1, t2 = (gaussian.max() - 13), gaussian.max()

    thresh = cv2.threshold(gaussian, t1, t2, cv2.THRESH_BINARY)[1]

    kernel = np.ones((5, 5), np.float32) / 25
    dst = cv2.morphologyEx(thresh, cv2.MORPH_GRADIENT, kernel)

    labels = measure.label(dst, neighbors=8, background=0)
    mask = np.zeros(dst.shape, dtype="uint8")

    for label in np.unique(labels):
        if label == 0:
            continue

        labelMask = np.zeros(dst.shape, dtype="uint8")
        labelMask[labels == label] = 255
        numPixels = cv2.countNonZero(labelMask)
        if numPixels <= 20:
            mask = cv2.add(mask, labelMask)

    defects = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    defects = imutils.grab_contours(defects)
    defects = contours.sort_contours(defects)[0]

    # Draw bounding boxes on image
    for (i, c) in enumerate(defects):
        (x, y, w, h) = cv2.boundingRect(c)
        ((cX, cY), radius) = cv2.minEnclosingCircle(c)
        cv2.circle(image, (int(cX), int(cY)), int(radius), (245, 197, 66), 2)

    # # Plotting the image, You can delete this tho if you want to save the image into the media folder
    # plt.subplot(1, 1, 1), plt.imshow(image), plt.title("Calculated")
    # plt.xticks([]), plt.yticks([])
    # plt.show()

    # to save the file in media folder
    dot = filename.find(".")
    ret = filename[:dot] + "_recognized" + filename[dot:]
    write = os.path.join("app", "static", "images", ret)

    cv2.imwrite(write, image)
    return ret
