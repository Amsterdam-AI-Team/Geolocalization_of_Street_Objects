from math import sqrt

def pixel_to_viewpoint(pixel, image_width):
    """
    Convert width in pixels to viewpoint in degrees
    """
    return 360 * pixel / image_width

def viewpoint_to_pixels(viewpoint, image_width):
    """
    Convert viewpoint in degrees to width in pixels
    """
    return viewpoint / 360 * image_width

def euclidean_distance(x_1, y_1, x_2, y_2):
    """
    Calculate the Euclidean distance between two vectors
    """
    return sqrt(((x_1 - x_2)**2) + ((y_1 - y_2)**2))