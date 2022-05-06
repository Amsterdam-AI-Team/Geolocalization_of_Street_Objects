Geospatial Localization from Panoramic Images

This repo is a refactored version of https://github.com/Amsterdam-AI-Team/Geolocalization_of_Street_Objects and made available in a python package.

The original author summaries the functionality as:

A refactored Python implementation of the MRF-based triangulation procedure to estimate object geolocations from bounding box predictions on imagery, introduced in "Automatic Discovery and Geotagging of Objects from Street View Imagery" by V. A. Krylov, E. Kenny, R. Dahyot.


---

## Getting started

```
Install the triangulation depedency:

```shell
pip install triangulation
```

Use the triangulation algorithm to retrieve exact location of the desired object from a COCO predictions file
:
```python
from triangulation.triangulation import triangulate
input_file = "coco_instances_results.json"
output_file = "object_locations.csv"
triangulate(input_file, output_file)
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