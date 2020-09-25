"""
Visualize viewpoints of a panoramic image on street view and top view
"""
import argparse
import requests
import json
import math
from osgeo import ogr, osr
from PIL import Image
from io import BytesIO
import numpy as np
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from src.api_request import get_pano_location, get_pano_data
from src.geometry import viewpoint_to_pixels, pixel_to_viewpoint

PANO_WIDTH = 2000 # pixels
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)

def visualize_viewpoint_street_view(pano_url, bbox, center_bbox, heading):
    """
    Street view visualization
    :param pano_url: Url of a panoramic image 
    :param bbox: Bbox coordinates of an object
    :param center_bbox: Horizontal center of a bbox
    :param heading: Horizontal rotation angle of the camera
    :return: Save the image
    """

    # Get the panoramic image
    try:
        response = requests.get(pano_url)
        source_image = Image.open(BytesIO(response.content))
    except requests.exceptions.RequestException:
        print("HTTP Request failed. Aborting.")
        return

    # Convert the viewpoints (in degrees) to pixel values
    viewpoint_front = viewpoint_to_pixels(heading, PANO_WIDTH)
    viewpoint_back = viewpoint_to_pixels(heading - 180, PANO_WIDTH)
    
    # Draw the front and back viewpoints of the vehicle
    np_image = np.array(source_image)
    np_image[:, int(viewpoint_front), :] = RED
    np_image[:, int(viewpoint_back), :] = BLUE
    
    # Draw a bbox around the detected object
    x_min, y_min, x_max, y_max = bbox    
    np_image[y_min:y_max, x_min, :] = GREEN
    np_image[y_min:y_max, x_max, :] = GREEN
    np_image[y_min, x_min:x_max, :] = GREEN
    np_image[y_max, x_min:x_max, :] = GREEN
    
    # Draw a line through the center of the bbox
    np_image[:, int(center_bbox), :] = GREEN
    
    # Save the image
    img = Image.fromarray(np_image, "RGB")
    img.save(f"examples/street_view.jpeg", "jpeg")

def visualize_viewpoint_top_view(initial_location, center_bbox, heading):
    """
    Top view visualization
    :param initial_location: Location at which the panoramic image was taken
    :param center_bbox: Horizontal center of a bbox
    :param heading: Horizontal rotation angle of the camera
    :return: Save the image
    """
        
    # Viewpoints of front and back of vehicle from degrees to radians
    viewpoint_front_radians = math.radians(90 + (180 - heading))
    viewpoint_back_radians = math.radians(90 + (360 - heading))
    viewpoint_object = pixel_to_viewpoint(center_bbox, PANO_WIDTH)
    viewpoint_object_radians = math.radians(90 + (180 - viewpoint_object))
    
    # Plot directions in 2D upper view
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)
    
    # Set the data limits for the x- and yaxis
    ax.set_xlim([initial_location[0]-8, initial_location[0]+8])
    ax.set_ylim([initial_location[1]-8, initial_location[1]+8])
    
    # Plot initial location of panoramic image
    ax.plot(initial_location[0], initial_location[1], 'o', color = 'k')
    
    # Plot front direction of vehicle
    ax.arrow(initial_location[0], initial_location[1], 
             math.cos(viewpoint_front_radians), math.sin(viewpoint_front_radians),
             head_width=0.1, head_length=0.1, color = 'red')

    # Plot back direction of vehicle
    ax.arrow(initial_location[0], initial_location[1], 
             math.cos(viewpoint_back_radians), math.sin(viewpoint_back_radians),
             head_width=0.1, head_length=0.1, color = 'blue')

    # Plot direction line to object
    ax.plot([initial_location[0], initial_location[0] + (2 * math.cos(viewpoint_object_radians))],
            [initial_location[1], initial_location[1] + (2 * math.sin(viewpoint_object_radians))],
            '--', color = 'green')

    # Save the image
    plt.grid()
    plt.savefig("examples/top_view.jpeg", dpi=300)
        
if __name__ == '__main__':
    # Read command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bbox', type=str, required=True,
                        help='Bounding box of the detected bicycle symbol: x_min y_min x_max y_max')
    parser.add_argument('-p', '--pano_id', type=str, required=True,
                        help='Id of the panoramic image')
    args = parser.parse_args()

    bbox = [int(item)for item in args.bbox.split(',')]

    # API calls
    initial_location = get_pano_location(args.pano_id)
    panoramic_image, heading = get_pano_data(args.pano_id)
    
    # Get the horizontal center of a bbox
    center_bbox = (bbox[0] + bbox[2]) / 2
    
    # Visualize viewpoints
    visualize_viewpoint_street_view(panoramic_image, bbox, center_bbox, heading)
    visualize_viewpoint_top_view(initial_location, center_bbox, heading)
