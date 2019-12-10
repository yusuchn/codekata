"""
main code comes from this example https://www.pyimagesearch.com/2014/07/21/detecting-circles-images-using-opencv-hough-circles/
docs on `cv2.HoughCircles()` https://www.docs.opencv.org/2.4/doc/tutorials/imgproc/imgtrans/hough_circle/hough_circle.html
docs on  `cv2.GaussianBlur()` https://www.tutorialkart.com/opencv/python/opencv-python-gaussian-image-smoothing/

the main thing i did to reduce false positives is to increase the value of the
4th parameter (min_dist) which is the "Minimum distance between detected centers"

run the script with

    $> python machine_vision.py <path to image>

"""
# import the necessary packages
import numpy as np
import argparse
import cv2

# # construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True, help="Path to the image")
# args = vars(ap.parse_args())

# load the image, clone it for output, and then convert it to grayscale
# image = cv2.imread(args["image"])
image = cv2.imread("fromserver_1..png")
output = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), cv2.BORDER_DEFAULT)

print(gray.shape)
print(output.shape)

# detect circles in the image
circles = cv2.HoughCircles(
    # gray, cv2.HOUGH_GRADIENT, 0.9, 500, param2=1, minRadius=1, maxRadius=20  # success, 2 false positives
    gray, cv2.HOUGH_GRADIENT, 0.9, 1600, param2=1, minRadius=1, maxRadius=20  # success,
)

# ensure at least some circles were found
if circles is not None:
    # convert the (x, y) coordinates and radius of the circles to integers
    circles = np.round(circles[0, :]).astype("int")

    # loop over the (x, y) coordinates and radius of the circles
    for (x, y, r) in circles:
        # draw the circle in the output image, then draw a rectangle
        # corresponding to the center of the circle
        cv2.circle(output, (x, y), r, (0, 255, 0), 4)
        cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        print("({}, {})".format(x, y))

    # show the output image
    # cv2.imshow("output", np.hstack([image, output]))
    cv2.imshow("output", output)
    # cv2.imshow("output", gray)
    cv2.waitKey(0)
