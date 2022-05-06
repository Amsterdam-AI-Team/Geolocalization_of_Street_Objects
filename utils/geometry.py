from math import sqrt
from osgeo import osr

def rd_to_wgs(coords):
    """
    Convert rijksdriehoekcoordinates into WGS84 cooridnates. Input parameters: x (float), y (float).
    """
    epsg28992 = osr.SpatialReference()
    epsg28992.ImportFromEPSG(28992)

    epsg4326 = osr.SpatialReference()
    epsg4326.ImportFromEPSG(4326)

    rd2latlon = osr.CoordinateTransformation(epsg28992, epsg4326)
    lonlatz = rd2latlon.TransformPoint(coords[0], coords[1])
    return lonlatz[:2]

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