import requests
import json
import csv

from osgeo import ogr
from math import sqrt
from osgeo import osr
from pathlib import Path
from panorama.client import PanoramaClient
from panorama import models


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

def get_pano_location(pano_id):
    """
    Get the initial location coordinates of a panoramic image
    and convert it from WGS84 (EPSG:4326) to Rijksdriehoek (EPSG:28992)

    Amsterdam API description: https://api.data.amsterdam.nl/api/
    """
    pano_url = f"https://api.data.amsterdam.nl/panorama/panoramas/{pano_id}/"

    try:
        response = requests.get(pano_url)
        pano_data = json.loads(response.content)
    except requests.exceptions.RequestException:
        print('HTTP Request failed. Aborting.')
        return

    # Get location coordinates
    geom = pano_data['geometry']['coordinates']

    # WGS84 to RD conversion
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(max(geom), min(geom))
    #
    source = osr.SpatialReference()
    source.ImportFromEPSG(4326)

    target = osr.SpatialReference()
    target.ImportFromEPSG(28992)

    transform = osr.CoordinateTransformation(source, target)
    point.Transform(transform)

    return [point.GetX(), point.GetY()]


def get_panos_from_points_of_interest(point_of_interest, timestamp_before, timestamp_after):
    """
    Get the panoramas that are closest to the points of interest
    Takes as input a csv file with lon, lat coordinates outputs images in the output folder
    """
    panoramas = []
    with open(point_of_interest, 'r') as file:
        reader = csv.reader(file)
        next(reader) #skip first line
        for row in reader:
            location = models.LocationQuery(
                latitude=float(row[0]), longitude=float(row[1]), radius=25
            )
            query_result: models.PagedPanoramasResponse = PanoramaClient.list_panoramas(
                location=location,
                timestamp_after=timestamp_after,
                timestamp_before=timestamp_before)
            panoramas.append(query_result.panoramas[0])
    return panoramas
