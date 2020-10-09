"""
Visualize viewpoints of multiple panoramic images
"""
import argparse
import math
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from src.api_request import get_pano_location, get_pano_data
from src.geometry import pixel_to_viewpoint

PANO_WIDTH = 2000 # pixels

def visualize_viewpoints_top_view(objects_base):
    """
    Top view visualization of possible object intersections
    """

    # Get min and max dimensions
    x_max = max(objects_base, key=lambda item: item[2])[2]
    x_min = min(objects_base, key=lambda item: item[2])[2]
    y_max = max(objects_base, key=lambda item: item[3])[3]
    y_min = min(objects_base, key=lambda item: item[3])[3]

    # Plot directions in 2D upper view
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)

    # Set the data limits for the x- and yaxis
    ax.set_xlim([x_min-10, x_max+10])
    ax.set_ylim([y_min-10, y_max+10])

    for pano in objects_base:
        # Viewpoints of front and back of vehicle from degrees to radians
        viewpoint_front_radians = math.radians(90 + (180 - pano[1]))
        viewpoint_back_radians = math.radians(90 + (360 - pano[1]))
        viewpoint_object = pixel_to_viewpoint(pano[4], PANO_WIDTH)
        viewpoint_object_radians = math.radians(90 + (180 - viewpoint_object))

        # Plot initial location of panoramic image
        ax.plot(pano[2], pano[3], 'o', color = 'k')
        ax.annotate('{}'.format(pano[0]), (pano[2], pano[3]))

        # Plot front direction of vehicle
        ax.arrow(pano[2], pano[3],
                 math.cos(viewpoint_front_radians), math.sin(viewpoint_front_radians),
                 head_width=0.1, head_length=0.1, color = 'red')

        # Plot back direction of vehicle
        ax.arrow(pano[2], pano[3],
                 math.cos(viewpoint_back_radians), math.sin(viewpoint_back_radians),
                 head_width=0.1, head_length=0.1, color = 'blue')

        # Plot direction line to object
        ax.plot([pano[2], pano[2] + (15 * math.cos(viewpoint_object_radians))],
                [pano[3], pano[3] + (15 * math.sin(viewpoint_object_radians))],
                '--', color = 'green')

    # Save the image
    plt.grid()
    plt.savefig("examples/top_view.jpeg", dpi=300)

if __name__ == '__main__':
    # Read command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--csv_file', type=str, required=True,
                        help='Input csv file (output of Faster R-CNN)')
    args = parser.parse_args()

    objects_base = []
    with open(args.csv_file, "r") as f:
        next(f)  # skip the first line
        for line in f:
            nums = line.split(",")
            if len(nums) < 2:
                print("Broken entry ignored")
                continue
            if len(nums) < 3:
                pano_id, center_bbox = nums[0], float(nums[1])

            # API calls
            initial_location = get_pano_location(pano_id)
            _, heading = get_pano_data(pano_id)

            objects_base.append((
                pano_id,
                heading,
                initial_location[0], # x
                initial_location[1], # y
                center_bbox
            ))

    # Visualize viewpoints and possible intersections
    visualize_viewpoints_top_view(objects_base)
