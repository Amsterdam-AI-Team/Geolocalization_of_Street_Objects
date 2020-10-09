"""
Visualize viewpoints of one panoramic image
"""
import argparse
from io import BytesIO
import requests
from PIL import Image
import numpy as np

from src.api_request import get_pano_data
from src.geometry import viewpoint_to_pixels

PANO_WIDTH = 2000 # pixels
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)

def visualize_viewpoints_street_view(pano_url, bbox, center_bbox, heading):
    """
    Save visualization of viewpoint directions of one panoramic image
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
    img.save("examples/street_view.jpeg", "jpeg")

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
    panoramic_image, heading = get_pano_data(args.pano_id)

    # Get the horizontal center of a bbox
    center_bbox = (bbox[0] + bbox[2]) / 2

    # Visualize viewpoints
    visualize_viewpoints_street_view(panoramic_image, bbox, center_bbox, heading)
