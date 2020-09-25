import requests
import json
from osgeo import ogr, osr

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
    point.AddPoint(geom[0], geom[1])
    
    source = osr.SpatialReference()
    source.ImportFromEPSG(4326)
    
    target = osr.SpatialReference()
    target.ImportFromEPSG(28992)
    
    transform = osr.CoordinateTransformation(source, target)
    point.Transform(transform)

    return [point.GetX(), point.GetY()]

def get_pano_data(pano_id):
    """
    Get panoramic image url and orientation information using the API
    """
    pano_url = f"https://api.data.amsterdam.nl/panorama/panoramas/{pano_id}/" 
    
    try:
        response = requests.get(pano_url)
        pano_data = json.loads(response.content)
    except requests.exceptions.RequestException:
        print('HTTP Request failed. Aborting.')
        return
    
    # Get panoramic image from API
    image_url = pano_data['_links']['equirectangular_small']['href']
    
    # Get heading
    heading = pano_data['heading']

    return image_url, heading