## Geospatial Localization from Panoramic Images

A refactored Python implementation of the MRF-based triangulation procedure to estimate object geolocations from bounding box predictions on imagery, introduced in "Automatic Discovery and Geotagging of Objects from Street View Imagery" by V. A. Krylov, E. Kenny, R. Dahyot.

## References
This repo is a refactored version of https://github.com/Amsterdam-AI-Team/Geolocalization_of_Street_Objects and made available in a python package.

## Requirements

- A recent version of Python 3. The project is being developed on Python 3.9, but should be compatible with some older minor versions.
- This project uses [Poetry](https://python-poetry.org/) as its package manager.

## Getting started


Install Triangulation package:

```shell
pip install git+ssh://git@github.com/Computer-Vision-Team-Amsterdam/Geolocalization_of_Street_Objects.git
```

Use the triangulation algorithm to retrieve exact location of the desired object from a COCO predictions file
:

```python
from triangulation.triangulate import triangulate

input_file = "data/coco_instances_results.json"
output_file = "output/object_locations.csv"
cluster_intersections = triangulate(input_file)
write_output(output_file, cluster_intersections)
```

There is also code to only get the side view of a panoramic image:
```python
from triangulation.masking import get_side_view_of_pano
from PIL import Image

image_width = 4000
image_height = 2000
heading = 252 # Direction of the car
mask_degrees = 90 # Number of degrees to view from the side of the car

mask = get_side_view_of_pano(image_width, image_height, heading, mask_degrees)
    with Image.open('../examples/panorama_4000.jpeg') as source_image:
        masked_image = mask_image(source_image, mask)
        masked_image.save("../examples/panorama_4000_masked.jpeg", "jpeg")
```
