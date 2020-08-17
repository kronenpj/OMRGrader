#!/usr/bin/env python3

import argparse
import inspect
import logging
import sys

import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar

logging.basicConfig()
global_log = logging.getLogger(__package__)
log = global_log.getChild(__name__.replace(f"{__package__}.", ""))
log.setLevel(global_log.getEffectiveLevel())

"""
Decode routine from https://www.learnopencv.com/barcode-and-qr-code-scanner-using-zbar-and-opencv/

Updates by Paul Kronenwetter <n2kiq0@gmail.com>
Extracts QR code from VE exam sheets as text / text + encoded answers for grading randomized exams. 
"""


def zbar_decode_file(in_file: str) -> list:
    mylog = log.getChild(f"{inspect.currentframe().f_code.co_name}")
    mylog.setLevel(global_log.getEffectiveLevel())
    mylog.debug(f"Entering...")

    # Consume image file
    im = cv2.imread(in_file)
    return zbar_decode(im)


def zbar_decode(im) -> list:
    mylog = log.getChild(f"{inspect.currentframe().f_code.co_name}")
    mylog.setLevel(global_log.getEffectiveLevel())
    mylog.debug(f"Entering...")

    # Find barcodes and QR codes
    decoded_objects = pyzbar.decode(im)

    # zbar_display(im, decoded_objects)

    data = list()
    # Collect results
    for obj in decoded_objects:
        # Obj has two attributes we know about: obj.type and obj.data
        data.append(obj.data)

    return data


# Display barcode and QR code location
def zbar_display(im, decoded_objects):
    mylog = log.getChild(f"{inspect.currentframe().f_code.co_name}")
    mylog.setLevel(global_log.getEffectiveLevel())
    mylog.debug(f"Entering...")

    # Loop over all decoded objects
    for decoded_object in decoded_objects:
        points = decoded_object.polygon

        # If the points do not form a quad, find convex hull
        if len(points) > 4:
            hull = cv2.convexHull(
                np.array([point for point in points], dtype=np.float32)
            )
            hull = list(map(tuple, np.squeeze(hull)))
        else:
            hull = points

        # Number of points in the convex hull
        n = len(hull)

        # Draw the convex hull
        for j in range(0, n):
            cv2.line(im, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)

    # Display results
    cv2.imshow("Results", im)
    cv2.waitKey(0)


def arg_parser():
    log.debug(f"Entering arg_parser...")

    log.debug(f"Number of arguments: {len(sys.argv)}")

    argp = argparse.ArgumentParser(description="An amateur radio exam importer.")
    argp.add_argument("inputfile", nargs="*", type=str, default=None)
    args: argparse.Namespace = argp.parse_args()
    return args


def main():
    args = arg_parser()

    for input_file in args.inputfile:
        data = zbar_decode_file(in_file=input_file)
        for d in data:
            print(f"Extracted: {d}")


# Main
if __name__ == "__main__":
    main()
